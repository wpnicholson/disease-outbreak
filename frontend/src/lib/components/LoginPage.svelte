<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';

  let email = '';
  let password = '';
  let error: string | null = null;

  async function handleLogin() {
    error = null;
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const errorData = await response.json();
        error = errorData.detail || 'Login failed';
        return;
      }

      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);
      goto('/dashboard'); // Redirect after login success
    } catch (err) {
      error = 'Network error or server unavailable';
    }
  }
</script>

<div class="flex flex-col items-center justify-center min-h-screen p-4 bg-gray-100">
  <div class="w-full max-w-sm p-8 bg-white rounded-lg shadow">
    <h1 class="mb-6 text-2xl font-bold text-center">Login</h1>

    {#if error}
      <p class="mb-4 text-sm text-red-600">{error}</p>
    {/if}

    <div class="mb-4">
      <label class="block mb-1 text-sm font-medium">Email</label>
      <input class="w-full p-2 border rounded" type="email" bind:value={email} required />
    </div>

    <div class="mb-6">
      <label class="block mb-1 text-sm font-medium">Password</label>
      <input class="w-full p-2 border rounded" type="password" bind:value={password} required />
    </div>

    <button
      on:click|preventDefault={handleLogin}
      class="w-full p-2 font-semibold text-white bg-blue-600 rounded hover:bg-blue-700"
    >
      Log In
    </button>
  </div>
</div>
