import { NODE_ENV } from '$env/static/private';
import type { Actions } from './$types';
import { redirect, fail } from '@sveltejs/kit';

const isProduction = NODE_ENV === 'production';

export const actions = {
    login: async (event) => {
        const formData = await event.request.formData();
        const email = formData.get('email');
        const password = formData.get('password');
        event.cookies.delete('session_id', { path: '/' });


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

        if (!response.ok) {
            return fail(400, { email, password_incorrect: true });
        }

        const { access_token } = await response.json();
        event.cookies.set('session_id', access_token, {
            path: '/',
            httpOnly: true,
            sameSite: 'lax',
            secure: isProduction, // Use secure cookies in production
            maxAge: 60 * 60 // 1 hour
        });
        throw redirect(303, '/dashboard');
    }
} satisfies Actions;
