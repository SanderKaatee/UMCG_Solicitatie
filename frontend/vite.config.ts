import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    port: 3000,
    host: '0.0.0.0'
  },
  ssr: {
    noExternal: ['@tsparticles/engine', '@tsparticles/slim', '@tsparticles/svelte']
  }
});
