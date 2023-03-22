from typing import Union
import typing
from .ConnectionInfo import ConnectionInfo
from netmiko import BaseConnection
# from .StateClasses.Interface import Interface


class NetDevice:
    hostname = ""
    domainName: str = ""
    connectionInfo: ConnectionInfo
    conn: BaseConnection
    # interfaces: list[Interface]

    def __init__(self, connectionInfo: Union[ConnectionInfo, None] = None):
        if connectionInfo is None:
            return

        self.connectionInfo = connectionInfo

    def connect(self):
        if self.connectionInfo is None:
            raise AttributeError("Connection info not set")
        self.connectionInfo.connect()
        self.conn = typing.cast(BaseConnection, self.connectionInfo.conn)

    def getDeviceID(self):
        return self.hostname + "." + self.domainName
