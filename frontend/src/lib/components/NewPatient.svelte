<script lang="ts">
	import { onMount } from 'svelte';
	import type { Report, Patient } from '$lib/backendtypes';
	import { once, preventDefault } from '$lib/utils/preventdefault';
	import PatientListing from '$lib/components/PatientListing.svelte';
	const today = new Date().toISOString().split('T')[0];
	let patients: Patient[] = $state([]);

	// We call this component from within a Svelte `{#if report && token}` block;
	// so we expect `report` and `token` to be defined.
	let { report, token }: { report: Report; token: string } = $props();

	async function getPatientsThisReport() {
		const res = await fetch(`/api/reports/${report.id}/patient`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			}
		});
		if (res.ok) {
			const data = await res.json();
			console.log('Patients for this report:', data);
			return data;
		} else {
			console.error('Failed to fetch patients for this report');
			console.error(await res.text());
			return [];
		}
	}

	onMount(async () => {
		if (report && token) {
			patients = await getPatientsThisReport();
		}
	});
</script>

{#if report?.disease}
	<div class="shadow-xs bg-white ring-1 ring-gray-900/5 sm:rounded-xl md:col-span-2">
		{#if patients.length > 0}
			<PatientListing {patients} />
		{:else}
			<p
				class="px-4 py-6 text-sm/6 text-gray-600
				sm:p-8"
			>
				No patients associated with this report yet. Add a new patient below.
			</p>
		{/if}

		<!-- Save button -->
		<div
			class="flex items-center justify-end gap-x-6 border-t border-gray-900/10 px-4 py-4 sm:px-8"
		>
			<button
				type="submit"
				onclick={once(preventDefault(updatePatients))}
				class="shadow-xs rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
				>Save</button
			>
		</div>
	</div>
{/if}
