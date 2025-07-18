<script lang="ts">
	import type { Report } from '$lib/backendtypes';
	import { onMount } from 'svelte';
	import NewDisease from '$lib/components/NewDisease.svelte';
	import TableReports from '$lib/components/TableReports.svelte';
	const today = new Date().toISOString().split('T')[0];

	// Props come over from the sibling `routes/dashboard/+page.server.ts`.
	let { data } = $props();
	let token = data.token;
	let reports = $state<Report[] | null>(null);
	let report = $state<Report | null>(null);

	async function createNewReport() {
		const res = await fetch('/api/reports/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			},
			body: JSON.stringify(data.user)
		});
		if (res.ok) {
			report = await res.json();
			if (report) {
				report.disease = {
					id: 0, // New disease ID will be assigned by the backend.
					disease_name: '',
					disease_category: 'Bacterial', // Assumed default category.
					severity_level: 'Low', // Assumed default severity level.
					date_detected: today,
					symptoms: [],
					lab_results: '',
					treatment_status: 'None' // Assumed default treatment status.
				};
			}
			console.log('New report created:', report);
		} else {
			console.error('Failed to create new report');
			console.error(await res.text());
		}
	}

	async function updateReportStatus() {
		if (!report) {
			console.error('No report to update');
			return;
		}
		const res = await fetch(`/api/reports/${report.id}`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			},
			body: JSON.stringify({
				status: 'Draft'
			})
		});
		if (res.ok) {
			const updatedReport = await res.json();
			console.log('Report status updated:', updatedReport);
			report = updatedReport;
		} else {
			console.error('Failed to update report status');
			console.error(await res.text());
		}
	}

	// When the component mounts load the reports this user has created.
	async function loadReports() {
		const res = await fetch('/api/reports/', {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${token}`
			}
		});
		if (res.ok) {
			reports = await res.json();

			console.log('Dashboard reports loaded:', reports);
		} else {
			console.error('Dashboard failed to load reports');
		}
	}

	onMount(() => {
		loadReports();
	});

</script>

<div>
	<h1 class="mb-5 text-2xl font-semibold">Reports</h1>
	{#if Array.isArray(reports) && reports.length > 0}
		<TableReports {reports} />
	{:else}
		<p>No reports created yet.</p>
	{/if}
</div>
