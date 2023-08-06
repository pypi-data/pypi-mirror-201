import json
import logging
import pickle
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, cast

import httpx
from httpx import AsyncClient, NetworkError

from ._cache import getCacheDir
from ._constants import DEVICE_NAME
from ._keystore import KeyStore
from ._unit import Group, Scene, Unit, UnitControl, UnitControlType, UnitType
from .errors import (
    AuthenticationError,
    NetworkNotFoundError,
    NetworkOnlineUpdateNeededError,
    NetworkUpdateError,
)


@dataclass()
class _NetworkSession:
    session: str
    network: str
    manager: bool
    keyID: int
    expires: datetime

    role: int = 3  # TODO: Support other role types?

    def expired(self) -> bool:
        return datetime.utcnow() > self.expires


class Network:
    def __init__(self, uuid: str, httpClient: AsyncClient) -> None:
        self._session: Optional[_NetworkSession] = None

        self._networkName: Optional[str] = None
        self._networkRevision: Optional[int] = None

        self._unitTypes: dict[int, UnitType] = {}
        self.units: list[Unit] = []
        self.groups: list[Group] = []
        self.scenes: list[Scene] = []

        self._logger = logging.getLogger(__name__)
        # TODO: Create LoggingAdapter to prepend uuid.

        self._id: Optional[str] = None
        self._uuid = uuid
        self._httpClient = httpClient

        self._cachePath = getCacheDir(uuid)
        self._keystore = KeyStore(self._cachePath)

        self._sessionPath = self._cachePath / "session.pck"
        if self._sessionPath.exists():
            self._loadSession()

        self._typeCachePath = self._cachePath / "types.pck"
        if self._typeCachePath.exists():
            self._loadTypeCache()

    def _loadSession(self) -> None:
        self._logger.info("Loading session...")
        self._session = pickle.load(self._sessionPath.open("rb"))

    def _saveSesion(self) -> None:
        self._logger.info("Saving session...")
        pickle.dump(self._session, self._sessionPath.open("wb"))

    def _loadTypeCache(self) -> None:
        self._logger.info("Loading unit type cache...")
        self._unitTypes = pickle.load(self._typeCachePath.open("rb"))

    def _saveTypeCache(self) -> None:
        self._logger.info("Saving type cache...")
        pickle.dump(self._unitTypes, self._typeCachePath.open("wb"))

    async def getNetworkId(self, forceOffline: bool = False) -> None:
        self._logger.info("Getting network id...")

        networkCacheFile = self._cachePath / "networkid"

        if networkCacheFile.exists():
            self._id = networkCacheFile.read_text()

        if forceOffline:
            if not self._id:
                raise NetworkOnlineUpdateNeededError("Network isn't cached.")
            else:
                return

        getNetworkIdUrl = f"https://api.casambi.com/network/uuid/{self._uuid}"
        try:
            res = await self._httpClient.get(getNetworkIdUrl)
        except NetworkError as err:
            if not self._id:
                raise NetworkOnlineUpdateNeededError from err
            else:
                self._logger.warning(
                    "Network error while fetching network id. Continuing with cache.",
                    exc_info=True,
                )
                return

        if res.status_code == httpx.codes.NOT_FOUND:
            raise NetworkNotFoundError(
                "API failed to find network. Is your network configured correctly?"
            )
        if res.status_code != httpx.codes.OK:
            raise NetworkNotFoundError(
                f"Getting network id returned unexpected status {res.status_code}"
            )

        new_id = cast(str, res.json()["id"])
        if self._id != new_id:
            self._logger.info(f"Network id changed from {self._id} to {new_id}.")
            networkCacheFile.write_text(new_id)
            self._id = new_id
        self._logger.info(f"Got network id {self._id}.")

    def authenticated(self) -> bool:
        if not self._session:
            return False
        return not self._session.expired()

    def getKeyStore(self) -> KeyStore:
        return self._keystore

    async def logIn(self, password: str, forceOffline: bool = False) -> None:
        await self.getNetworkId(forceOffline)

        # No need to be authenticated if we try to be offline anyway.
        if self.authenticated() or forceOffline:
            return

        self._logger.info("Logging in to network...")
        getSessionUrl = f"https://api.casambi.com/network/{self._id}/session"

        res = await self._httpClient.post(
            getSessionUrl, json={"password": password, "deviceName": DEVICE_NAME}
        )
        if res.status_code == httpx.codes.OK:
            # Parse session
            sessionJson = res.json()
            sessionJson["expires"] = datetime.utcfromtimestamp(
                sessionJson["expires"] / 1000
            )
            self._session = _NetworkSession(**sessionJson)
            self._logger.info("Login sucessful.")
            self._saveSesion()
        else:
            raise AuthenticationError(f"Login failed: {res.status_code}\n{res.text}")

    async def update(self, forceOffline: bool = False) -> None:
        self._logger.info("Updating network...")
        if not self.authenticated() and not forceOffline:
            raise AuthenticationError("Not authenticated!")

        assert self._id is not None, "Network id must be set."

        # TODO: Save and send revision to receive actual updates?

        cachedNetworkPah = self._cachePath / f"{self._id}.json"
        if cachedNetworkPah.exists():
            network = json.loads(cachedNetworkPah.read_bytes())
            self._networkRevision = network["network"]["revision"]
            self._logger.info(
                f"Loaded cached network. Revision: {self._networkRevision}"
            )
        else:
            if forceOffline:
                raise NetworkOnlineUpdateNeededError("Network isn't cached.")
            self._networkRevision = 0

        if not forceOffline:
            getNetworkUrl = f"https://api.casambi.com/network/{self._id}/"

            # **SECURITY**: Do not set session header for client! This could leak the session with external clients.
            res = await self._httpClient.put(
                getNetworkUrl,
                json={
                    "formatVersion": 1,
                    "deviceName": DEVICE_NAME,
                    "revision": self._networkRevision,
                },
                headers={"X-Casambi-Session": self._session.session},  # type: ignore[union-attr]
            )

            if res.status_code != httpx.codes.OK:
                self._logger.error(f"Update failed: {res.status_code}\n{res.text}")
                raise NetworkUpdateError("Could not update network!")

            self._logger.debug(f"Network: {res.text}")

            updateResult = res.json()
            if updateResult["status"] != "UPTODATE":
                self._networkRevision = updateResult["network"]["revision"]
                cachedNetworkPah.write_bytes(res.content)
                network = updateResult
                self._logger.info(
                    f"Fetched updated network with revision {self._networkRevision}"
                )

        # Prase general information
        self._networkName = network["network"]["name"]

        # Parse keys if there are any. Otherwise the network is probably a classic network.
        if "keyStore" in network["network"]:
            keys = network["network"]["keyStore"]["keys"]
            for k in keys:
                self._keystore.addKey(k)

        # TODO: Parse managerKey and visitorKey for classic networks.

        # Parse units
        self.units = []
        units = network["network"]["units"]
        for u in units:
            uType = await self._fetchUnitInfo(u["type"])
            uObj = Unit(
                u["type"],
                u["deviceID"],
                u["uuid"],
                u["address"],
                u["name"],
                str(u["firmware"]),
                uType,
            )
            self.units.append(uObj)

        # Parse cells
        self.groups = []
        cells = network["network"]["grid"]["cells"]
        for c in cells:
            # Only one type at top level is currently supported
            if c["type"] != 2:
                continue

            # Parse group members
            group_units = []
            # We assume no nested groups here
            for subC in c["cells"]:
                # Ignore everyting that isn't a unit
                if subC["type"] != 1:
                    continue

                unitMatch = list(
                    filter(lambda u: u.deviceId == subC["unit"], self.units)
                )
                if len(unitMatch) != 1:
                    self._logger.warning(
                        f"Incositent unit reference to {subC['unit']} in group {c['groupID']}. Got {len(unitMatch)} matches."
                    )
                    continue
                group_units.append(unitMatch[0])

            gObj = Group(c["groupID"], c["name"], group_units)
            self.groups.append(gObj)

        # Parse scenes
        self.scenes = []
        scenes = network["network"]["scenes"]
        for s in scenes:
            sObj = Scene(s["sceneID"], s["name"])
            self.scenes.append(sObj)

        # TODO: Parse more stuff

        self._saveTypeCache()

        self._logger.info("Network updated.")

    async def _fetchUnitInfo(self, id: int) -> UnitType:
        self._logger.info(f"Fetching unit type for id {id}...")

        # Check whether unit type is already cached
        cachedType = self._unitTypes.get(id)
        if cachedType:
            self._logger.info("Using cached type.")
            return cachedType

        getUnitInfoUrl = f"https://api.casambi.com/fixture/{id}"
        async with AsyncClient() as request:
            res = await request.get(getUnitInfoUrl)

        if res.status_code != httpx.codes.OK:
            self._logger.error(f"Getting unit info returned {res.status_code}")

        unitTypeJson = res.json()

        # Parse UnitControls
        controls = []
        for controlJson in unitTypeJson["controls"]:
            typeStr = controlJson["type"].upper()
            try:
                type = UnitControlType[typeStr]
            except KeyError:
                self._logger.warning(
                    f"Unsupported control mode {typeStr} in fixture {id}."
                )
                type = UnitControlType.UNKOWN

            controlObj = UnitControl(
                type,
                controlJson["offset"],
                controlJson["length"],
                controlJson["default"],
                controlJson["readonly"],
                controlJson["min"] if "min" in controlJson else None,
                controlJson["max"] if "max" in controlJson else None,
            )

            controls.append(controlObj)

        # Parse UnitType
        unitTypeObj = UnitType(
            unitTypeJson["id"],
            unitTypeJson["model"],
            unitTypeJson["vendor"],
            unitTypeJson["mode"],
            unitTypeJson["stateLength"],
            controls,
        )

        # Chache unit type
        self._unitTypes[unitTypeObj.id] = unitTypeObj

        self._logger.info("Sucessfully fetched unit type.")
        return unitTypeObj

    async def disconnect(self) -> None:
        return None
