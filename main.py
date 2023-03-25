import jsonpickle
from typing import cast
from modules.NetDevice import NetDevice
from modules.ConnectionInfo import ConnectionInfo
from modules.InformationModules.BasicInformation import BasicInformation
from modules.InformationModules.InterfaceInformation import InterfaceInformation
from modules.InformationModules.Healthcheck import Healthcheck
from modules.InformationModules.BGPInformation import BGPInformation
from modules.StateClasses.Connection import Connection
import utils.numUtils as nu

deviceMap: dict[str, NetDevice] = {}
connectionMap: dict[str, Connection] = {}

host = "168.16.1.1"
user = "admin"
password = "admin"
secret = "cisco"
r1 = NetDevice(ConnectionInfo(host, user, password, secret))
r1.visited = True
r1.connect()

binfoModule = BasicInformation()
binfoModule.getInfo(r1)

ifModule = InterfaceInformation()
ifModule.getInfo(r1, deviceMap, connectionMap)

bgpModule = BGPInformation()
bgpModule.getInfo(r1)

# print("======================= Healthcheck =======================")

# hcModule = Healthcheck()
# hcModule.getInfo(r1)

# print(f"CPU Usage: {r1.deviceHealth.cpuUsage}%")
# print(f"Memory Usage: {r1.deviceHealth.getMemoryPercentage()}% \
#       ({round(nu.BtoMB(r1.deviceHealth.memoryUsed), 3)} MB / {round(nu.BtoMB(r1.deviceHealth.freeMemory), 3)}MB)")
# print(f"Avg latency: {r1.deviceHealth.latency}ms")


print(jsonpickle.encode(deviceMap, indent=4, unpicklable=False))
print(jsonpickle.encode(connectionMap, indent=4, unpicklable=False))
# print(connectionMap)
