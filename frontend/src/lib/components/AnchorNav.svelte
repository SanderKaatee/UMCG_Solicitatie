<script lang="ts">
  import { t } from "$lib/stores/language";

  const navItems = [
    { href: "#motivation", label: "motivation" },
    { href: "#chat",        label: "chat" },
    { href: "#cv",          label: "cv" },
    { href: "#portfolio",   label: "portfolio" },
  ];

  let activeSection = "#motivation";

  function handleScroll() {
    const sections = navItems.map(item => ({
      id:  item.href,
      top: document.querySelector(item.href)?.getBoundingClientRect().top ?? 0
    }));
    activeSection = sections.reduce((p,c)=>Math.abs(c.top)<Math.abs(p.top)?c:p).id;
  }
</script>

<!-- Use 'contents' on mobile to participate in parent grid -->
<nav class="contents sm:flex sm:gap-2 sm:whitespace-nowrap">
  {#each navItems as item}
    <a
      href={item.href}
      class="flex items-center justify-center
             px-3 py-2 text-sm leading-tight
             rounded-lg transition-all duration-200
             {activeSection === item.href
               ? 'bg-primary-500 text-white'
               : 'bg-surface-100 dark:bg-surface-800 hover:bg-surface-200 dark:hover:bg-surface-700'}">
      {$t.nav[item.label]}
    </a>
  {/each}
</nav>