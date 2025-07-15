<script lang="ts" >
    import { goto } from '$app/navigation';

    function redirectToAbout() {
        goto('/dashboard/summary');
    }
</script>

<div>
    <h1>Dashboard</h1>

    <button onclick={redirectToAbout}>Create a New Report</button>
</div>
