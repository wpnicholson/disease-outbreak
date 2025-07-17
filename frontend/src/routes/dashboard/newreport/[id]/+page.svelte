<script lang="ts">
    import type { Report } from '$lib/backendtypes';
    import ReportDisplay from '$lib/components/ReportDisplay.svelte';
    // Props come over from the sibling `+page.server.ts`.
    let { data } = $props();
    let id = data.id;
    let report: Report | null = data.report;
    let token = data.token;
    console.log('Data received in NewReport page:', data);

</script>
<h1 class="text-lg font-semibold text-gray-900">Edit Report Id {id}</h1>

{#if report}
    <ReportDisplay {report} {token}/>
{:else}
    <p>Loading report {id}...</p>
{/if}
