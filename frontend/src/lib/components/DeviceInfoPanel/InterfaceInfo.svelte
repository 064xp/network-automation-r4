<script lang="ts">
    import type { DeviceInterface } from '$lib/types/devices';
    import { IndicatorStatus } from '$lib/components/StatusIndicatorBubble.svelte';

    import StatusIndicatorBubble from '$lib/components/StatusIndicatorBubble.svelte';
    import InformationElement from './InformationElement.svelte';
    import routerImg from '$lib/images/router.png';

    export let deviceInterface: DeviceInterface;

    let status: IndicatorStatus;

    const updateStatus = (intStatus: string, lineProto: string) => {
        if (intStatus === 'up' && lineProto === 'up') status = IndicatorStatus.Active;
        else if (intStatus === 'up' && lineProto !== 'up') status = IndicatorStatus.Idle;
        else status = IndicatorStatus.Inactive;
    };

    $: updateStatus(deviceInterface.status, deviceInterface.lineProtocol);
</script>

<div class="container">
    <div class="header">
        <StatusIndicatorBubble {status} size={10} />
        <h2>
            {deviceInterface.type}{deviceInterface.number}
        </h2>

        <div class="int-status">
            <span
                class="status-left"
                class:active={deviceInterface.status === 'up'}
                class:inactive={deviceInterface.status !== 'up'}>{deviceInterface.status}</span
            >
            <span
                class="lineProto-right"
                class:active={deviceInterface.status === 'up'}
                class:inactive={deviceInterface.status !== 'up'}
                >{deviceInterface.lineProtocol}</span
            >
        </div>
    </div>
    <div class="indent">
        <div class="section">
            <h3 class="subtitle">Basic Info</h3>

            <div class="indent">
                <InformationElement name="IP" content={deviceInterface.ip || ''} />
                <InformationElement
                    name="Input Packet Loss"
                    content={deviceInterface.inputPacketLoss}
                />
                <InformationElement
                    name="Ouput Packet Loss"
                    content={deviceInterface.outputPacketLoss}
                />
            </div>
        </div>
        {#if deviceInterface.neighbors.length > 0}
            <h3 class="subtitle">Neighbors</h3>
            <div class="neighbors indent">
                {#each deviceInterface.neighbors as neighbor}
                    <div class="neighbor-header">
                        <img src={routerImg} alt="Network device" />
                        <h4>{neighbor.deviceID}</h4>
                    </div>
                    <div class="neighbor-details indent">
                        <InformationElement name="IP" content={neighbor.ip} />
                        <InformationElement name="Int" content={neighbor.interface} />
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</div>

<style>
    .container {
        margin-bottom: 1em;
        padding-bottom: 1em;
        border-bottom: 2px solid #cacaca;
    }

    .header {
        display: flex;
        align-items: center;
    }

    .header h2 {
        margin: 0 0 0 0.5em;
        font-size: 1.4em;
    }

    .section {
        margin: 0 0 0.6em 0;
    }

    .int-status {
        display: flex;
        margin: 0 0 0 1em;
    }

    .int-status span {
        color: white;
        margin: 0;
        padding: 0.2em 0.4em;
        font-size: 0.8em;
    }

    .status-left {
        border-radius: 6px 0 0 6px;
    }

    .status-left.inactive {
        border-right: 2px solid #902e25;
    }

    .status-left.active {
        border-right: 2px solid #219552;
    }

    .lineProto-right {
        border-radius: 0 6px 6px 0;
    }

    .active {
        background-color: #2ecc71;
    }

    .inactive {
        background-color: #e74c3c;
    }

    .subtitle {
        margin: 0.3em 0 0.5em 0;
        border-bottom: 2px solid #34495e;
        display: inline-block;
    }

    .neighbor-header {
        display: flex;
        align-items: center;
    }

    .neighbor-header h4 {
        margin: 0.3em;
        font-weight: normal;
    }

    .indent {
        padding-left: 1.4em;
    }

    .neighbor-header img {
        margin: 0 0.4em 0 0;
        height: 1.1em;
        width: auto;
    }
</style>
