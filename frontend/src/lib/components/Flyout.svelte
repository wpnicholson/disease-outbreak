<script lang="ts">
	let showFlyout = $state(false);

	function toggleFlyout() {
		showFlyout = !showFlyout;
	}
</script>

<div class="relative">
	<button
		type="button"
		onclick={toggleFlyout}
		aria-expanded="false"
		class="inline-flex items-center gap-x-1 text-sm/6 font-semibold text-gray-900"
	>
		<span>Add new patient</span>
		<svg viewBox="0 0 20 20" fill="currentColor" data-slot="icon" aria-hidden="true" class="size-5">
			<path
				d="M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z"
				clip-rule="evenodd"
				fill-rule="evenodd"
			/>
		</svg>
	</button>

	<!--
    Flyout menu, show/hide based on flyout menu state.

    Entering: "transition ease-out duration-200"
      From: "opacity-0 translate-y-1"
      To: "opacity-100 translate-y-0"
    Leaving: "transition ease-in duration-150"
      From: "opacity-100 translate-y-0"
      To: "opacity-0 translate-y-1"
  -->
	{#if showFlyout}
		<form class="fixed left-1/2 top-10 z-50 -translate-x-1/2">
			<div
				class="w-screen max-w-md flex-auto overflow-hidden rounded-3xl bg-white text-sm/6 shadow-lg ring-1 ring-gray-900/5 lg:max-w-3xl"
			>
				<div class="grid grid-cols-1 gap-x-6 gap-y-1 p-4 lg:grid-cols-2">
					<!-- First name -->
					<div class="group relative flex gap-x-6 rounded-lg p-4 hover:bg-gray-50">
						<div
							class="mt-1 flex size-11 flex-none items-center justify-center rounded-lg bg-gray-50 group-hover:bg-white"
						>
							<span class="icon-park--first-name"></span>
						</div>
						<div class="flex flex-col">
							<label for="firstName" class="font-semibold text-gray-900">First name</label>
							<input
								id="firstName"
								name="firstName"
								class="mt-1 text-gray-600"
								placeholder="Enter first name"
							/>
						</div>
					</div>
					<!-- Last name -->
					<div class="group relative flex gap-x-6 rounded-lg p-4 hover:bg-gray-50">
						<div
							class="mt-1 flex size-11 flex-none items-center justify-center rounded-lg bg-gray-50 group-hover:bg-white"
						>
							<span class="icon-park--last-name"></span>
						</div>
						<div class="flex flex-col">
							<label for="lastName" class="font-semibold text-gray-900">Last name</label>
							<input
								id="lastName"
								name="lastName"
								class="mt-1 text-gray-600"
								placeholder="Enter last name"
							/>
						</div>
					</div>
					<!-- Date of birth -->
					<div class="group relative flex gap-x-6 rounded-lg p-4 hover:bg-gray-50">
						<div
							class="mt-1 flex size-11 flex-none items-center justify-center rounded-lg bg-gray-50 group-hover:bg-white"
						>
							<span class="icon-park-outline--calendar"></span>
						</div>
						<div class="flex flex-col">
							<label for="dateOfBirth" class="font-semibold text-gray-900">Date of birth</label>
							<input
								id="dateOfBirth"
								name="dateOfBirth"
								type="date"
								class="mt-1 text-gray-600"
								placeholder="Enter date of birth"
							/>
						</div>
					</div>
					<!-- Gender -->
					<div class="group relative flex gap-x-6 rounded-lg p-4 hover:bg-gray-50">
						<div
							class="mt-1 flex size-11 flex-none items-center justify-center rounded-lg bg-gray-50 group-hover:bg-white"
						>
							<span class="streamline-ultimate--gender-hetero"></span>
						</div>
						<div class="flex flex-col">
							<label for="gender" class="font-semibold text-gray-900">Gender</label>
							<input
								id="gender"
								name="gender"
								class="mt-1 text-gray-600"
								placeholder="Enter gender"
							/>
						</div>
					</div>
					<!-- Medical repord number -->
					<div class="group relative flex gap-x-6 rounded-lg p-4 hover:bg-gray-50">
						<div
							class="mt-1 flex size-11 flex-none items-center justify-center rounded-lg bg-gray-50 group-hover:bg-white"
						>
							<span class="icon-park-outline--id-card"></span>
						</div>
						<div class="flex flex-col">
							<label for="medicalRecord" class="font-semibold text-gray-900"
								>Medical record number</label
							>
							<input
								id="medicalRecord"
								name="medicalRecord"
								class="mt-1 text-gray-600"
								placeholder="Enter medical record number"
							/>
						</div>
					</div>
					<!-- Emergency contact -->
					<div class="group relative flex gap-x-6 rounded-lg p-4 hover:bg-gray-50">
						<div
							class="mt-1 flex size-11 flex-none items-center justify-center rounded-lg bg-gray-50 group-hover:bg-white"
						>
							<span class="streamline-sharp--emergency-call"></span>
						</div>
						<div class="flex flex-col">
							<label for="emergencyContact" class="font-semibold text-gray-900"
								>Emergency contact</label
							>
							<input
								id="emergencyContact"
								name="emergencyContact"
								class="mt-1 text-gray-600"
								placeholder="Enter emergency contact"
							/>
						</div>
					</div>
				</div>
			</div>
		</form>
	{/if}
</div>
