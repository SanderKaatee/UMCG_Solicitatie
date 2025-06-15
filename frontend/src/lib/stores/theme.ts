// src/lib/stores/theme.ts
import { browser } from '$app/environment';
import { writable } from 'svelte/store';

export type Theme = 'light' | 'dark';

function createThemeStore() {
	const { subscribe, set, update } = writable<Theme>('light');

	return {
		subscribe,
		toggle: () => update(t => (t === 'light' ? 'dark' : 'light')),
		set,
		init: () => {
			if (!browser) return;

			const stored      = localStorage.getItem('theme') as Theme | null;
			const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
			const initial     = stored ?? (prefersDark ? 'dark' : 'light');

			set(initial);
			document.documentElement.classList.toggle('dark', initial === 'dark');

			subscribe(value => {
				localStorage.setItem('theme', value);
				document.documentElement.classList.toggle('dark', value === 'dark');
			});
		}
	};
}

/** The singleton store the rest of the app imports */
export const theme = createThemeStore();
