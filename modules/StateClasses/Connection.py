class Connection:

    def __init__(self):
        self. interfaces: list[str] = []
        self.devices: list[str] = []

    def addDevice(self, deviceID: str, interface: str):
        self.interfaces.append(interface)
        self.devices.append(deviceID)
        self.__sortInterfaces()

    def __sortInterfaces(self):
        if len(self.interfaces) == 1:
            return

        if self.devices[0] > self.devices[1]:
            tmpDev = self.devices[0]
            tmpInt = self.devices[1]
            self.devices[0] = self.devices[1]
            self.interfaces[0] = self.interfaces[1]
            self.devices[1] = tmpDev
            self.interfaces[1] = tmpInt

    def getID(self):
        return self.devices[0] + \
            self.interfaces[0] + \
            self.devices[1] + \
            self.interfaces[1]
