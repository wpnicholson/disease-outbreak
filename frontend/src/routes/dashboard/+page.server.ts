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

    // Sent to the sibling `+page.svelte` as props.
    return {
        user,
        token,
        login
    };
}
