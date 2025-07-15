<script lang="ts">
	let dob: string | undefined = $state();
	let today: Date = new Date();
	let age: number | null = $derived.by(() => {
		if (!dob) return null;
		const birthDate = new Date(dob);
		let years = today.getFullYear() - birthDate.getFullYear();
		const m = today.getMonth() - birthDate.getMonth();
		if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
			years--;
		}
		return years;
	});
</script>

<div class="divide-y divide-gray-900/10">
	<div class="grid grid-cols-1 gap-x-8 gap-y-8 py-10 md:grid-cols-3">
		<div class="px-4 sm:px-0">
			<h2 class="text-base/7 font-semibold text-gray-900">Personal Information</h2>
			<p class="mt-1 text-sm/6 text-gray-600">
				Use a permanent address where you can receive mail.
			</p>
		</div>

		<form class="shadow-xs bg-white ring-1 ring-gray-900/5 sm:rounded-xl md:col-span-2">
			<div class="px-4 py-6 sm:p-8">
				<div class="grid max-w-2xl grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
					<div class="sm:col-span-3">
						<label for="first-name" class="block text-sm/6 font-medium text-gray-900"
							>First name</label
						>
						<div class="mt-2">
							<input
								type="text"
								name="first-name"
								id="first-name"
								autocomplete="given-name"
								class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
							/>
						</div>
					</div>

					<div class="sm:col-span-3">
						<label for="last-name" class="block text-sm/6 font-medium text-gray-900"
							>Last name</label
						>
						<div class="mt-2">
							<input
								type="text"
								name="last-name"
								id="last-name"
								autocomplete="family-name"
								class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
							/>
						</div>
					</div>

					<div class="sm:col-span-3">
						<label for="dob" class="block text-sm/6 font-medium text-gray-900">Date of birth</label>
						<div class="mt-2">
							<input
								bind:value={dob}
								id="dob"
								name="dob"
								type="date"
								autocomplete="bday"
                                max={today.toISOString().split('T')[0]}
								class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
							/>
						</div>
					</div>

					<div class="sm:col-span-3">
						<label for="email" class="block text-sm/6 font-medium text-gray-900">Age <span class="text-xs">(in years)</span></label>
						<div class="mt-2">{age}</div>
					</div>

					<div class="sm:col-span-3">
						<label for="country" class="block text-sm/6 font-medium text-gray-900">Gender</label>
						<div class="mt-2 grid grid-cols-1">
							<select
								id="country"
								name="country"
								autocomplete="country-name"
								class="col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pl-3 pr-8 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
							>
								<option>Male</option>
								<option>Female</option>
								<option>Other</option>
							</select>
							<svg
								class="pointer-events-none col-start-1 row-start-1 mr-2 size-5 self-center justify-self-end text-gray-500 sm:size-4"
								viewBox="0 0 16 16"
								fill="currentColor"
								aria-hidden="true"
								data-slot="icon"
							>
								<path
									fill-rule="evenodd"
									d="M4.22 6.22a.75.75 0 0 1 1.06 0L8 8.94l2.72-2.72a.75.75 0 1 1 1.06 1.06l-3.25 3.25a.75.75 0 0 1-1.06 0L4.22 7.28a.75.75 0 0 1 0-1.06Z"
									clip-rule="evenodd"
								/>
							</svg>
						</div>
					</div>

					<div class="col-span-full">
						<label for="street-address" class="block text-sm/6 font-medium text-gray-900"
							>Patient address</label
						>
						<div class="mt-2">
							<input
								type="text"
								name="street-address"
								id="street-address"
								autocomplete="street-address"
								class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
							/>
						</div>
					</div>

					<div class="col-span-full">
						<label for="street-address" class="block text-sm/6 font-medium text-gray-900"
							>Emergency contact</label
						>
						<div class="mt-2">
							<input
								type="text"
								name="street-address"
								id="street-address"
								autocomplete="street-address"
								class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
							/>
						</div>
					</div>
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
