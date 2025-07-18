<script lang="ts">
	import type { Report } from '$lib/backendtypes';
	import NewDisease from '$lib/components/NewDisease.svelte';
	import NewPatient from '$lib/components/NewPatient.svelte';
	import Flyout from '$lib/components/Flyout.svelte';

	// We call this component from within a Svelte `{#if report && token}` block;
	// so we expect `report` and `token` to be defined.
	let { report, token }: { report: Report; token: string } = $props();

	console.log('Report component initialized with report:', report);
</script>

<div class="divide-y divide-gray-900/10">
	<div class="grid grid-cols-1 gap-x-8 gap-y-8 py-10 md:grid-cols-3">
		<div class="px-4 sm:px-0">
			<h2 class="text-base/7 font-semibold text-gray-900">Details (read only)</h2>
			<p class="mt-1 text-sm/6 text-gray-600">
				This is system automatically generated - and so is read only.
			</p>
		</div>

		<div class="shadow-xs bg-slate-100 ring-1 ring-gray-900/5 sm:rounded-xl md:col-span-2">
			<div class="px-4 py-6 sm:p-8">
				<div class="grid max-w-2xl grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
					<div class="sm:col-span-4">
						<span class="block text-sm/6 font-medium text-gray-900">Created</span>
						<input
							bind:value={report.created_at}
							readonly
							class="block min-w-0 grow py-1.5 pl-1 pr-3 text-base text-gray-900 sm:text-sm/6"
						/>
					</div>
					<div class="sm:col-span-4">
						<span class="block text-sm/6 font-medium text-gray-900">Status</span>
						<input
							bind:value={report.status}
							readonly
							class="block min-w-0 grow py-1.5 pl-1 pr-3 text-base text-gray-900 sm:text-sm/6"
						/>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Disease Information -->
	<div id="disease-info" class="grid grid-cols-1 gap-x-8 gap-y-8 py-10 md:grid-cols-3">
		<div class="px-4 sm:px-0">
			<h2 class="text-base/7 font-semibold text-gray-900">Disease Information</h2>
			<p class="mt-1 text-sm/6 text-gray-600">Add or update disease information for this report.</p>
		</div>

		<div class="shadow-xs bg-slate-100 ring-1 ring-gray-900/5 sm:rounded-xl md:col-span-2">
			<NewDisease {report} {token} />
		</div>
	</div>

	<!-- Patient Information -->
	<div id="patient-info" class="grid grid-cols-1 gap-x-8 gap-y-8 py-10 md:grid-cols-3">
		<div class="px-4 sm:px-0">
			<h2 class="text-base/7 font-semibold text-gray-900">Patient Information</h2>
			<p class="mt-1 text-sm/6 text-gray-600">Add or update patient information for this report.</p>
			<Flyout />
		</div>

		<div class="shadow-xs bg-slate-100 ring-1 ring-gray-900/5 sm:rounded-xl md:col-span-2">
			<NewPatient {report} {token} />
		</div>
	</div>
</div>
