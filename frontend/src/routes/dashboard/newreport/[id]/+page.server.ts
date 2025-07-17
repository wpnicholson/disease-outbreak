import type { PageServerLoad } from './$types';

// You can send relative URLs to your backend API.
// Make sure to set the BACKEND_URL in your environment variables.
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'; // Set this in your env

export const load: PageServerLoad = async ({ params, locals }) => {
    const token = locals.token;
    const id = params.id;

    const res = await fetch(`${BACKEND_URL}/api/reports/${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        },
    });

    if (res.ok) {
        // Sent to the sibling `+page.svelte` as props.
        return { id, report: res.ok ? await res.json() : null, token };
    } else {
        console.error('Failed to fetch report:', res.statusText);
    }

    return { id, report: null };
};
