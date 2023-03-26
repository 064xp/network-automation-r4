from typing import cast
import re

from .InformationModule import InformationModule
from ..NetDevice import NetDevice
from ..StateClasses.BGPNeighbor import BGPNeighbor
from ..StateClasses.BGPInfo import BGPInfo


class BGPInformation(InformationModule):
    def getInfo(self, netDevice: NetDevice):
        netDevice.conn.enable()
        bgpSummary = netDevice.conn.send_command("show ip bgp summary")
        bgpSummary = cast(str, bgpSummary)

        AS = self.__getAS(bgpSummary)
        neighbors = self.__getNeighbors(bgpSummary)

        netDevice.routingInfo = BGPInfo("BGP", neighbors, AS)

    def __getNeighbors(self, bgpSummary: str) -> list[BGPNeighbor]:
        bgpNeighbors: list[BGPNeighbor] = []

        lines = bgpSummary.split('\n')

        neighborLinesStart = False
        for line in lines:
            if neighborLinesStart:
                bgpNeighbors.append(self.__getNeighbor(line))
                continue

            if line.startswith("Neighbor"):
                neighborLinesStart = True
                continue

        return bgpNeighbors

    def __getNeighbor(self, neighborData: str) -> BGPNeighbor:
        pattern = r'[\w\.\:]+'

        res = re.findall(pattern, neighborData)

        if len(res) == 0:
            return BGPNeighbor()

        ip = res[0]
        AS = int(res[2])
        uptime = res[8]
        statePref = res[9]

        uptimeHours = 0
        uptimeMinutes = 0
        uptimeSeconds = 0

        if any(chr.isdigit() for chr in uptime):
            uptimeSplit = uptime.split(':')
            uptimeHours = int(uptimeSplit[0])
            uptimeMinutes = int(uptimeSplit[1])
            uptimeSeconds = int(uptimeSplit[2])

        state: str = "Establish"
        prefixes: int = 0

        if statePref.isalpha():
            state = statePref
        else:
            prefixes = int(statePref)

        neighbor = BGPNeighbor()

        neighbor.ip = ip
        neighbor.state = state
        neighbor.prefixes = prefixes
        neighbor.uptimeHours = uptimeHours
        neighbor.uptimeMinutes = uptimeMinutes
        neighbor.uptimeSeconds = uptimeSeconds
        neighbor.autonomousSystem = AS

        return neighbor

    def __getAS(self, bgpSummary: str) -> int:
        pattern = r'local AS number (\d+)'
        res = re.search(pattern, bgpSummary)

        if res is None:
            return -1

        return int(res.group(1))

    def moduleSupported(self, netDevice: NetDevice) -> bool:
        netDevice.conn.enable()
        output = netDevice.conn.send_command("show ip protocols")
        if "bgp" in output:
            return True

        return False
