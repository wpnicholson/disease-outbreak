<script lang="ts">
	let { form } = $props();
</script>

<div>
	<label for="email" class="block text-sm/6 font-medium text-gray-900">Email address</label>
	<div class="mt-2">
		<input
			type="email"
			name="email"
			id="email"
			autocomplete="off"
			value={form?.email || ''}
			required
			class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
		/>
		{#if form?.missing_email}<p class="error text-red-500 font-semibold">Please provide an email</p>{/if}
	</div>
</div>

<div>
	<div class="flex items-center justify-between">
		<label for="password" class="block text-sm/6 font-medium text-gray-900">Password</label>
	</div>
	<div class="mt-2">
		<input
			type="password"
			name="password"
			id="password"
			autocomplete="off"
			value={''}
			required
			class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
		/>
		{#if form?.missing_password}<p class="error text-red-500 font-semibold">Please provide a password</p>{/if}
	</div>
</div>

<div>
	{#if form?.password_incorrect}<p class="error text-red-500 font-semibold">Check credentials and try again</p>{/if}
	<button
		type="submit"
		class="shadow-xs flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
		>Sign in</button
	>
</div>
