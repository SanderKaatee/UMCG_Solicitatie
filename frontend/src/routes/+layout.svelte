<script lang="ts">
  import "../app.css";
  import { onMount } from "svelte";
  import { theme } from "$lib/stores/theme";
  import { language, t } from "$lib/stores/language";
  import ThemeToggle from "$lib/components/ThemeToggle.svelte";
  import LanguageToggle from "$lib/components/LanguageToggle.svelte";
  import AnchorNav from "$lib/components/AnchorNav.svelte";
  import Typewriter from "$lib/components/Typewriter.svelte";
  import Particles from "$lib/components/Particles.svelte";

  onMount(() => {
    theme.init();
    language.init();
  });
</script>

<div class="min-h-screen">
  <!-- Header -->
  <header
    class="sticky top-0 z-50 bg-white/80 dark:bg-surface-900/80 backdrop-blur-md border-b border-surface-200 dark:border-surface-700"
  >
    <div class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-8">
          <a href="/" class="text-2xl font-bold text-primary-500">SK</a>
          <AnchorNav />
        </div>

        <div class="flex items-center gap-2">
          <LanguageToggle />
          <ThemeToggle />
        </div>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section
    class="border-b border-surface-200 dark:border-surface-700"
  >
    <div
      class="relative overflow-hidden bg-gradient-to-br from-primary-50 to-surface-100 dark:from-surface-900 dark:to-surface-800"
    >
      <!-- Particles are mounted here, contained within this relative div -->
      <Particles />
      
      <!-- Grid pattern on top of particles -->
      <div class="absolute inset-0 bg-grid-pattern opacity-5 pointer-events-none"></div>
      
      <!-- Hero content with higher z-index -->
      <div class="container mx-auto px-4 py-20 relative z-20">
        <div class="text-center animate-fade-in">
          <h1
            class="text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-primary-500 to-primary-700 dark:from-primary-400 dark:to-primary-600 bg-clip-text text-transparent"
          >
            {$t.hero.title}
          </h1>

          <Typewriter
            phrases={$t.hero.subtitleCycle}
            class="text-xl md:text-2xl text-surface-600 dark:text-surface-300 mb-8"
          />

          <a href="#chat" class="btn-primary inline-flex items-center gap-2">
            {$t.hero.cta}
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
              />
            </svg>
          </a>
        </div>
      </div>
    </div>
  </section>


  <!-- Main Content -->
  <main class="container mx-auto px-4 md:px-16 lg:px-48 xl:px-64 2xl:px-80 py-8">
    <slot />
  </main>

  <!-- Footer -->
  <footer class="mt-20 border-t border-surface-200 dark:border-surface-700">
    <div class="container mx-auto px-4 py-8">
      <p class="text-center text-surface-500 dark:text-surface-400">
        © 2025 Sander Kaatee. Built with SvelteKit & Flask.
      </p>
    </div>
  </footer>
</div>

<style>
  .bg-grid-pattern {
    background-image: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 40px,
        currentColor 40px,
        currentColor 41px
      ),
      repeating-linear-gradient(
        90deg,
        transparent,
        transparent 40px,
        currentColor 40px,
        currentColor 41px
      );
  }
</style>