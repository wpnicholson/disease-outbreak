<script lang="ts">
	import type { Report } from '$lib/backendtypes';
	import NewDisease from '$lib/components/NewDisease.svelte';
	const today = new Date().toISOString().split('T')[0];

	// Props come over from the sibling `+page.server.ts`.
	let { data } = $props();
	let token = data.token;
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
				disease: resDisease,
				disease_id: resDisease.id
			})
		});
		if (res.ok) {
			const updatedReport = await res.json();
			console.log('Report updated:', updatedReport);
			report = updatedReport;
		} else {
			console.error('Failed to update report');
			console.error(await res.text());
		}
	}

	function once<T extends Event>(fn: ((event: T) => void) | null): (event: T) => void {
		return function (this: unknown, event: T) {
			if (fn) fn.call(this, event);
			fn = null;
		};
	}
	function preventDefault<T extends Event>(fn: (event: T) => void): (event: T) => void {
		return function (this: unknown, event: T) {
			event.preventDefault();
			fn.call(this, event);
		};
	}
</script>

<div>
	<h1 class="mb-5 text-2xl font-semibold">New Report</h1>

	<button
		onclick={createNewReport}
		class="shadow-xs rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
	>
		Create New Report
	</button>

	{#if report}
		<form>
			<div class="mt-10 space-y-12">
				<div
					class="grid grid-cols-1 gap-x-8 gap-y-10 border-b border-gray-900/10 pb-12 md:grid-cols-3"
				>
					<NewDisease {token} {report} />
				</div>
			</div>
			<div class="mt-6 flex items-center justify-end gap-x-6">
				<button type="button" class="text-sm/6 font-semibold text-gray-900">Cancel</button>
				<button
					onclick={once(preventDefault(updateReportStatus))}
					class="shadow-xs rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
					>Finalise Report</button
				>
			</div>
		</form>
	{/if}
</div>
