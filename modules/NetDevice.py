from __future__ import annotations
from typing import Union, cast
from netmiko import BaseConnection
from typing import TYPE_CHECKING

from .ConnectionInfo import ConnectionInfo
from .StateClasses.DeviceHealth import DeviceHealth

if TYPE_CHECKING:
    from .StateClasses.Interface import Interface


class NetDevice:

    def __init__(self, connectionInfo: Union[ConnectionInfo, None] = None):
        self.hostname = ""
        self.domainName: str = ""
        self.connectionInfo: ConnectionInfo
        self.conn: BaseConnection
        self.interfaces: list[Interface]
        self.deviceHealth: DeviceHealth
        self.visited = False

        if connectionInfo is None:
            return

        self.connectionInfo = connectionInfo

    def connect(self):
        if self.connectionInfo is None:
            raise AttributeError("Connection info not set")
        self.connectionInfo.connect()
        self.conn = cast(BaseConnection, self.connectionInfo.conn)

    def getDeviceID(self) -> str:
        deviceID = self.hostname
        if len(self.domainName) > 0:
            deviceID += '.' + self.domainName

        return deviceID
