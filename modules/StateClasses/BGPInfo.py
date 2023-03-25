from ..StateClasses.RoutingInfo import RoutingInfo
from ..StateClasses.BGPNeighbor import BGPNeighbor


class BGPInfo(RoutingInfo):

    def __init__(
        self,
        name: str,
        neighbors: list[BGPNeighbor],
        autonomousSystem: int
    ):
        self.name = name
        self.neighbors = neighbors
        self.autonomousSystem = autonomousSystem
