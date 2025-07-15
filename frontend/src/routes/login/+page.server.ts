import type { Actions } from './$types';

export const actions = {
	login: async (event) => {
        const formData = await event.request.formData();
        const email = formData.get('email');
        const password = formData.get('password');
        console.log('Email:', email, 'Password:', password);
	}
} satisfies Actions;
