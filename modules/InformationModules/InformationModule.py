from modules.NetDevice import NetDevice


class InformationModule:
    def getInfo(self, netDevice: NetDevice):
        raise NotImplementedError("Start get info not implemented")

    def moduleSupported(self, netDevice: NetDevice) -> bool:
        return True
