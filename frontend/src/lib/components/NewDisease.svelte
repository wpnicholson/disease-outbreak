<script lang="ts">
	import type { Report } from '$lib/backendtypes';
	const today = new Date().toISOString().split('T')[0];

	let data = $props();
	let token = $state(data.token);

	// When `report` changes shape Svelte does not detect the update in a way
	// that causes the NewDisease child component to remount or re-evaluate properly.
	// So to force reactivity we reassign a new object to `report` after the mutation.
	// This works because Svelte tracks object references for reactivity.
	let report = $state<Report | null>(data.report || null);

	async function updateDisease() {
		if (!report) {
			console.error('No report to update');
			return;
		}
		if (!report.disease) {
			console.error('No disease information to update');
			return;
		}
		const symptomsArray: string[] = Array.isArray(report.disease.symptoms)
			? report.disease.symptoms
			: (report.disease.symptoms || '')
					.split(',')
					.map((s) => s.trim())
					.filter(Boolean);

		const resDisease = await fetch(`/api/reports/${report.id}/disease`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			},
			body: JSON.stringify({
				disease_name: report.disease.disease_name,
				disease_category: report.disease.disease_category,
				severity_level: report.disease.severity_level,
				date_detected: report.disease.date_detected,
				symptoms: symptomsArray,
				lab_results: report.disease.lab_results,
				treatment_status: report.disease.treatment_status
			})
		});
		if (resDisease.ok) {
			const diseaseData = await resDisease.json();
			console.log('Disease data updated:', diseaseData);

			const reportResponse = await fetch(`/api/reports/${report.id}`, {
				headers: { Authorization: `Bearer ${token}` }
			});
			const updatedReport = await reportResponse.json();
			console.log('The updated report after the disease was created:', updatedReport);

			return diseaseData;
		} else {
			console.error('Failed to update disease data');
			console.error(await resDisease.text());
			return false;
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

{#if report}
	<div>
		<h2 class="text-base/7 font-semibold text-gray-900">Disease</h2>
		<div class="mt-1 text-sm/6 text-gray-600">
			Report ID:
			<input bind:value={report.id} readonly />
		</div>
	</div>
	<div class="grid max-w-2xl grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6 md:col-span-2">
		<div class="sm:col-span-4">
			<label for="diseaseName" class="block text-sm/6 font-medium text-gray-900">Disease name</label
			>
			<div class="mt-2">
				<div
					class="inline-flex w-fit items-center rounded-md bg-white outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600"
				>
					<input
						name="diseaseName"
						type="text"
						class="shrink-0 select-none text-base text-gray-500 sm:text-sm/6"
						bind:value={report.disease.disease_name}
						placeholder="Enter disease name"
					/>
				</div>
			</div>
		</div>
		<div class="sm:col-span-4">
			<label for="diseasecategory" class="block text-sm/6 font-medium text-gray-900"
				>Disease category</label
			>
			<div class="mt-2">
				<div
					class="inline-flex w-fit items-center rounded-md bg-white outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600"
				>
					<select
						name="diseasecategory"
						class="shrink-0 select-none text-base text-gray-500 sm:text-sm/6"
						bind:value={report.disease.disease_category}
					>
						<option value="" disabled selected>Select a category</option>
						<option value="Viral">Viral</option>
						<option value="Bacterial">Bacterial</option>
						<option value="Parasitic">Parasitic</option>
						<option value="Other">Other</option>
					</select>
				</div>
			</div>
		</div>
		<div class="sm:col-span-4">
			<label for="severitylevel" class="block text-sm/6 font-medium text-gray-900"
				>Severity level</label
			>
			<div class="mt-2">
				<div
					class="inline-flex w-fit items-center rounded-md bg-white outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600"
				>
					<select
						name="severitylevel"
						class="shrink-0 select-none text-base text-gray-500 sm:text-sm/6"
						bind:value={report.disease.severity_level}
					>
						<option value="" disabled selected>Select a severity</option>
						<option value="Low">Low</option>
						<option value="Medium">Medium</option>
						<option value="High">High</option>
						<option value="Critical">Critical</option>
					</select>
				</div>
			</div>
		</div>
		<div class="sm:col-span-4">
			<label for="datedetected" class="block text-sm/6 font-medium text-gray-900"
				>Date detected</label
			>
			<div class="mt-2">
				<div
					class="inline-flex w-fit items-center rounded-md bg-white outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600"
				>
					<input
						type="date"
						name="datedetected"
						max={today}
						defaultValue={today}
						class="shrink-0 select-none text-base text-gray-500 sm:text-sm/6"
						bind:value={report.disease.date_detected}
					/>
				</div>
			</div>
		</div>
		<div class="col-span-full">
			<label for="symptoms" class="block text-sm/6 font-medium text-gray-900">Symptoms</label>
			<div class="mt-2">
				<textarea
					name="symptoms"
					id="symptoms"
					rows="3"
					bind:value={report.disease.symptoms}
					class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
				></textarea>
			</div>
			<p class="mt-3 text-sm/6 text-gray-600">List symptoms separated by commas.</p>
		</div>
		<div class="col-span-full">
			<label for="labs" class="block text-sm/6 font-medium text-gray-900">Laboratory results</label>
			<div class="mt-2">
				<textarea
					name="labs"
					id="labs"
					rows="3"
					bind:value={report.disease.lab_results}
					class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
				></textarea>
			</div>
			<p class="mt-3 text-sm/6 text-gray-600">Enter the laboratory results (if any) here.</p>
		</div>
		<div class="sm:col-span-4">
			<label for="severitylevel" class="block text-sm/6 font-medium text-gray-900"
				>Treatment status</label
			>
			<div class="mt-2">
				<div
					class="inline-flex w-fit items-center rounded-md bg-white outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600"
				>
					<select
						name="severitylevel"
						class="shrink-0 select-none text-base text-gray-500 sm:text-sm/6"
						bind:value={report.disease.treatment_status}
					>
						<option value="" disabled selected>Select a treatment status</option>
						<option value="None">None</option>
						<option value="Ongoing">Ongoing</option>
						<option value="Completed">Completed</option>
					</select>
				</div>
			</div>
		</div>
		<div class="mt-6 flex items-center justify-end gap-x-6">
			<button
				onclick={once(preventDefault(updateDisease))}
				class="shadow-xs rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
				>Save</button
			>
		</div>
	</div>
{/if}
