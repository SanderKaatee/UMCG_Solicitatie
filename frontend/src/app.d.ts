/// <reference types="@sveltejs/kit" />

declare global {
  namespace App {
    interface Locals {}
    interface PageData {}
    interface Error {}
    interface Platform {}
  }
}

export {};