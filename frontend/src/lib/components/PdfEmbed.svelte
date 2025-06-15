<script lang="ts">
  import { language, t } from '$lib/stores/language';
  
  let isLoading = true;
  
  function handleLoad() {
    isLoading = false;
  }
  
  // Reactive statement to determine PDF path based on language
  $: pdfPath = $language === 'en' 
    ? '/Sander_Kaatee___Resume_UMCG_EN.pdf'
    : '/Sander_Kaatee___CV_UMCG.pdf';
  
  // Reactive statement for download filename
  $: downloadFilename = $language === 'en'
    ? 'Sander_Kaatee_Resume_EN.pdf'
    : 'Sander_Kaatee_CV_NL.pdf';
  
  // Reset loading state when language changes
  $: if ($language) {
    isLoading = true;
  }
</script>

<div class="glass-card p-6 h-[800px] flex flex-col">
  <div class="flex justify-between items-center mb-4">
    <h2 class="text-2xl font-bold">{$t.cv.title}</h2>
    <a
      href={pdfPath}
      download={downloadFilename}
      class="btn-primary text-sm"
    >
      {$t.cv.download}
    </a>
  </div>
  
  <div class="flex-1 relative">
    {#if isLoading}
      <div class="absolute inset-0 flex items-center justify-center">
        <p class="text-surface-500 animate-pulse">{$t.cv.loading}</p>
      </div>
    {/if}
    
    <iframe
      src={pdfPath}
      title="CV"
      class="w-full h-full rounded-lg"
      on:load={handleLoad}
    />
  </div>
</div>