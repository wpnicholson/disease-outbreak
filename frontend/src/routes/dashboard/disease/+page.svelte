<script lang="ts">
	import type { Report } from '$lib/backendtypes';
	import NewDisease from '$lib/components/NewDisease.svelte';
	const today = new Date().toISOString().split('T')[0];

	let data = $props();
    console.log('Data received in disease page:', data);
	let token = $state(data.token);
	let report = $state<Report | null>(data.report || null);
</script>

{#if report}
	<NewDisease {token} {report} />
{/if}
