import { NODE_ENV } from '$env/static/private';
import type { Actions } from './$types';
import { redirect, fail } from '@sveltejs/kit';

const isProduction = NODE_ENV === 'production';

export const actions = {
    login: async (event) => {
        const formData = await event.request.formData();
        const email = formData.get('email');
        const password = formData.get('password');

        // Clear any existing session cookies.
        event.cookies.delete('session_id', { path: '/' });
        // Clear any existing session user cookies.
        event.cookies.delete('session_user', { path: '/' });

        if (!email) {
            return fail(400, { missing_email: true });
        }
        if (!password) {
            return fail(400, { missing_password: true });
        }

        // Send as is via secure HTTPS connection
        const response = await event.fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });

        if (response.status === 401) {
            return fail(401, { email, password_incorrect: true });
        }
        if (response.status === 404) {
            return fail(404, { email, user_not_found: true });
        }
        if (!response.ok) {
            return fail(500, { unknown_error: true });
        }

        const { access_token, user } = await response.json();

        // User is returned as JSON string, parse it
        const userObj = JSON.parse(user);

        // Set cookies
        event.cookies.set('session_id', access_token, {
            path: '/',
            httpOnly: true,
            sameSite: 'lax',
            secure: isProduction,
            maxAge: 60 * 60
        });

        // Optional: store user in a non-httpOnly cookie for client-side access
        event.cookies.set('session_user', JSON.stringify(userObj), {
            path: '/',
            httpOnly: false,
            sameSite: 'lax',
            secure: isProduction,
            maxAge: 60 * 60
        });

        throw redirect(303, '/dashboard');
    }
} satisfies Actions;
