import { browser } from '$app/environment';
import { writable, derived } from 'svelte/store';
import en from '$lib/i18n/en.json';
import nl from '$lib/i18n/nl.json';

type Language = 'en' | 'nl';
type Translations = typeof en;

const translations: Record<Language, Translations> = { en, nl };

function createLanguageStore() {
  const { subscribe, set, update } = writable<Language>('en');

  return {
    subscribe,
    toggle: () => update(l => l === 'en' ? 'nl' : 'en'),
    set,
    init: () => {
      if (browser) {
        const stored = localStorage.getItem('language') as Language;
        const browserLang = navigator.language.startsWith('nl') ? 'nl' : 'en';
        const language = stored || browserLang;
        
        set(language);
        document.documentElement.lang = language;
        
        subscribe(value => {
          localStorage.setItem('language', value);
          document.documentElement.lang = value;
        });
      }
    }
  };
}

export const language = createLanguageStore();
export const t = derived(language, $language => translations[$language]);