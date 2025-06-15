<script lang="ts">
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import { theme } from '$lib/stores/theme';
  import { loadSlim } from '@tsparticles/slim';
  import { particlesInit } from '@tsparticles/svelte';

  // The Svelte wrapper will be loaded only in the browser
  let ParticlesComponent: typeof import('@tsparticles/svelte').default | null = null;

  /* ---------- particles config ---------- */
  function config(dark: boolean) {
    return {
      particles: {
        number: { value: 80, density: { enable: true, area: 800 } },
        color: { value: dark ? '#60a5fa' : '#3b82f6' },
        shape: { type: 'circle' },
        opacity: { value: dark ? 0.6 : 0.5 },
        size: { value: { min: 1, max: 3 } },
        links: {
          enable: true,
          distance: 150,
          color: dark ? '#60a5fa' : '#3b82f6',
          opacity: dark ? 0.4 : 0.2,
          width: 1
        },
        move: {
          enable: true,
          speed: 1,
          outModes: { default: 'out' }
        }
      },
      interactivity: {
        events: {
          onHover: { enable: true, mode: 'grab' },
          onClick: { enable: true, mode: 'repulse' },
          resize: true
        },
        modes: {
          grab: { distance: 150, links: { opacity: 1 } },
          repulse: { distance: 150, duration: 0.5 }
        }
      },
      detectRetina: true,
      background: { color: 'transparent' },
      fullScreen: { enable: false, zIndex: -1 } // Disable fullscreen mode
    };
  }

  /* ---------- mount ---------- */
  onMount(async () => {
    if (!browser) return;

    // tell the wrapper which bundle to use
    await particlesInit(loadSlim);

    // dynamically import the Svelte component (SSR-safe)
    ParticlesComponent = (await import('@tsparticles/svelte')).default;
  });

  /* ---------- reactive options ---------- */
  // whenever the theme store changes, this recomputes
  $: options = config($theme === 'dark');
</script>

{#if ParticlesComponent}
  <div class="particles-container">
    <svelte:component
      this={ParticlesComponent}
      id="hero-particles"
      class="particles-canvas"
      {options}
    />
  </div>
{/if}

<style>
  .particles-container {
    position: absolute;
    inset: 0;
    z-index: 0;
    pointer-events: none;
  }
  
  .particles-container :global(.particles-canvas),
  .particles-container :global(#hero-particles) {
    position: absolute !important;
    width: 100% !important;
    height: 100% !important;
    top: 0 !important;
    left: 0 !important;
    pointer-events: auto;
  }
  
  /* Ensure tsparticles canvas doesn't escape */
  .particles-container :global(#tsparticles),
  .particles-container :global(canvas) {
    position: absolute !important;
    width: 100% !important;
    height: 100% !important;
  }
</style>