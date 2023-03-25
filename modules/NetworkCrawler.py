from collections import OrderedDict
from typing import Union, cast

from modules.NetDevice import NetDevice
from modules.ConnectionInfo import ConnectionInfo
from modules.InformationModules.BasicInformation import BasicInformation
from modules.InformationModules.InterfaceInformation import InterfaceInformation
from modules.InformationModules.Healthcheck import Healthcheck
from modules.InformationModules.BGPInformation import BGPInformation
from modules.StateClasses.Connection import Connection


class NetworkCrawler:
    def __init__(
            self,
            defaultCredentials: dict[str, str],
            credentialMap: dict[str, dict[str, str]],
    ):
        self.defaultCredentials: dict[str, str] = defaultCredentials
        self.credentialMap: dict[str, dict[str, str]] = credentialMap
        self.deviceMap: OrderedDict[str, NetDevice] = OrderedDict()
        self.connectionMap: dict[str, Connection] = {}
        self.deviceQueue: list[dict[str, str]] = []
        # [ { "deviceID": "", "ip": "" } ]

    def crawl(self, initialHost: str, initialCreds: dict[str, str]):
        self.performScan(initialHost, None, initialCreds)
        c = 1

        while len(self.deviceQueue) > 0:
            d = self.deviceQueue.pop(0)
            self.performScan(d["ip"], d["deviceID"])
            c += 1

        print(f"{c} devices scanned")

    def performScan(
        self,
        host: str,
        deviceID: Union[str, None] = None,
        creds: Union[dict[str, str], None] = None
    ):
        credentials: dict[str, str] = {}
        if creds:
            credentials = creds
        else:
            # If the deviceID is not in the credentials map, use default credentials
            credentials = \
                self.defaultCredentials \
                if deviceID not in self.credentialMap \
                else self.credentialMap[deviceID]

        user = credentials['user']
        password = credentials['password']
        secret = credentials['secret']
        dev = NetDevice(ConnectionInfo(host, user, password, secret))
        dev.visited = True

        try:
            dev.connect()
        except:
            print(f"wrong crds {host}")
            return

        binfoModule = BasicInformation()

        if binfoModule.moduleSupported(dev):
            binfoModule.getInfo(dev)

        ifModule = InterfaceInformation()
        ifModule.getInfo(dev, self.deviceMap,
                         self.connectionMap, self.deviceQueue)

        bgpModule = BGPInformation()
        if bgpModule.moduleSupported(dev):
            bgpModule.getInfo(dev)

        hcModule = Healthcheck()
        hcModule.getInfo(dev)

        if dev.getDeviceID() not in self.deviceMap:
            self.deviceMap[dev.getDeviceID()] = dev
