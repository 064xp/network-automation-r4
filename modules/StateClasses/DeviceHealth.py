class DeviceHealth:
    def __init__(self):
        self.cpuUsage: int
        self.memoryUsed: int
        self.freeMemory: int
        self.latency: float

    def getMemoryPercentage(self) -> int:
        totalMemory = self.freeMemory + self.memoryUsed
        return round(self.memoryUsed * 100 / totalMemory)
