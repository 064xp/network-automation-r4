from __future__ import annotations
from typing import Union, cast
from netmiko import BaseConnection
from typing import TYPE_CHECKING

from .ConnectionInfo import ConnectionInfo
from .StateClasses.DeviceHealth import DeviceHealth

if TYPE_CHECKING:
    from .StateClasses.Interface import Interface


class NetDevice:
    hostname = ""
    domainName: str = ""
    connectionInfo: ConnectionInfo
    conn: BaseConnection
    interfaces: list[Interface]
    deviceHealth: DeviceHealth
    visited = False

    def __init__(self, connectionInfo: Union[ConnectionInfo, None] = None):
        if connectionInfo is None:
            return

        self.connectionInfo = connectionInfo

    def connect(self):
        if self.connectionInfo is None:
            raise AttributeError("Connection info not set")
        self.connectionInfo.connect()
        self.conn = cast(BaseConnection, self.connectionInfo.conn)

    def getDeviceID(self):
        return self.hostname + \
            "." if self.domainName != "" else "" + \
            self.domainName
