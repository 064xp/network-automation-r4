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
        console.log('hello');
        // @ts-ignore
        devices = demoJSON.devices as NetDevices;
        connections = demoJSON.connections;
        const keys = Object.keys(devices);
        if (keys.length > 0) selectedDevice = devices['R1.r1.com'];
        // const res = await axios.get("localhost:8000");
        // console.log(res);
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
