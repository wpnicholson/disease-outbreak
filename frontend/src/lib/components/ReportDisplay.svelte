<script lang="ts">
	import type { Report } from '$lib/backendtypes';
	import NewDisease from '$lib/components/NewDisease.svelte';

	// We call this component from within a Svelte `{#if report && token}` block;
	// so we expect `report` and `token` to be defined.
	let { report, token }: { report: Report, token: string } = $props();

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
						<input bind:value={report.created_at} readonly class="block min-w-0 grow py-1.5 pl-1 pr-3 text-base text-gray-900 sm:text-sm/6" />
					</div>
					<div class="sm:col-span-4">
						<span class="block text-sm/6 font-medium text-gray-900">Status</span>
						<input bind:value={report.status} readonly class="block min-w-0 grow py-1.5 pl-1 pr-3 text-base text-gray-900 sm:text-sm/6" />
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Disease Information -->
	<div class="grid grid-cols-1 gap-x-8 gap-y-8 py-10 md:grid-cols-3">
		<div class="px-4 sm:px-0">
			<h2 class="text-base/7 font-semibold text-gray-900">Disease Information</h2>
			<p class="mt-1 text-sm/6 text-gray-600">Add or update disease information for this report.</p>
		</div>

		<div class="shadow-xs bg-slate-100 ring-1 ring-gray-900/5 sm:rounded-xl md:col-span-2">
					<NewDisease {report} {token} />
		</div>
	</div>

	<div class="grid grid-cols-1 gap-x-8 gap-y-8 py-10 md:grid-cols-3">
		<div class="px-4 sm:px-0">
			<h2 class="text-base/7 font-semibold text-gray-900">Notifications</h2>
			<p class="mt-1 text-sm/6 text-gray-600">
				We'll always let you know about important changes, but you pick what else you want to hear
				about.
			</p>
		</div>

		<form class="shadow-xs bg-white ring-1 ring-gray-900/5 sm:rounded-xl md:col-span-2">
			<div class="px-4 py-6 sm:p-8">
				<div class="max-w-2xl space-y-10 md:col-span-2">
					<fieldset>
						<legend class="text-sm/6 font-semibold text-gray-900">By email</legend>
						<div class="mt-6 space-y-6">
							<div class="flex gap-3">
								<div class="flex h-6 shrink-0 items-center">
									<div class="group grid size-4 grid-cols-1">
										<input
											id="comments"
											type="checkbox"
											name="comments"
											checked
											aria-describedby="comments-description"
											class="col-start-1 row-start-1 appearance-none rounded-sm border border-gray-300 bg-white checked:border-indigo-600 checked:bg-indigo-600 indeterminate:border-indigo-600 indeterminate:bg-indigo-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100 forced-colors:appearance-auto"
										/>
										<svg
											viewBox="0 0 14 14"
											fill="none"
											class="group-has-disabled:stroke-gray-950/25 pointer-events-none col-start-1 row-start-1 size-3.5 self-center justify-self-center stroke-white"
										>
											<path
												d="M3 8L6 11L11 3.5"
												stroke-width="2"
												stroke-linecap="round"
												stroke-linejoin="round"
												class="group-has-checked:opacity-100 opacity-0"
											/>
											<path
												d="M3 7H11"
												stroke-width="2"
												stroke-linecap="round"
												stroke-linejoin="round"
												class="group-has-indeterminate:opacity-100 opacity-0"
											/>
										</svg>
									</div>
								</div>
								<div class="text-sm/6">
									<label for="comments" class="font-medium text-gray-900">Comments</label>
									<p id="comments-description" class="text-gray-500">
										Get notified when someones posts a comment on a posting.
									</p>
								</div>
							</div>
							<div class="flex gap-3">
								<div class="flex h-6 shrink-0 items-center">
									<div class="group grid size-4 grid-cols-1">
										<input
											id="candidates"
											type="checkbox"
											name="candidates"
											aria-describedby="candidates-description"
											class="col-start-1 row-start-1 appearance-none rounded-sm border border-gray-300 bg-white checked:border-indigo-600 checked:bg-indigo-600 indeterminate:border-indigo-600 indeterminate:bg-indigo-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100 forced-colors:appearance-auto"
										/>
										<svg
											viewBox="0 0 14 14"
											fill="none"
											class="group-has-disabled:stroke-gray-950/25 pointer-events-none col-start-1 row-start-1 size-3.5 self-center justify-self-center stroke-white"
										>
											<path
												d="M3 8L6 11L11 3.5"
												stroke-width="2"
												stroke-linecap="round"
												stroke-linejoin="round"
												class="group-has-checked:opacity-100 opacity-0"
											/>
											<path
												d="M3 7H11"
												stroke-width="2"
												stroke-linecap="round"
												stroke-linejoin="round"
												class="group-has-indeterminate:opacity-100 opacity-0"
											/>
										</svg>
									</div>
								</div>
								<div class="text-sm/6">
									<label for="candidates" class="font-medium text-gray-900">Candidates</label>
									<p id="candidates-description" class="text-gray-500">
										Get notified when a candidate applies for a job.
									</p>
								</div>
							</div>
							<div class="flex gap-3">
								<div class="flex h-6 shrink-0 items-center">
									<div class="group grid size-4 grid-cols-1">
										<input
											id="offers"
											type="checkbox"
											name="offers"
											aria-describedby="offers-description"
											class="col-start-1 row-start-1 appearance-none rounded-sm border border-gray-300 bg-white checked:border-indigo-600 checked:bg-indigo-600 indeterminate:border-indigo-600 indeterminate:bg-indigo-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100 forced-colors:appearance-auto"
										/>
										<svg
											viewBox="0 0 14 14"
											fill="none"
											class="group-has-disabled:stroke-gray-950/25 pointer-events-none col-start-1 row-start-1 size-3.5 self-center justify-self-center stroke-white"
										>
											<path
												d="M3 8L6 11L11 3.5"
												stroke-width="2"
												stroke-linecap="round"
												stroke-linejoin="round"
												class="group-has-checked:opacity-100 opacity-0"
											/>
											<path
												d="M3 7H11"
												stroke-width="2"
												stroke-linecap="round"
												stroke-linejoin="round"
												class="group-has-indeterminate:opacity-100 opacity-0"
											/>
										</svg>
									</div>
								</div>
								<div class="text-sm/6">
									<label for="offers" class="font-medium text-gray-900">Offers</label>
									<p id="offers-description" class="text-gray-500">
										Get notified when a candidate accepts or rejects an offer.
									</p>
								</div>
							</div>
						</div>
					</fieldset>

					<fieldset>
						<legend class="text-sm/6 font-semibold text-gray-900">Push notifications</legend>
						<p class="mt-1 text-sm/6 text-gray-600">
							These are delivered via SMS to your mobile phone.
						</p>
						<div class="mt-6 space-y-6">
							<div class="flex items-center gap-x-3">
								<input
									id="push-everything"
									type="radio"
									name="push-notifications"
									checked
									class="not-checked:before:hidden relative size-4 appearance-none rounded-full border border-gray-300 bg-white before:absolute before:inset-1 before:rounded-full before:bg-white checked:border-indigo-600 checked:bg-indigo-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:border-gray-300 disabled:bg-gray-100 disabled:before:bg-gray-400 forced-colors:appearance-auto forced-colors:before:hidden"
								/>
								<label for="push-everything" class="block text-sm/6 font-medium text-gray-900"
									>Everything</label
								>
							</div>
							<div class="flex items-center gap-x-3">
								<input
									id="push-email"
									type="radio"
									name="push-notifications"
									class="not-checked:before:hidden relative size-4 appearance-none rounded-full border border-gray-300 bg-white before:absolute before:inset-1 before:rounded-full before:bg-white checked:border-indigo-600 checked:bg-indigo-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:border-gray-300 disabled:bg-gray-100 disabled:before:bg-gray-400 forced-colors:appearance-auto forced-colors:before:hidden"
								/>
								<label for="push-email" class="block text-sm/6 font-medium text-gray-900"
									>Same as email</label
								>
							</div>
							<div class="flex items-center gap-x-3">
								<input
									id="push-nothing"
									type="radio"
									name="push-notifications"
									class="not-checked:before:hidden relative size-4 appearance-none rounded-full border border-gray-300 bg-white before:absolute before:inset-1 before:rounded-full before:bg-white checked:border-indigo-600 checked:bg-indigo-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:border-gray-300 disabled:bg-gray-100 disabled:before:bg-gray-400 forced-colors:appearance-auto forced-colors:before:hidden"
								/>
								<label for="push-nothing" class="block text-sm/6 font-medium text-gray-900"
									>No push notifications</label
								>
							</div>
						</div>
					</fieldset>
				</div>
			</div>
			<div
				class="flex items-center justify-end gap-x-6 border-t border-gray-900/10 px-4 py-4 sm:px-8"
			>
				<button type="button" class="text-sm/6 font-semibold text-gray-900">Cancel</button>
				<button
					type="submit"
					class="shadow-xs rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
					>Save</button
				>
			</div>
		</form>
	</div>
</div>
