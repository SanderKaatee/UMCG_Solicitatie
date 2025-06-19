<script lang="ts">
    import { t } from "$lib/stores/language";

    // Define project metadata separately to keep it DRY
    const projectMetadata = {
        enterprise: [
            {
                tech: ["Python", "Speech Recognition", "NLP"]
            },
            {
                tech: ["LangChain", "RAG", "Vector DB"]
            }
        ],
        public: [
            {
                tech: [
                    "SvelteKit",
                    "Flask",
                    "TypeScript",
                    "OpenAI API",
                    "WebSockets",
                    "Redis",
                    "Docker",
                ],
                github: "https://github.com/SanderKaatee/UMCG_Solicitatie",
                demo: "",
                isCurrent: true,
            },
            {
                tech: ["Python/Flask", "JavaScript", "Canvas API", "Docker"],
                github: "https://github.com/SanderKaatee/trickie",
                demo: "https://trickie.me",
            },
            {
                tech: ["Python", "MoviePy", "dlib", "OpenCV"],
                github: "https://github.com/SanderKaatee/SomethingLikeMeGen",
            },
            {
                tech: [
                    "Python",
                    "GPT-4 Vision",
                    "PyBoy Emulator",
                    "OpenAI API",
                ],
                github: "https://github.com/SanderKaatee/GPT_Pokemon/",
                demo: "",
            },
        ]
    };

    // Reactive statements to merge translations with metadata
    $: enterpriseProjects = $t.portfolio.enterpriseProjects.map((project: any, index: number) => ({
        ...project,
        ...projectMetadata.enterprise[index]
    }));

    $: publicProjects = $t.portfolio.publicProjects.map((project: any, index: number) => ({
        ...project,
        ...projectMetadata.public[index]
    }));
</script>

<div class="space-y-12 animate-fade-in">
    <div class="glass-card p-8">
        <h2 class="text-3xl font-bold mb-8">{$t.portfolio.title}</h2>

        <!-- Enterprise Projects -->
        <div class="mb-12">
            <h3
                class="text-2xl font-semibold mb-6 text-primary-600 dark:text-primary-400"
            >
                {$t.portfolio.enterprise}
            </h3>
            <p class="text-surface-600 dark:text-surface-300 mb-6">
                {$t.portfolio.enterpriseNote}
            </p>
            <div class="grid gap-6">
                {#each enterpriseProjects as project}
                    <div
                        class="bg-surface-100 dark:bg-surface-800 rounded-lg p-6 hover:shadow-lg transition-shadow"
                    >
                        <h4 class="text-xl font-semibold mb-2">
                            {project.name}
                        </h4>
                        <div class="flex flex-wrap gap-2 mb-3">
                            {#each project.tech as tech}
                                <span
                                    class="px-3 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-sm"
                                >
                                    {tech}
                                </span>
                            {/each}
                        </div>
                        <p class="text-surface-600 dark:text-surface-300 mb-3">
                            {project.description}
                        </p>
                        <p
                            class="text-sm font-medium text-primary-600 dark:text-primary-400"
                        >
                        </p>
                    </div>
                {/each}
            </div>
        </div>

        <!-- Competition Achievements -->
        <div class="mb-12">
            <h3
                class="text-2xl font-semibold mb-6 text-primary-600 dark:text-primary-400"
            >
                {$t.portfolio.competitions}
            </h3>
            <div class="grid gap-6">
               {#each $t.portfolio.competitionsList as comp}
                    <div
                        class="bg-gradient-to-r from-primary-50 to-surface-100 dark:from-surface-800 dark:to-surface-700 rounded-lg p-6"
                    >
                        <div class="flex justify-between items-start mb-3">
                            <a
                                href={comp.link}
                                target="_blank"
                                rel="noopener noreferrer"
                                class="text-xl font-semibold hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
                            >
                                {comp.name}
                            </a>
                            <span
                                class="text-sm text-surface-500 dark:text-surface-400"
                                >{comp.period}</span
                            >
                        </div>
                        <div class="mb-3">
                            <span
                                class="inline-flex items-center px-3 py-1 bg-primary-500 text-white rounded-full text-sm font-medium"
                            >
                                🏆 {$t.portfolio.labels.placed} {comp.placement}
                            </span>
                        </div>
                        {#if comp.tech && comp.tech.length > 0}
                            <div class="flex flex-wrap gap-2 mb-3">
                                {#each comp.tech as tech}
                                    <span
                                        class="px-3 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-sm"
                                    >
                                        {tech}
                                    </span>
                                {/each}
                            </div>
                        {/if}
                        <p class="text-surface-600 dark:text-surface-300 mb-3">
                            {comp.description}
                        </p>
                        <a
                            href={comp.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            class="text-primary-600 dark:text-primary-400 hover:underline text-sm font-medium"
                        >
                            {$t.portfolio.labels.viewResults} →
                        </a>
                    </div>
                {/each}
            </div>
        </div>

        <!-- Public Projects -->
        <div>
            <h3
                class="text-2xl font-semibold mb-6 text-primary-600 dark:text-primary-400"
            >
                {$t.portfolio.public}
            </h3>
            <div class="grid gap-6">
                {#each publicProjects as project}
                    <div
                        class="bg-surface-100 dark:bg-surface-800 rounded-lg p-6 hover:shadow-lg transition-shadow {project.isCurrent
                            ? 'ring-2 ring-primary-500 ring-opacity-50 bg-gradient-to-br from-primary-50 via-surface-100 to-surface-100 dark:from-primary-900/20 dark:via-surface-800 dark:to-surface-800'
                            : ''}"
                    >
                        {#if project.isCurrent}
                            <div class="mb-3">
                                <span
                                    class="inline-flex items-center px-3 py-1 bg-primary-500 text-white rounded-full text-sm font-medium animate-pulse"
                                >
                                    ⭐ {$t.portfolio.labels.featuredProject}
                                </span>
                            </div>
                        {/if}

                        <h4
                            class="text-xl font-semibold mb-2 {project.isCurrent
                                ? 'text-primary-700 dark:text-primary-300'
                                : ''}"
                        >
                            {project.name}
                        </h4>

                        {#if project.highlight}
                            <div
                                class="mb-3 p-3 bg-primary-100 dark:bg-primary-900/50 rounded-lg border-l-4 border-primary-500"
                            >
                                <p
                                    class="text-sm font-medium text-primary-700 dark:text-primary-300"
                                >
                                    {project.highlight}
                                </p>
                            </div>
                        {/if}

                        <div class="flex flex-wrap gap-2 mb-3">
                            {#each project.tech as tech}
                                <span
                                    class="px-3 py-1 {project.isCurrent
                                        ? 'bg-primary-200 dark:bg-primary-800 text-primary-800 dark:text-primary-200'
                                        : 'bg-surface-200 dark:bg-surface-700 text-surface-700 dark:text-surface-300'} rounded-full text-sm"
                                >
                                    {tech}
                                </span>
                            {/each}
                        </div>
                        <p class="text-surface-600 dark:text-surface-300 mb-4">
                            {project.description}
                        </p>

                        {#if project.isCurrent && project.keyAchievement}
                            <div
                                class="mb-4 p-3 bg-surface-50 dark:bg-surface-900/50 rounded-lg"
                            >
                                <p
                                    class="text-sm text-surface-600 dark:text-surface-400"
                                >
                                    <strong>{$t.portfolio.labels.keyAchievement}</strong> {project.keyAchievement}
                                </p>
                            </div>
                        {/if}

                        <div class="flex gap-4">
                            <a
                                href={project.github}
                                target="_blank"
                                rel="noopener noreferrer"
                                class="{project.isCurrent
                                    ? 'text-primary-700 dark:text-primary-300'
                                    : 'text-primary-600 dark:text-primary-400'} hover:underline text-sm font-medium flex items-center gap-1"
                            >
                                <svg
                                    class="w-4 h-4"
                                    fill="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"
                                    />
                                </svg>
                                {$t.portfolio.labels.github}
                            </a>
                            {#if project.demo}
                                <a
                                    href={project.demo}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="text-primary-600 dark:text-primary-400 hover:underline text-sm font-medium flex items-center gap-1"
                                >
                                    <svg
                                        class="w-4 h-4"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                                        />
                                    </svg>
                                    {$t.portfolio.labels.liveDemo}
                                </a>
                            {:else if project.isCurrent}
                                <span
                                    class="text-primary-700 dark:text-primary-300 text-sm font-medium flex items-center gap-1"
                                >
                                    <svg
                                        class="w-4 h-4"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                                        />
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                                        />
                                    </svg>
                                    {$t.portfolio.labels.youAreHere}
                                </span>
                            {/if}
                        </div>
                    </div>
                {/each}
            </div>

            <div class="mt-6 p-4 bg-surface-100 dark:bg-surface-800 rounded-lg">
                <p class="text-surface-600 dark:text-surface-300 text-center">
                    {$t.portfolio.moreOnGithub} <a
                        href="https://github.com/SanderKaatee/"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="text-primary-600 dark:text-primary-400 hover:underline font-medium"
                    >
                        {$t.portfolio.githubPortfolioLink}
                    </a>
                </p>
            </div>
        </div>
    </div>
</div>