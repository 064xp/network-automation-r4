<script lang="ts">
    import InformationElement from '../InformationElement.svelte';
    import StatusIndicatorBubble from '$lib/components/StatusIndicatorBubble.svelte';
    import { IndicatorStatus } from '$lib/components/StatusIndicatorBubble.svelte';

    type BGPNeighbor = {
        deviceID: string;
        ip: string;
        state: string;
        prefixes: number;
        uptimeHours: number;
        uptimeMinutes: number;
        uptimeSeconds: number;
        autonomousSystem: number;
    };

    type BGPRoutingInfo = {
        name: string;
        autonomousSystem: number;
        neighbors: BGPNeighbor[];
    };

    export let routingInfo: BGPRoutingInfo;

    const getUptime = (uptimeHours: number, uptimeMinutes: number, uptimeSeconds: number) => {
        return `${String(uptimeHours).padStart(2)}h ${String(uptimeMinutes).padStart(2)}m ${String(
            uptimeSeconds
        ).padStart(2)}s`;
    };

    const getStatus = (neighbor: BGPNeighbor): IndicatorStatus => {
        if (neighbor.state === 'Establish') return IndicatorStatus.Active;
        else if (neighbor.state === 'Active') return IndicatorStatus.Idle;
        else return IndicatorStatus.Inactive;
    };
</script>

<InformationElement name="Protocol" content={routingInfo.name} />
<InformationElement name="Autonomous System" content={routingInfo.autonomousSystem} />

{#if routingInfo.neighbors.length > 0}
    <InformationElement name="Neighbors" content="" />
    {#each routingInfo.neighbors as n}
        <div class="indent neighbor-section">
            <div class="neighbor-header">
                <StatusIndicatorBubble
                    status={getStatus(n)}
                    size={15}
                    style="margin-right: .8em;"
                />
                <InformationElement name="Host" content={n.ip} />
            </div>
            <div class="indent-double">
                <InformationElement name="State" content={n.state} />
                <InformationElement name="Prefixes" content={n.prefixes} />
                <InformationElement
                    name="Uptime"
                    content={getUptime(n.uptimeHours, n.uptimeMinutes, n.uptimeSeconds)}
                />
                <InformationElement name="Autonomous System" content={n.autonomousSystem} />
            </div>
        </div>
    {/each}
{/if}

<style>
    .neighbor-section {
        border-bottom: 2px solid #cacaca;
        margin-bottom: 1em;
    }

    .neighbor-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
