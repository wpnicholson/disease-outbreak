<script lang="ts">
	import { page } from '$app/state';
	import Headshot from '$lib/assets/icons-192.webp?enhanced';

	// Reactive variable to track the state of the mobile menu
	let isMenuOpen = false;

	// Function to toggle the menu state
	function toggleMenu() {
		isMenuOpen = !isMenuOpen;
	}
</script>

<nav class="shadow-sm">
	<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="flex h-16 justify-between">
			<div class="flex items-center">
				<a href="/dashboard" aria-label="Headshot" class="flex items-center">
					<enhanced:img
						src={Headshot}
						alt="Headshort of the author"
						class="inline-block size-6 sm:size-8 lg:size-12 rounded-full mr-2"
					/>
				</a>
			</div>
			<div class="hidden sm:ml-6 sm:flex sm:space-x-8">
				<a
					href="/dashboard"
					class={`inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium ${
						page.url.pathname === '/dashboard'
							? 'border-highlight text-gray-900'
							: 'border-transparent text-gray-600 hover:border-gray-300 hover:text-gray-800'
					}`}>Home</a
				>
				<a
					href="/dashboard/audit-logs"
					class={`inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium ${
						page.url.pathname === '/dashboard/audit-logs'
							? 'border-highlight text-gray-900'
							: 'border-transparent text-gray-600 hover:border-gray-300 hover:text-gray-800'
					}`}>Audit</a
				>
				<a
					href="/dashboard/statistics"
					class={`inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium ${
						page.url.pathname === '/dashboard/statistics'
							? 'border-highlight text-gray-900'
							: 'border-transparent text-gray-600 hover:border-gray-300 hover:text-gray-800'
					}`}>Statistics</a
				>
				<a
					href="/dashboard/reporter"
					class={`inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium ${
						page.url.pathname === '/dashboard/reporter'
							? 'border-highlight text-gray-900'
							: 'border-transparent text-gray-600 hover:border-gray-300 hover:text-gray-800'
					}`}>Reporter</a
				>
				<a
					href="/dashboard/patient"
					class={`inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium ${
						page.url.pathname === '/dashboard/patient'
							? 'border-highlight text-gray-900'
							: 'border-transparent text-gray-600 hover:border-gray-300 hover:text-gray-800'
					}`}>Patient</a
				>
				<a
					href="/dashboard/disease"
					class={`inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium ${
						page.url.pathname === '/dashboard/disease'
							? 'border-highlight text-gray-900'
							: 'border-transparent text-gray-600 hover:border-gray-300 hover:text-gray-800'
					}`}>Disease</a
				>
				<a
					href="/dashboard/summary"
					class={`inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium ${
						page.url.pathname === '/dashboard/summary'
							? 'border-highlight text-gray-900'
							: 'border-transparent text-gray-600 hover:border-gray-300 hover:text-gray-800'
					}`}>Summary</a
				>
			</div>

			<div class="-mr-2 flex items-center sm:hidden">
				<!-- Mobile menu button -->
				<button
					type="button"
					class="relative inline-flex items-center justify-center rounded-md p-2 text-gray-900 hover:bg-gray-100 focus:ring-2 focus:ring-indigo-500 focus:outline-hidden focus:ring-inset"
					aria-controls="mobile-menu"
					aria-expanded={isMenuOpen}
					on:click={toggleMenu}
				>
					<!-- Icon when menu is closed -->
					<svg
						class={isMenuOpen ? 'hidden size-6' : 'block size-6'}
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						aria-hidden="true"
						data-slot="icon"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
						/>
					</svg>
					<!-- Icon when menu is open -->
					<svg
						class={isMenuOpen ? 'block size-6' : 'hidden size-6'}
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						aria-hidden="true"
						data-slot="icon"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
					</svg>
				</button>
			</div>
		</div>
	</div>

	<!-- Mobile menu, show/hide based on menu state. -->
	<div class="sm:hidden" id="mobile-menu" class:hidden={!isMenuOpen}>
		<div class="space-y-1 pt-2 pb-3">
			<a
				href="/"
				class={`block border-l-4 py-2 pr-4 pl-3 text-base font-medium ${
					page.url.pathname === '/'
						? 'border-accent bg-highlight text-primary'
						: 'border-transparent text-gray-600 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-700'
				}`}>Home</a
			>
			<a
				href="/mapping"
				class={`block border-l-4 py-2 pr-4 pl-3 text-base font-medium ${
					page.url.pathname === '/mapping'
						? 'border-accent bg-highlight text-primary'
						: 'border-transparent text-gray-600 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-700'
				}`}>Map Design</a
			>
			<a
				href="/identity"
				class={`block border-l-4 py-2 pr-4 pl-3 text-base font-medium ${
					page.url.pathname === '/identity'
						? 'border-accent bg-highlight text-primary'
						: 'border-transparent text-gray-600 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-700'
				}`}>Visual Design</a
			>
			<a
				href="/storytelling"
				class={`block border-l-4 py-2 pr-4 pl-3 text-base font-medium ${
					page.url.pathname === '/storytelling'
						? 'border-accent bg-highlight text-primary'
						: 'border-transparent text-gray-600 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-700'
				}`}>Storytelling</a
			>
		</div>
	</div>
</nav>
