<script lang="ts">
  import { t } from '$lib/stores/language';
</script>

<div class="glass-card p-8 animate-fade-in">
  <h2 class="text-3xl font-bold mb-6">{$t.motivation.title}</h2>
  <div class="prose prose-lg dark:prose-invert max-w-none">
    {#each $t.motivation.content.split('\n\n') as paragraph}
      <p class="mb-4 leading-relaxed">{paragraph}</p>
    {/each}
  </div>
</div>