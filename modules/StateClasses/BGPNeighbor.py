from .RoutingNeighbor import RoutingNeighbor


class BGPNeighbor(RoutingNeighbor):
    def __init__(self):
        self.deviceID: str = ""
        self.ip: str = ""
        self.state: str = "Establish"
        self.prefixes: int = 0
        self.uptimeHours: int = 0
        self.uptimeMinutes: int = 0
        self.uptimeSeconds: int = 0
        self.autonomousSystem: int = 0

    def getUptime(self) -> str:
        return f"{self.uptimeHours:02}:{self.uptimeMinutes:02}:{self.uptimeSeconds:02}"
