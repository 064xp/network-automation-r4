class DeviceHealth:
    cpuUsage: int
    memoryUsed: int
    freeMemory: int
    latency: float

    def getMemoryPercentage(self) -> int:
        totalMemory = self.freeMemory + self.memoryUsed
        return round(self.memoryUsed * 100 / totalMemory)
