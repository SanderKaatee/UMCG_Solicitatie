<script lang="ts">
  import ChatPanel from '$lib/components/ChatPanel.svelte';
  import MotivationLetter from '$lib/components/MotivationLetter.svelte';
  import PdfEmbed from '$lib/components/PdfEmbed.svelte';
  import Portfolio from '$lib/components/Portfolio.svelte';
</script>

<svelte:head>
  <title>Sander Kaatee - Solicitatie UMCG</title>
  <meta name="description" content="Job Application by Sander Kaatee for the UMCG" />
</svelte:head>

<div class="space-y-20">

  <!-- Motivation Section -->
  <section id="motivation" class="scroll-mt-20">
    <MotivationLetter />
  </section>

  <!-- Chat Section -->
  <section id="chat" class="scroll-mt-20">
    <ChatPanel />
  </section>
  
  <!-- CV Section -->
  <section id="cv" class="scroll-mt-20">
    <PdfEmbed />
  </section>

  <!-- Porfolio Section -->
  <section id="portfolio" class="scroll-mt-20">
    <Portfolio />
  </section>
</div>