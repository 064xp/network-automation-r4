<script lang="ts">
    import type { NetDevice } from '$lib/types/devices';
    import { IndicatorStatus } from '$lib/components/StatusIndicatorBubble.svelte';

    import StatusIndicatorBubble from '$lib/components/StatusIndicatorBubble.svelte';
    import InterfaceInfo from '$lib/components/DeviceInfoPanel/InterfaceInfo.svelte';
    import InformationElement from './InformationElement.svelte';
    import BGPInfo from './RoutingInfo/BGPInfo.svelte';

    export let device: NetDevice;

    $: console.log(device);

    const getPercentage = (total: number, ammount: number): number => (ammount * 100) / total;
</script>

<div class="container">
    {#if device !== undefined}
        <div class="device-header">
            <h1>
                {device.hostname}
            </h1>

            <StatusIndicatorBubble status={IndicatorStatus.Active} />
        </div>
        <p class="domain-name">
            {device.domainName}
        </p>
        {#if device.visited}
            <div class="info-section">
                <!-- Device Health -->
                <h2 class="info-section_header">Device Health</h2>
                <InformationElement name="CPU Usage" content={`${device.deviceHealth.cpuUsage}%`} />
                <InformationElement
                    name="Memory Usge"
                    content={`${getPercentage(
                        device.deviceHealth.freeMemory + device.deviceHealth.memoryUsed,
                        device.deviceHealth.memoryUsed
                    ).toFixed(2)}%`}
                />
                <InformationElement name="Latency" content={`${device.deviceHealth.latency} ms`} />

                {#if device.routingInfo}
                    <!-- Routing Info -->
                    <h2 class="info-section_header">Routing</h2>
                    <BGPInfo routingInfo={device.routingInfo} />
                {/if}

                <!-- Interfaces -->
                <h2 class="info-section_header">Interfaces</h2>
                {#each device.interfaces as int}
                    <InterfaceInfo deviceInterface={int} />
                {/each}
            </div>
        {/if}
        <p />
    {/if}
</div>

<style>
    .container {
        height: 100vh;
        box-sizing: border-box;
        width: 35vw;
        background-color: white;
        border-radius: 0 7px 7px 0;

        box-shadow: 10px 0px 15px -5px rgba(0, 0, 0, 0.55);
        -webkit-box-shadow: 10px 0px 15px -5px rgba(0, 0, 0, 0.55);
        -moz-box-shadow: 10px 0px 15px -5px rgba(0, 0, 0, 0.55);
        padding: 1em;

        overflow: scroll;
    }

    .device-header {
        display: flex;
        justify-self: flex-start;
        align-items: center;
        border-bottom: 1px solid #95a5a6;
    }

    .device-header h1 {
        margin: 0 0.5em 0 0;
    }

    .domain-name {
        margin: 0.3em;
    }

    .info-section {
        margin: 0 0 0.5em 0;
    }

    .info-section_header {
        background-color: #ecf0f1;
        text-align: center;
        font-size: 1.5em;
        padding: 0.2em;
        border-radius: 7px;
    }
</style>
