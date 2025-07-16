<script lang="ts">
	let { data } = $props();
	let reportDetails = $state(null);
	const today = new Date().toISOString().split('T')[0];

	async function createNewReport() {
		const res = await fetch('/api/reports/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${data.token}`
			},
			body: JSON.stringify(data.user)
		});
		if (res.ok) {
			const report = await res.json();
			console.log('New report created:', report);
			reportDetails = report;
			reportDetails.reporter = data.user.id;
		} else {
			console.error('Failed to create new report');
			console.error(await res.text());
		}
	}

	async function updateDisease() {
		const symptomsArray = Array.isArray(reportDetails.symptoms)
			? reportDetails.symptoms
			: (reportDetails.symptoms || '')
					.split(',')
					.map((s) => s.trim())
					.filter(Boolean);

		const resDisease = await fetch(`/api/reports/${reportDetails.id}/disease`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${data.token}`
			},
			body: JSON.stringify({
				disease_name: reportDetails.disease_name,
				disease_category: reportDetails.disease_category,
				severity_level: reportDetails.severity_level,
				date_detected: reportDetails.date_detected,
				symptoms: symptomsArray,
				lab_results: reportDetails.lab_results,
				treatment_status: reportDetails.treatment_status
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

	async function updateReport() {
		const resDisease = await updateDisease();

		if (!resDisease) {
			console.error('Not attempting to update report without disease data');
			return;
		}

		console.log('Updating report with disease data:', resDisease);

		const res = await fetch(`/api/reports/${reportDetails.id}`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${data.token}`
			},
			body: JSON.stringify({
				disease: resDisease,
				disease_id: resDisease.id
			})
		});
		if (res.ok) {
			const updatedReport = await res.json();
			console.log('Report updated:', updatedReport);
			reportDetails = updatedReport;
		} else {
			console.error('Failed to update report');
			console.error(await res.text());
		}
	}

	function once(fn) {
		return function (event) {
			if (fn) fn.call(this, event);
			fn = null;
		};
	}
	function preventDefault(fn) {
		return function (event) {
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

	{#if reportDetails}
		<form>
			<div class="mt-10 space-y-12">
				<div
					class="grid grid-cols-1 gap-x-8 gap-y-10 border-b border-gray-900/10 pb-12 md:grid-cols-3"
				>
					<div>
						<h2 class="text-base/7 font-semibold text-gray-900">Disease</h2>
						<div class="mt-1 text-sm/6 text-gray-600">
							Report ID:
							<input bind:value={reportDetails.id} readonly />
						</div>
					</div>

					<div class="grid max-w-2xl grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6 md:col-span-2">
						<div class="sm:col-span-4">
							<label for="diseaseName" class="block text-sm/6 font-medium text-gray-900"
								>Disease name</label
							>
							<div class="mt-2">
								<div
									class="inline-flex w-fit items-center rounded-md bg-white outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600"
								>
									<input
										name="diseaseName"
										type="text"
										class="shrink-0 select-none text-base text-gray-500 sm:text-sm/6"
										bind:value={reportDetails.disease_name}
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
										bind:value={reportDetails.disease_category}
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
										bind:value={reportDetails.severity_level}
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
										bind:value={reportDetails.date_detected}
									/>
								</div>
							</div>
						</div>
						<div class="col-span-full">
							<label for="symptoms" class="block text-sm/6 font-medium text-gray-900"
								>Symptoms</label
							>
							<div class="mt-2">
								<textarea
									name="symptoms"
									id="symptoms"
									rows="3"
									bind:value={reportDetails.symptoms}
									class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
								></textarea>
							</div>
							<p class="mt-3 text-sm/6 text-gray-600">List symptoms separated by commas.</p>
						</div>
						<div class="col-span-full">
							<label for="labs" class="block text-sm/6 font-medium text-gray-900"
								>Laboratory results</label
							>
							<div class="mt-2">
								<textarea
									name="labs"
									id="labs"
									rows="3"
									bind:value={reportDetails.lab_results}
									class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
								></textarea>
							</div>
							<p class="mt-3 text-sm/6 text-gray-600">
								Enter the laboratory results (if any) here.
							</p>
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
										bind:value={reportDetails.treatment_status}
									>
										<option value="" disabled selected>Select a treatment status</option>
										<option value="None">None</option>
										<option value="Ongoing">Ongoing</option>
										<option value="Completed">Completed</option>
									</select>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="mt-6 flex items-center justify-end gap-x-6">
				<button type="button" class="text-sm/6 font-semibold text-gray-900">Cancel</button>
				<button
					onclick={once(preventDefault(updateReport))}
					class="shadow-xs rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
					>Save</button
				>
			</div>
		</form>
	{/if}
</div>
