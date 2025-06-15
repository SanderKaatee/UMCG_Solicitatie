<script lang="ts">
  import { onMount } from "svelte";
  import { v4 as uuidv4 } from "uuid";
  import { t } from "$lib/stores/language";

  /** ---- message model ---- */
  interface Message {
    id: string;
    role: "user" | "assistant";
    content: string;
    timestamp: Date;
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
      // Fetch the complete response from the backend
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmedInput }),
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
          <p class="whitespace-pre-wrap">{message.content}</p>
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
</div>
