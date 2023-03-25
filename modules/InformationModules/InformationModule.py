from abc import abstractmethod
from modules.NetDevice import NetDevice


class InformationModule:
    def getInfo(self, netDevice: NetDevice):
        raise NotImplementedError("Start get info not implemented")

    @abstractmethod
    def moduleSupported(self, netDevice: NetDevice) -> bool:
        return True
