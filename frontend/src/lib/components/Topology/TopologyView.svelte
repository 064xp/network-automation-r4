<script lang="ts">
    import type { NetDevices, Connections } from '$lib/types/devices';

    import { Shape, Svg, SVG } from '@svgdotjs/svg.js';
    import { onMount, afterUpdate, tick } from 'svelte';
    import routerImg from '$lib/images/router.svg';
    import switchImg from '$lib/images/l2-switch.svg';
    import Page from '../../../routes/+page.svelte';

    export let devices: NetDevices;
    export let connections: Connections;

    let renderedDevices: { [key: string]: Shape } = {};

    let draw: Svg;

    onMount(async () => {
        // @ts-ignore
        draw = SVG().addTo('#topology-view').size('100%', '100%');
    });

    const renderDevice = (
        x: number,
        y: number,
        deviceID: string,
        size: number,
        parent?: Shape
    ): Shape[] => {
        // Draw device
        const newDev = draw.image(routerImg).center(x, y).size(size, size);
        const text = draw.text(deviceID).center(x + size / 2, y + size + 5);
        renderedDevices[deviceID] = newDev;
        return [newDev, text];
    };

    $: renderTopology(devices, connections);

    // let conn = draw
    //     .line(r1.cx(), r1.cy(), r2.cx(), r2.cy())
    //     .stroke({ width: 2, color: 'black' })
    //     .insertBefore(r1);

    const renderTopology = (devices: NetDevices, connections: Connections) => {
        if (
            Object.keys(devices).length === 0 ||
            Object.keys(connections).length === 0 ||
            draw === undefined
        )
            return;
        const device = devices['R1.r1.com'];
        const radius = 300;
        const iconSize = 60;

        const cx = draw.node.clientWidth / 2;
        const cy = draw.node.clientHeight / 2;

        let [d, dText] = renderDevice(cx, cy, `${device.hostname}.${device.domainName}`, iconSize);

        const interfacesWithNeighbors = device.interfaces.filter((i) => i.neighbors.length > 0);
        const angle = 360 / interfacesWithNeighbors.length;

        let currentAngle = 0;

        interfacesWithNeighbors.forEach((int) => {
            if (int.neighbors.length == 0) return;

            if (int.neighbors.length > 1) {
                /// render multiple
                return;
            }

            let angleRad = currentAngle * (Math.PI / 180);

            const x = (d.x() as number) + radius * Math.cos(angleRad);
            const y = (d.y() as number) + radius * Math.sin(angleRad);

            renderDevice(x, y, int.neighbors[0].deviceID, iconSize);
            currentAngle += angle;
        });

        renderConnections();
    };

    const renderConnections = () => {
        Object.values(connections).forEach((conn) => {
            const d1 = renderedDevices[conn.devices[0]];
            const d2 = renderedDevices[conn.devices[1]];

            // Draw line

            let color = '';

            if (conn.interfaces[0].startsWith('Serial')) color = '#e74c3c';
            else color = '#2c3e50';

            draw.line(d1.cx(), d1.cy(), d2.cx(), d2.cy())
                .stroke({ width: 2, color })
                .insertBefore(d1);

            drawInterfaceLabel(d1, d2, conn.interfaces[0]);
            drawInterfaceLabel(d2, d1, conn.interfaces[1]);
        });
    };

    const drawInterfaceLabel = (d1: Shape, d2: Shape, text: string) => {
        const labelDistance = 80;

        let vec = { x: d2.cx() - d1.cx(), y: d2.cy() - d1.cy() };
        let magnitude = Math.sqrt(vec.x * vec.x + vec.y * vec.y);
        vec.x /= magnitude;
        vec.y /= magnitude;

        let x = (d1.cx() as number) + vec.x * labelDistance;
        let y = (d1.cy() as number) + vec.y * labelDistance;
        console.log('coords', vec, x, y);

        let labelText = draw.text(text).center(x, y).fill('white');

        const padding = 7;
        let labelRect = draw
            .rect(labelText.bbox().width + padding, labelText.bbox().height + padding)
            .attr({
                rx: 3,
                ry: 3,
                fill: '#34495e'
            })
            .center(labelText.cx(), labelText.cy())
            .insertBefore(labelText);
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
