<script lang="ts">
  import { onMount } from "svelte";
  import { v4 as uuidv4 } from "uuid";
  import { t } from "$lib/stores/language";
  import { marked } from "marked"; // Add this import

  /** ---- message model ---- */
  interface Message {
    id: string;
    role: "user" | "assistant";
    content: string;
    timestamp: Date;
  }

  /** ---- Configure marked for better formatting ---- */
  marked.setOptions({
    breaks: true, // Convert line breaks to <br>
    gfm: true,    // GitHub Flavored Markdown
  });

  /** ---- Helper function to parse markdown ---- */
  function parseMarkdown(content: string): string {
    return marked(content) as string;
  }

  /** ---- state ---- */
  let messages: Message[] = [];
  let input = "";
  let isLoading = false;
  let messagesContainer: HTMLDivElement;
  let suggestions: string[] = [];
  let showSuggestions = true;

  import { browser } from "$app/environment";
  import { env } from "$env/dynamic/public";

  console.log(
    "Attempting to read env var. Value:",
    env.PUBLIC_API_BASE_URL,
  );

  const API_URL = browser ? `${env.PUBLIC_API_BASE_URL}/api/chat` : "";

  const exampleQuestions = [
    "Why is Sander passionate about working in healthcare?",
    "Tell me about the creation of this AI assistant.",
    "How would Sander learn a new technology stack?",
    'What does "meaningful impact" mean to Sander?',
    "How does Sander's Psychology background influence his work in AI?",
    "What is Sander's greatest strength as a developer?",
    "What did Sander learn from his time as a semi-professional musician?",
    "Describe Sander's process for starting a new AI project.",
    'How does Sander view the role of "failure" in innovation?',
    "What are Sander's long-term career ambitions?",
  ];

  /** ---- Prepare conversation history for API ---- */
  function prepareConversationHistory(): Array<{role: string, content: string}> {
    // Skip the initial welcome message and prepare history for API
    // Limit to last 10 messages to prevent context overflow
    const relevantMessages = messages.slice(1, -1); // Exclude welcome and current message
    const recentMessages = relevantMessages.slice(-10); // Keep last 10 messages
    
    return recentMessages.map(msg => ({
      role: msg.role,
      content: msg.content
    }));
  }

  /** ---- Send user input and get response ---- */
  async function sendMessage() {
    const trimmedInput = input.trim();
    if (!trimmedInput || isLoading) return;

    showSuggestions = false; // Hide suggestions when a message is sent

    // Add user message to the UI
    messages = [
      ...messages,
      {
        id: uuidv4(),
        role: "user",
        content: trimmedInput,
        timestamp: new Date(),
      },
    ];

    input = "";
    isLoading = true;
    scrollToBottom();

    try {
      // Prepare conversation history
      const history = prepareConversationHistory();

      // Fetch the complete response from the backend
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          message: trimmedInput,
          history: history 
        }),
      });

      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }

      const data = await response.json();

      // Add the full assistant message at once
      messages = [
        ...messages,
        {
          id: uuidv4(),
          role: "assistant",
          content: data.content,
          timestamp: new Date(),
        },
      ];
    } catch (error) {
      console.error("Failed to send message:", error);
      messages = [
        ...messages,
        {
          id: uuidv4(),
          role: "assistant",
          content: $t.chat.error, // Your existing error message
          timestamp: new Date(),
        },
      ];
    } finally {
      isLoading = false;
      scrollToBottom();
    }
  }

  /** ---- Handle suggestion click ---- */
  function handleSuggestionClick(question: string) {
    input = question;
    sendMessage();
  }

  /** ---- UI helpers ---- */
  function scrollToBottom() {
    setTimeout(() => {
      if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
      }
    }, 50);
  }

  /** ---- Lifecycle ---- */
  onMount(() => {
    // Select 3 random questions
    const shuffled = [...exampleQuestions].sort(() => 0.5 - Math.random());
    suggestions = shuffled.slice(0, 3);

    // You can add an initial welcome message if you like
    messages = [
      {
        id: uuidv4(),
        role: "assistant",
        content: "Hello! How can I help you learn about Sander Kaatee today?",
        timestamp: new Date(),
      },
    ];
  });
</script>

<div class="glass-card p-6 h-[600px] flex flex-col">
  <h2 class="text-2xl font-bold mb-4">{$t.chat.title}</h2>

  <div
    bind:this={messagesContainer}
    class="flex-1 overflow-y-auto space-y-4 mb-4 scroll-smooth"
  >
    <!-- Messages -->
    {#each messages as message (message.id)}
      <div
        class="animate-slide-in {message.role === 'user'
          ? 'text-right'
          : 'text-left'}"
      >
        <div
          class="inline-block max-w-[80%] {message.role === 'user'
            ? 'bg-primary-500 text-white'
            : 'bg-surface-100 dark:bg-surface-700'} rounded-lg px-4 py-2"
        >
          {#if message.role === 'assistant'}
            <!-- Render assistant messages with markdown support -->
            <div class="prose prose-sm max-w-none dark:prose-invert">
              {@html parseMarkdown(message.content)}
            </div>
          {:else}
            <!-- Render user messages as plain text -->
            <p class="whitespace-pre-wrap">{message.content}</p>
          {/if}
        </div>
      </div>
    {/each}

    <!-- Loading Indicator -->
    {#if isLoading}
      <div class="text-left animate-pulse">
        <div
          class="inline-block bg-surface-100 dark:bg-surface-700 rounded-lg px-4 py-2"
        >
          <p>{$t.chat.thinking}</p>
        </div>
      </div>
    {/if}
  </div>

    <!-- Suggestions Bubbles -->
  {#if showSuggestions && messages.length <= 1}
    <div class="mb-4 flex flex-wrap justify-center gap-2">
      {#each suggestions as question}
        <button
          on:click={() => handleSuggestionClick(question)}
          class="bg-surface-200 dark:bg-surface-600 hover:bg-surface-300 dark:hover:bg-surface-500 text-sm font-medium px-3 py-2 rounded-full transition-colors"
        >
          {question}
        </button>
      {/each}
    </div>
  {/if}

  <form on:submit|preventDefault={sendMessage} class="flex gap-2">
    <input
      bind:value={input}
      type="text"
      placeholder={$t.chat.placeholder}
      disabled={isLoading}
      class="flex-1 px-4 py-2 rounded-lg bg-surface-100 dark:bg-surface-700 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
    />
    <button
      type="submit"
      disabled={isLoading || !input.trim()}
      class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {$t.chat.send}
    </button>
  </form>

  <!-- AI Disclaimer -->
  <div class="mt-3 pt-2 border-t border-surface-200 dark:border-surface-600">
    <p class="text-xs text-surface-500 dark:text-surface-400 text-center leading-relaxed">
      <span class="inline-flex items-center gap-1">
        <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
        </svg>
        <strong>{$t.chat.poweredBy}</strong>
      </span>
      <br>
      {$t.chat.disclaimer}
    </p>
  </div>
</div>

<style>
  /* Custom styles for markdown content */
  :global(.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6) {
    margin-top: 0.5em;
    margin-bottom: 0.5em;
  }
  
  :global(.prose p) {
    margin-top: 0.25em;
    margin-bottom: 0.25em;
  }
  
  :global(.prose ol, .prose ul) {
    margin-top: 0.25em;
    margin-bottom: 0.25em;
    padding-left: 1.5em;
  }
  
  :global(.prose li) {
    margin-top: 0.125em;
    margin-bottom: 0.125em;
  }
  
  :global(.prose strong) {
    font-weight: 600;
  }
  
  :global(.prose em) {
    font-style: italic;
  }
  
  :global(.prose code) {
    background-color: rgba(0, 0, 0, 0.1);
    padding: 0.125em 0.25em;
    border-radius: 0.25em;
    font-size: 0.875em;
  }
  
  :global(.dark .prose code) {
    background-color: rgba(255, 255, 255, 0.1);
  }
</style>