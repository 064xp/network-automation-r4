<script context="module" lang="ts">
    export enum IndicatorStatus {
        Active,
        Inactive,
        Idle
    }
</script>

<script lang="ts">
    export let style: string = '';
    export let status: IndicatorStatus = IndicatorStatus.Active;
    export let size: number = 20;
</script>

<div
    class="indicator"
    class:active={status === IndicatorStatus.Active}
    class:inactive={status === IndicatorStatus.Inactive}
    class:idle={status === IndicatorStatus.Idle}
    style="height: {size}px; width: {size}px; {style}"
/>

<style>
    .indicator {
        border-radius: 99px;
    }

    .active {
        background-color: #2ecc71;
    }

    .inactive {
        background-color: #e74c3c;
    }

    .idle {
        background-color: #f1c40f;
    }
</style>
