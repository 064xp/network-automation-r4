import json
from typing import cast, Union
from .InformationModule import InformationModule
from ..StateClasses.Interface import Interface
from ..NetDevice import NetDevice
from modules.StateClasses.Connection import Connection
import re


class InterfaceNeighbor:
    ip: str
    interface: str
    deviceID: str

    def __init__(self, ip: str, interface: str, deviceID: str):
        self.ip = ip
        self.interface = interface
        self.deviceID = deviceID


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

    def __getNeighbors(
            self,
            netDevice: NetDevice,
            neighborOutput: str,
            intType: str,
            intNum: str,
            deviceMap: dict[str, NetDevice],
            connectionMap: dict[str, Connection]
    ) -> list[InterfaceNeighbor]:
        # Patterns
        devIdPattern = r'Device ID: ([\w\.]+)'
        ipPattern = r'IP address: ([\d\.]+)'
        portIDPattern = r'Port ID \(outgoing port\): ([\w\/]+)'
        neighborsSplit = neighborOutput.split("-------------------------")
        neighborInfo = None
        interfaceName = intType + intNum
        neighbors: list[InterfaceNeighbor] = []

        for n in neighborsSplit:
            if f"Interface: {interfaceName}" not in n:
                continue

            neighborInfo = n

            # Variables
            deviceId = ""
            hostname = ""
            domain = ""
            ip = ""
            portID = ""

            devIdSearch = re.search(devIdPattern, neighborInfo)
            if devIdSearch is not None:
                deviceId = devIdSearch.group(1)
                split = deviceId.split('.')
                hostname = split[0]
                domain = ".".join(split[1:])

            ipSearch = re.search(ipPattern, neighborInfo)
            if ipSearch is not None:
                ip = ipSearch.group(1)

            portIDSearch = re.search(portIDPattern, neighborInfo)
            if portIDSearch is not None:
                portID = portIDSearch.group(1)

            # make NetDevice of neighbor
            neighborDevice = NetDevice()
            neighborDevice.domainName = domain
            neighborDevice.hostname = hostname

            if neighborDevice.getDeviceID() not in deviceMap:
                # Add to deviceMap, key is its deviceID
                deviceMap[neighborDevice.getDeviceID()] = neighborDevice

            # Create interface neighbor
            intNeighbor = InterfaceNeighbor(ip, portID, deviceId)
            neighbors.append(intNeighbor)

            # Make connection
            conn = Connection()
            conn.addDevice(netDevice.getDeviceID(), interfaceName)
            conn.addDevice(neighborDevice.getDeviceID(), portID)
            print(conn.devices)
            print(conn.interfaces)

            if conn.getID() not in connectionMap:
                connectionMap[conn.getID()] = conn

        return neighbors

    def __getPacketLoss(self, intInfo: str) -> tuple[int, int]:
        pattern = r'Input queue: \d+\/\d+\/(\d+)\/\d+.*Total output drops: (\d+)'
        m = re.search(pattern, intInfo)

        if m is None:
            return 0, 0

        return int(m.group(1)), int(m.group(2))

    def getInfo(
            self,
            netDevice: NetDevice,
            deviceMap: dict[str, NetDevice],
            connectionMap: dict[str, Connection]
    ):
        interfaces: list[Interface] = []
        netDevice.conn.enable()
        result = netDevice.conn.send_command("show interfaces")
        intInfo = self.__separateInterfaceInfo(cast(str, result))
        cdpNeighbors = netDevice.conn.send_command(
            "show cdp neighbors detail")

        neighbors: list[InterfaceNeighbor]

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

            # Get Neighbors
            if basicInfo["lineProtocol"] == "up":
                neighbors = self.__getNeighbors(
                    netDevice,
                    cast(str, cdpNeighbors),
                    basicInfo["type"],
                    basicInfo["number"],
                    deviceMap,
                    connectionMap
                )

                interface.neighbors = neighbors

            inputPacketLoss, outputPacketLoss = self.__getPacketLoss(i)
            interface.inputPacketLoss = inputPacketLoss
            interface.outputPacketLoss = outputPacketLoss

            interfaces.append(interface)

        # update device
        netDevice.interfaces = interfaces
        # Add to device map if not in already
        if netDevice.getDeviceID() not in deviceMap:
            deviceMap[netDevice.getDeviceID()] = netDevice
