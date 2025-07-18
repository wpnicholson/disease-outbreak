<script lang="ts">
	import type { Report } from '$lib/backendtypes';
	import { once, preventDefault } from '$lib/utils/preventdefault';
	import { readonly } from 'svelte/store';
	const today = new Date().toISOString().split('T')[0];

	// We call this component from within a Svelte `{#if report && token}` block;
	// so we expect `report` and `token` to be defined.
	let { report, token }: { report: Report; token: string } = $props();

	function parseSymptoms(symptoms: string | string[] | undefined): string[] {
		if (Array.isArray(symptoms)) return symptoms;
		return (symptoms || '')
			.split(',')
			.map((s: string) => s.trim())
			.filter(Boolean);
	}

	async function updateDisease() {
		if (!report.disease) {
			console.error('No disease information to update');
			return;
		}
		const symptomsArray: string[] = parseSymptoms(report.disease.symptoms);

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

			return diseaseData;
		} else {
			console.error('Failed to update disease data');
			console.error(await resDisease.text());
			return false;
		}
	}
</script>

{#if report?.disease}
	<form class="shadow-xs bg-white ring-1 ring-gray-900/5 sm:rounded-xl md:col-span-2">
		<div class="px-4 py-6 sm:p-8">
			<!-- Disease ID -->
			<div class="sm:col-span-3">
				<label for="diseaseId" class="block text-sm/6 font-medium text-gray-900">Disease id:</label>
				<div class="mt-2">
					<input
						id="diseaseId"
						name="diseaseId"
						type="text"
						class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
						value={report.disease.id}
						readonly
					/>
				</div>
			</div>

			<!-- Disease details -->
			<div class="sm:col-span-3">
				<label for="diseaseName" class="block text-sm/6 font-medium text-gray-900"
					>Disease name</label
				>
				<div class="mt-2">
					<input
						id="diseaseName"
						name="diseaseName"
						type="text"
						class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
						bind:value={report.disease.disease_name}
						placeholder="Enter disease name"
					/>
				</div>
			</div>

			<!-- Disease category -->
			<div class="sm:col-span-3">
				<label for="diseasecategory" class="block text-sm/6 font-medium text-gray-900"
					>Disease category</label
				>
				<div class="mt-2">
					<select
						name="diseasecategory"
						class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
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

			<!-- Severity level -->
			<div class="sm:col-span-3">
				<label for="severitylevel" class="block text-sm/6 font-medium text-gray-900"
					>Severity level</label
				>
				<div class="mt-2">
					<select
						name="severitylevel"
						class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
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

			<!-- Date detected -->
			<div class="sm:col-span-3">
				<label for="datedetected" class="block text-sm/6 font-medium text-gray-900"
					>Date detected</label
				>
				<div class="mt-2">
					<input
						type="date"
						name="datedetected"
						max={today}
						defaultValue={today}
						class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
						bind:value={report.disease.date_detected}
					/>
				</div>
			</div>

			<!-- Symptoms -->
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

			<!-- Laboratory results -->
			<div class="col-span-full">
				<label for="labs" class="block text-sm/6 font-medium text-gray-900"
					>Laboratory results</label
				>
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

			<!-- Treatment status -->
			<div class="sm:col-span-4">
				<label for="severitylevel" class="block text-sm/6 font-medium text-gray-900"
					>Treatment status</label
				>
				<div class="mt-2">
					<select
						name="severitylevel"
						class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
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

		<!-- Save button -->
		<div class="flex items-center justify-end gap-x-6 border-t border-gray-900/10 px-4 py-4 sm:px-8">
			<button
				type="submit"
				onclick={once(preventDefault(updateDisease))}
				class="shadow-xs rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
				>Save</button
			>
		</div>
	</form>
{/if}
