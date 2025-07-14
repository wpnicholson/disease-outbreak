<!-- routes/login/+layout.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';

	let { children } = $props();

  onMount(() => {
    document.documentElement.className = 'h-full bg-white';
    document.body.className = 'h-full';
  });
</script>

{@render children()}
