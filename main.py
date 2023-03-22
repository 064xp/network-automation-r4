from modules.NetDevice import NetDevice
from modules.ConnectionInfo import ConnectionInfo
from modules.InformationModules.InterfaceInformation import InterfaceInformation


host = "168.16.1.1"
user = "admin"
password = "admin"
secret = "cisco"
r1 = NetDevice(ConnectionInfo(host, user, password, secret))
r1.connect()

ifModule = InterfaceInformation(r1)
result = ifModule.getInfo()

for i in result:
    print(f"Interface: {i.getName()}")
    print(f"  Status: {i.status}, line protocol: {i.lineProtocol}")
    if i.ip is not None:
        print(f"  IP: {i.ip}")
    if i.neighbor is not None:
        print(f"  Neighbor: {i.neighbor.getDeviceID()} -> {i.neighborIP}")
    print(f"  PacketLoss: I:{i.inputPacketLoss} O:{i.outputPacketLoss}")
    print("\n")
