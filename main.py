from modules.NetDevice import NetDevice
from modules.ConnectionInfo import ConnectionInfo
from modules.InformationModules.InterfaceInformation import InterfaceInformation
from modules.InformationModules.Healthcheck import Healthcheck
import utils.numUtils as nu


host = "168.16.1.1"
user = "admin"
password = "admin"
secret = "cisco"
r1 = NetDevice(ConnectionInfo(host, user, password, secret))
r1.connect()

ifModule = InterfaceInformation()
ifModule.getInfo(r1)

for i in r1.interfaces:
    print(f"Interface: {i.getName()}")
    print(f"  Status: {i.status}, line protocol: {i.lineProtocol}")
    if i.ip is not None:
        print(f"  IP: {i.ip}")
    if i.neighbor is not None:
        print(f"  Neighbor: {i.neighbor.getDeviceID()} -> {i.neighborIP}")
    print(f"  PacketLoss: I:{i.inputPacketLoss} O:{i.outputPacketLoss}")
    print("\n")


print("======================= Healthcheck =======================")

hcModule = Healthcheck()
hcModule.getInfo(r1)

print(f"CPU Usage: {r1.deviceHealth.cpuUsage}%")
print(f"Memory Usage: {r1.deviceHealth.getMemoryPercentage()}%\t({nu.BtoMB(r1.deviceHealth.memoryUsed)} MB / {nu.BtoMB(r1.deviceHealth.freeMemory)} MB)")
print(f"Avg latency: {r1.deviceHealth.latency}ms")
