<script lang="ts">
  import { t } from "$lib/stores/language";

  const navItems = [
    { href: "#motivation", label: "motivation" },
    { href: "#chat", label: "chat" },
    { href: "#cv", label: "cv" },
    { href: "#portfolio", label: "portfolio" },
  ];

  let activeSection = "#motivation";

  function handleScroll() {
    const sections = navItems.map((item) => ({
      id: item.href,
      top: document.querySelector(item.href)?.getBoundingClientRect().top ?? 0,
    }));

    const current = sections.reduce((prev, curr) => {
      return Math.abs(curr.top) < Math.abs(prev.top) ? curr : prev;
    });

    activeSection = current.id;
  }
</script>

<svelte:window on:scroll={handleScroll} />

<nav class="flex gap-2">
  {#each navItems as item}
    <a
      href={item.href}
      class="px-4 py-2 rounded-lg transition-all duration-200 {activeSection ===
      item.href
        ? 'bg-primary-500 text-white'
        : 'bg-surface-100 dark:bg-surface-800 hover:bg-surface-200 dark:hover:bg-surface-700'}"
    >
      {$t.nav[item.label]}
    </a>
  {/each}
</nav>
