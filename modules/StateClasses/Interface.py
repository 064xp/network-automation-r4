from __future__ import annotations
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from modules.InformationModules.InterfaceInformation import InterfaceNeighbor


class Interface:
    def __init__(self):
        self.type: str = ""
        self.number: str = ""
        self.ip: Union[str, None] = None
        self.neighbors: list[InterfaceNeighbor] = []
        self.inputPacketLoss: int = 0
        self.outputPacketLoss: int = 0
        self.status: str = ""
        self.lineProtocol: str = ""

    def getName(self) -> str:
        return self.type + self.number
