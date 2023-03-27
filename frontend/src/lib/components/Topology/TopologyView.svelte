<script lang="ts">
    import type { NetDevices, Connections } from '$lib/types/devices';

    import { Svg, SVG } from '@svgdotjs/svg.js';
    import { onMount, afterUpdate } from 'svelte';
    import routerImg from '$lib/images/router.svg';

    export let devices: NetDevices;
    export let connections: Connections;

    let draw: Svg;

    onMount(async () => {
        // @ts-ignore
        draw = SVG().addTo('#topology-view').size('100%', '100%');
        renderTopology();
    });

    const renderTopology = () => {
        const cx = draw.node.clientWidth / 2;
        const cy = draw.node.clientHeight / 2;
        let r1 = draw.image(routerImg).center(cx, cy).size(70, 70);
        let r2 = draw
            .image(routerImg)
            .center(cx + 180, cy)
            .size(70, 70);

        let conn = draw
            .line(r1.cx(), r1.cy(), r2.cx(), r2.cy())
            .stroke({ width: 2, color: 'black' })
            .insertBefore(r1);
    };
</script>

<div class="container" id="topology-view" />

<style>
    .container {
        background-color: rgb(190, 205, 218);
        height: 100vh;
        width: 100%;
    }
</style>
