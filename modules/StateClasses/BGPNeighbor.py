class BGPNeighbor:
    deviceID: str = ""
    ip: str = ""
    state: str = "Establish"
    prefixes: int = 0
    uptimeHours: int = 0
    uptimeMinutes: int = 0
    uptimeSeconds: int = 0
    autonomousSystem: int = 0

    def getUptime(self) -> str:
        return f"{self.uptimeHours:02}:{self.uptimeMinutes:02}:{self.uptimeSeconds:02}"
