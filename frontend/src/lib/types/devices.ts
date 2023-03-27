export type NetDevice = {
	hostname: string;
	domainName: string;
	visited: boolean;
	interfaces: DeviceInterface[];
	deviceHealth: DeviceHealth;
	routingInfo: { [key: string]: string | object };
};

export interface NetDevices {
	[key: string]: NetDevice;
}

export type DeviceInterface = {
	type: string;
	number: string;
	ip: string;
	neighbors: InterfaceNeighbor[];
	inputPacketLoss: number;
	outputPacketLoss: number;
	status: string;
	lineProtocol: string;
};

export type Connections = {
	[key: string]: {
		interfaces: string[];
		devices: string[];
	};
};

type InterfaceNeighbor = {
	ip: string;
	interface: string;
	deviceID: string;
};

type DeviceHealth = {
	cpuUsage: number;
	memoryUsed: number;
	freeMemory: number;
	latency: number;
};
