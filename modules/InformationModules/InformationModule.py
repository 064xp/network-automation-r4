from modules.NetDevice import NetDevice


class InformationModule:
    netDevice: NetDevice

    def __init__(self, netDevice: NetDevice):
        self.netDevice = netDevice

    def getInfo(self):
        raise NotImplementedError("Start get info not implemented")

    def moduleSupported(self) -> bool:
        return True
