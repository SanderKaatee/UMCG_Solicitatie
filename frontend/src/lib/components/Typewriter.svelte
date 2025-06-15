<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { writable } from 'svelte/store';

  /** Words or sentences you want to cycle through. */
  export let phrases: string[] = [];

  /** Current slice being displayed. */
  const typed = writable('');

  let phraseIndex = 0;

  /** Simple async pause helper. */
  const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

  /** Main loop: type, pause, delete, next phrase. */
  async function typeLoop() {
    while (phrases.length) {
      const text = phrases[phraseIndex];

      // Type forward
      for (let i = 0; i <= text.length; i++) {
        typed.set(text.slice(0, i));
        await tick();
        await sleep(60);
      }

      await sleep(900); // hold

      // Delete backward
      for (let i = text.length; i >= 0; i--) {
        typed.set(text.slice(0, i));
        await tick();
        await sleep(35);
      }

      phraseIndex = (phraseIndex + 1) % phrases.length;
    }
  }

  onMount(typeLoop);
</script>

<!-- Any attributes not exported above (including `class`) land here -->
<p {...$$restProps} aria-live="polite">
  {$typed}<span class="cursor select-none">▋</span>
</p>

<style>
  /* Blinking block cursor */
  .cursor {
    animation: blink 1s steps(1) infinite;
  }
  @keyframes blink {
    0%, 50%   { opacity: 1; }
    50.001%, 100% { opacity: 0; }
  }
</style>
