<script lang="ts">
    import type { DeviceInterface } from '$lib/types/devices';
    import { IndicatorStatus } from '$lib/components/StatusIndicatorBubble.svelte';

    import './infoSection.css';

    import StatusIndicatorBubble from '$lib/components/StatusIndicatorBubble.svelte';
    import Router from '$lib/images/router.png';

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
        {#if deviceInterface.neighbors.length > 0}
            <h3 class="neighbors-title">Neighbors</h3>
            <div class="neighbors indent">
                {#each deviceInterface.neighbors as neighbor}
                    <div class="neighbor-header">
                        <img src={Router} alt="Network device" />
                        <h4>{neighbor.deviceID}</h4>
                    </div>
                    <div class="neighbor-details indent">
                        <div class="info-section_element">
                            <p class="info-section_element-name">IP</p>
                            <p class="info-section_element-content">{neighbor.ip}</p>
                        </div>
                        <div class="info-section_element">
                            <p class="info-section_element-name">Int</p>
                            <p class="info-section_element-content">{neighbor.interface}</p>
                        </div>
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

    .neighbors-title {
        margin: 0.5em;
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
