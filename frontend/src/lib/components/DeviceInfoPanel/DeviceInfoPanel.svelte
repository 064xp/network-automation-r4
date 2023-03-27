<script lang="ts">
    import type { NetDevice } from '$lib/types/devices';
    import { IndicatorStatus } from '$lib/components/StatusIndicatorBubble.svelte';

    import StatusIndicatorBubble from '$lib/components/StatusIndicatorBubble.svelte';

    export let device: NetDevice;

    $: console.log(device);
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
        <div class="info-section">
            <h2 class="info-section_header">Interfaces</h2>

            <!-- Interfaces -->
            <div class="info-section_element">
                <p class="info-section_element-name">Thing</p>
                <p class="info-section_element-content">content</p>
            </div>
        </div>
        <p />
    {/if}
</div>

<style>
    .container {
        height: 100vh;
        width: 30vw;
        background-color: white;
        border-radius: 0 7px 7px 0;

        box-shadow: 10px 0px 15px -5px rgba(0, 0, 0, 0.55);
        -webkit-box-shadow: 10px 0px 15px -5px rgba(0, 0, 0, 0.55);
        -moz-box-shadow: 10px 0px 15px -5px rgba(0, 0, 0, 0.55);
        padding: 1em;
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

    .info-section {
        margin: 0 0 0.5em 0;
    }

    .domain-name {
        margin: 0.3em;
    }
    .info-section_header {
        background-color: #ecf0f1;
        text-align: center;
        font-size: 1.5em;
        padding: 0.2em;
        border-radius: 7px;
    }

    .info-section_element {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        width: 100%;
        font-size: 1.1em;
    }

    .info-section_element-name {
        font-weight: bold;
        margin: 0;
    }

    .info-section_element-content {
        margin: 0;
    }
</style>
