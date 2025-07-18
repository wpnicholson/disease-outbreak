import type { User } from '$lib/backendtypes';
import type { PageServerLoad } from './$types';

// We arrive here from `src/hooks.server.ts` where the user and token are set in `event.locals`.
export const load: PageServerLoad = ({ locals }) => {
    const user: User | null = locals.user;
    const token: string | undefined = locals.token;
    let login = false;

    if (user) {
        login = true;
    } else {
        login = false;
    }

    // Sent to the sibling `routes/dashboard/+page.svelte` as props.
    return {
        user,
        token,
        login
    };
}
