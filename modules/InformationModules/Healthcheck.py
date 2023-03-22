import subprocess
from typing import cast
import re

from ..StateClasses.DeviceHealth import DeviceHealth
from ..NetDevice import NetDevice
from .InformationModule import InformationModule


class Healthcheck(InformationModule):
    def getInfo(self, netDevice: NetDevice):
        netDevice.conn.enable()
        cpuOutput = netDevice.conn.send_command("show processes cpu")
        memoryOutput = netDevice.conn.send_command("show memory")
        devHealth = DeviceHealth()

        cpuUsage = self.__getCPUPercentage(cast(str, cpuOutput))
        usedMemory, freeMemory = self.__getMemoryUsage(cast(str, memoryOutput))
        avgPing = self.latencyTest(netDevice.connectionInfo.host)

        devHealth.cpuUsage = cpuUsage
        devHealth.memoryUsed = usedMemory
        devHealth.freeMemory = freeMemory
        devHealth.latency = avgPing

        netDevice.deviceHealth = devHealth

    def __getCPUPercentage(self, cpuOutput: str) -> int:
        cpuPattern = r'one minute: (\d+)%'

        res = re.search(cpuPattern, cpuOutput)

        if res is None:
            return 0

        return int(res.group(1))

    def __getMemoryUsage(self, memoryOutput: str) -> tuple[int, int]:
        '''
        Regresa: usedMemory, freeMemory in bytes
        '''
        memoryPattern = r'Processor\ +\w+\ +\w+\ +(\w+)\ +(\w+)'

        res = re.search(memoryPattern, memoryOutput)

        if res is None:
            return 0, 0

        return int(res.group(1)), int(res.group(2))

    def latencyTest(self, host: str) -> float:
        '''
            Pings host, returns average latency
        '''
        ping_process = subprocess.Popen(
            ["ping", "-c", "4", host], stdout=subprocess.PIPE)

        output, error = ping_process.communicate()
        output = output.decode('utf-8')

        if ping_process.returncode == 0:
            avgPingPattern = r'rtt [\w\/]* = [\d\.]+\/([\d\.]+)'
            res = re.search(avgPingPattern, output)
            if res is None:
                return -1

            return float(res.group(1))

        return -1
