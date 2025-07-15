<script lang="ts">
    import Header from '$lib/components/Header.svelte';

    let { children } = $props();
</script>

<Header />

<main class="flex-1 p-4 w-full max-w-7xl mx-auto">
	{@render children()}
</main>
