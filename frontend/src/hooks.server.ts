import { redirect } from '@sveltejs/kit'; // The 'redirect' helper is imported from '@sveltejs/kit'

/** @type {import('@sveltejs/kit').Handle} */ // The `handle` hook is of type `Handle` from `@sveltejs/kit`.
export async function handle({ event, resolve }) { // The `handle` function receives an `event` object and a `resolve` function.
    const sessionid = event.cookies.get('session_id'); // Access cookies from the `event` object to get the session ID.

    // Protect specific routes (e.g., '/admin', '/dashboard')
    if (!sessionid && event.url.pathname.startsWith('/dashboard')) { // The `event.url` object provides properties like `pathname`.
        // Redirect to login, preserving the intended destination
        const redirectTo = event.url.pathname + event.url.search;
        const params = new URLSearchParams({ redirectTo });
        // Use the `redirect` helper with an HTTP status code (e.g., 307 Temporary Redirect) and the login URL.
        // Calling `redirect(...)` will throw an exception, stopping further execution.
        redirect(307, `/login?${params}`);
    }

    const response = await resolve(event); // The `resolve` function renders the route and generates a `Response`.
    return response;
}
