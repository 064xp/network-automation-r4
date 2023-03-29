<script lang="ts">
    import type { NetDevices, NetDevice } from '$lib/types/devices';

    import DeviceInfoPanel from '$lib/components/DeviceInfoPanel/DeviceInfoPanel.svelte';
    import TopologyView from '$lib/components/Topology/TopologyView.svelte';

    import { onMount } from 'svelte';
    import axios from 'axios';
    import demoJSON from '$lib/demo.json';

    let devices: NetDevices = {};
    let connections = {};
    let selectedDevice: NetDevice;

    onMount(async () => {
        const res = await axios.get('http://localhost:8000/demo');

        // @ts-ignore
        devices = res.data.devices as NetDevices;
        // @ts-ignore
        connections = res.data.connections as Connections;
        const keys = Object.keys(devices);
        if (keys.length > 0) selectedDevice = devices['R1.r1.com'];
    });
</script>

<svelte:head>
    <title>Home</title>
    <meta name="description" content="Svelte demo app" />
</svelte:head>

<section class="main-container">
    <DeviceInfoPanel device={selectedDevice} />
    <TopologyView {connections} {devices} />
</section>

<style>
    .main-container {
        display: flex;
        width: 100vw;
    }
</style>
