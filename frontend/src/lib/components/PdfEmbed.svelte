<script lang="ts">
  import { language, t } from '$lib/stores/language';
  import { onMount } from 'svelte';
  
  let isLoading = true;
  let iframeElement: HTMLIFrameElement;
  
  function handleLoad() {
    isLoading = false;
    // Debug: log what actually loaded
    if (iframeElement) {
      console.log('Iframe loaded:', iframeElement.src);
      try {
        console.log('Iframe actual URL:', iframeElement.contentWindow?.location.href);
      } catch (e) {
        console.log('Cannot access iframe location (cross-origin)');
      }
    }
  }
  
  // Reactive statement to determine PDF path based on language
  $: pdfPath = $language === 'en' 
    ? '/Sander_Kaatee___Resume_UMCG_EN.pdf'
    : '/Sander_Kaatee___CV_UMCG.pdf';
  
  // Reactive statement for download filename
  $: downloadFilename = $language === 'en'
    ? 'Sander_Kaatee_Resume_EN.pdf'
    : 'Sander_Kaatee_CV_NL.pdf';
  
  // Debug: log when language or path changes
  $: console.log('Language:', $language, 'PDF Path:', pdfPath);
  
  // Reset loading state when language changes
  $: if ($language) {
    isLoading = true;
  }
  
  onMount(() => {
    console.log('PdfEmbed mounted, initial language:', $language);
  });
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
    
    <!-- Only render iframe if we have a valid path -->
    {#if pdfPath}
      <iframe
        bind:this={iframeElement}
        src={pdfPath}
        title="CV"
        class="w-full h-full rounded-lg"
        on:load={handleLoad}
        on:error={(e) => console.error('Iframe error:', e)}
      />
    {:else}
      <div class="absolute inset-0 flex items-center justify-center">
        <p class="text-surface-500">PDF path not set</p>
      </div>
    {/if}
  </div>
</div>