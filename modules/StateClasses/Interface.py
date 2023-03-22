from modules.NetDevice import NetDevice
from typing import Union


class Interface:
    type: str = ""
    number: str = ""
    ip: Union[str, None] = None
    neighborIP: Union[str, None] = None
    neighbor: Union[NetDevice, None] = None
    inputPacketLoss: int = 0
    outputPacketLoss: int = 0
    # MTU: int = 0
    # BW: int = 0
    # delay: int = 0
    status: str = ""
    lineProtocol: str = ""

    def getName(self) -> str:
        return self.type + self.number
