<script lang="ts">
    import type {NetDevices, Connections} from '$lib/types/devices';

    export let devices: NetDevices;
    export let connections: Connections;
</script>

<div class="container">
    topologyView
</div>

<style>
    .container {
        background-color: rgb(190, 205, 218);
        height: 100vh;
        width: 100%;
    }
</style>