<script>
	import { onMount } from "svelte";
    import axios from 'axios';
    import demoJSON from '../../demo.json'

    let devices = {}
    let connections = {}


    onMount(async () => {
        console.log("hello")
        devices = demoJSON.devices;
        connections = demoJSON.connections;
        // const res = await axios.get("localhost:8000");
        // console.log(res);
    })


</script>

<svelte:head>
    <title>Home</title>
    <meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
    <div class="main-container">
        hello world
    d
    </div>
</section>

<style>
    .main-container{ 
        background: white;
        width: 60vw;
        height: 95vh;
        border-radius: 10px;
    }
</style>
