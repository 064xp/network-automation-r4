from typing import cast, Union
from .InformationModule import InformationModule
from ..StateClasses.Interface import Interface
from ..NetDevice import NetDevice
import re


class InterfaceInformation(InformationModule):
    interfaces: list[Interface] = []

    def __separateInterfaceInfo(self, cmdOutput: str) -> list[str]:
        pattern = r'^(?:.+)\n\s+(?:.+(?:\n\s+.+\n*)*)$'
        matches = re.findall(pattern, cmdOutput, re.MULTILINE)

        return matches

    def __getBasicInfo(self, interfaceInfo: str) -> Union[dict[str, str], None]:
        pattern = r'([A-Za-z]+)([\d\/]+) is ([\w ]+), line protocol is (\w+)'
        m = re.search(pattern, interfaceInfo)
        if m is None:
            return None

        return {
            "type": m.group(1),
            "number": m.group(2),
            "status": m.group(3),
            "lineProtocol": m.group(4)
        }

    def __getIP(self, interfaceInfo: str) -> Union[str, None]:
        pattern = r'Internet address is ([\d\.]+)'
        m = re.search(pattern, interfaceInfo)

        if m is None:
            return None

        return m.group(1)

    def __getNeighbor(self, neighborOutput: str, intType: str, intNum: str) -> Union[None, tuple[NetDevice, str]]:
        neighborsSplit = neighborOutput.split("-------------------------")
        neighborInfo = None
        interfaceName = intType + intNum

        for n in neighborsSplit:
            if f"Interface: {interfaceName}" in n:
                neighborInfo = n
                break

        if neighborInfo is None:
            return None
        # Get neighbor info

        # Patterns
        devIdPattern = r'Device ID: ([\w\.]+)'
        ipPattern = r'IP address: ([\d\.]+)'

        # Variables
        deviceId = ""
        hostname = ""
        domain = ""
        ip = ""

        devIdSearch = re.search(devIdPattern, neighborInfo)
        if devIdSearch is not None:
            deviceId = devIdSearch.group(1)
            split = deviceId.split('.')
            hostname = split[0]
            domain = ".".join(split[1:])

        ipSearch = re.search(ipPattern, neighborInfo)
        if ipSearch is not None:
            ip = ipSearch.group(1)

        neighborDevice = NetDevice()
        neighborDevice.domainName = domain
        neighborDevice.hostname = hostname

        return neighborDevice, ip

    def __getPacketLoss(self, intInfo: str) -> tuple[int, int]:
        pattern = r'Input queue: \d+\/\d+\/(\d+)\/\d+.*Total output drops: (\d+)'
        m = re.search(pattern, intInfo)

        if m is None:
            return 0, 0

        return int(m.group(1)), int(m.group(2))

    def getInfo(self, netDevice: NetDevice) -> dict[str, NetDevice]:
        interfaces: list[Interface] = []
        netDevice.conn.enable()
        result = netDevice.conn.send_command("show interfaces")
        intInfo = self.__separateInterfaceInfo(cast(str, result))
        cdpNeighbors = netDevice.conn.send_command(
            "show cdp neighbors detail")

        neighbors: dict[str, NetDevice] = {}

        for i in intInfo:
            interface = Interface()

            # Get name, status & line protocol
            basicInfo = self.__getBasicInfo(i)

            if basicInfo is None:
                continue

            interface.type = basicInfo["type"]
            interface.number = basicInfo["number"]
            interface.status = basicInfo["status"]
            interface.lineProtocol = basicInfo["lineProtocol"]

            # Get IP
            if basicInfo["status"] == "up":
                interface.ip = self.__getIP(i)

            # Get Neighbor
            if basicInfo["lineProtocol"] == "up":
                nres = self.__getNeighbor(
                    cast(str, cdpNeighbors),
                    basicInfo["type"],
                    basicInfo["number"],
                )

                if nres is not None:
                    neighbor, neighborIP = nres
                    interface.neighbor = neighbor
                    interface.neighborIP = neighborIP
                    neighbors[neighbor.getDeviceID()] = neighbor

            inputPacketLoss, outputPacketLoss = self.__getPacketLoss(i)
            interface.inputPacketLoss = inputPacketLoss
            interface.outputPacketLoss = outputPacketLoss

            interfaces.append(interface)

        netDevice.interfaces = interfaces

        return neighbors
