import { redirect } from '@sveltejs/kit';

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
    const sessionId = event.cookies.get('session_id');
    const sessionUser = event.cookies.get('session_user');

    // Hydrate authenticated user into event.locals
    if (sessionId && sessionUser) {
        try {
            event.locals.user = JSON.parse(sessionUser);
            event.locals.token = sessionId;
            // Optional: Basic expiry check
            // const { exp } = jwtDecode(sessionId);
            // if (Date.now() >= exp * 1000) throw new Error('Token expired');
        } catch (error) {
            console.warn('Failed to parse session cookies', error);
            event.locals.user = undefined;
            event.locals.token = undefined;
        }
    } else {
        event.locals.user = undefined;
        event.locals.token = undefined;
    }

    // Redirect unauthenticated access to /dashboard
    if (!event.locals.user && event.url.pathname.startsWith('/dashboard')) {
        const redirectTo = event.url.pathname + event.url.search;
        const params = new URLSearchParams({ redirectTo });
        throw redirect(303, `/login?${params}`);
    }

    return resolve(event);
}
