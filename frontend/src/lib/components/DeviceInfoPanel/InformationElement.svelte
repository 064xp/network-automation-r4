<script lang="ts">
    export let name: string;
    export let content: string | number;
</script>

<div class="container">
    <p class="name">{name}</p>
    <p class="content">{content}</p>
</div>

<style>
    .container {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        width: 100%;
        font-size: 1.1em;
    }

    .name {
        font-weight: bold;
        margin: 0;
    }

    .content {
        margin: 0;
    }
</style>
