<script lang="ts">
  import { language, t } from '$lib/stores/language';
</script>

<button
  on:click={language.toggle}
  class="px-4 py-2 rounded-lg bg-surface-100 dark:bg-surface-800 hover:bg-surface-200 dark:hover:bg-surface-700 transition-colors duration-200 font-medium text-sm"
  aria-label={$t.language.toggle}
>
  {$language === 'en' ? 'NL' : 'EN'}
</button>