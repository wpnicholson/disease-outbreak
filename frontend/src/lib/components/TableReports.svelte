<script lang="ts">
	import type { Report } from '$lib/backendtypes';
	import { formatDate } from '$lib/utils/formatdate';
	let { reports }: { reports: Report[] | [] } = $props();

	console.log('Data received in TableReports page:', reports);
</script>

<div class="px-4 sm:px-6 lg:px-8">
	<div class="sm:flex sm:items-center">
		<div class="sm:flex-auto">
			<h1 class="text-base font-semibold text-gray-900">Your Reports</h1>
			<p class="mt-2 text-sm text-gray-700">
				A list of all the reports in your account including their ID, status, and disease.
			</p>
		</div>
		<div class="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
			<button
				type="button"
				class="shadow-xs block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
				>Add new report</button
			>
		</div>
	</div>
	<div class="mt-8 flow-root">
		<div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
			<div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
				<table class="min-w-full divide-y divide-gray-300">
					<thead>
						<tr>
							<th
								scope="col"
								class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-0"
								>Id</th
							>
							<th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
								>Created at</th
							>
							<th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
								>Updated at</th
							>
							<th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
								>Reporter Id</th
							>
							<th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
								>Number of Patients</th
							>
							<th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
								>Disease Id</th
							>
							<th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-0">
								<span class="sr-only">Edit</span>
							</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200">
						{#each reports as report}
							<tr>
								<td
									class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-0"
									>{report.id}</td
								>
								<td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500"
									>{formatDate(report.created_at)}</td
								>
								<td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500"
									>{formatDate(report.updated_at)}</td
								>
								<td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500"
									>{report.reporter?.id ?? 'None'}</td
								>
								<td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500"
									>{report.patients.length == 0 ? 'None' : report.patients.length}</td
								>
								<td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500"
									>{report.disease?.id ?? 'None'}</td
								>
								<td
									class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0"
								>
									<a
										href="/dashboard/newreport/{report.id}"
										class="text-indigo-600 hover:text-indigo-900"
										>Edit<span class="sr-only">report id {report.id}</span></a
									>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</div>
</div>
