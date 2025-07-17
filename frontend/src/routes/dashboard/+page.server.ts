import type { Load } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = ({ locals }) => {
    const user = locals.user;
    const token = locals.token;
    let login = false;

    if (user) {
        login = true;
    } else {
        login = false;
    }

    console.log('User in the +page.server.ts load function:', user);

    // Sent to the sibling `+page.svelte` as props.
    return {
        user,
        token,
        login
    };
}
