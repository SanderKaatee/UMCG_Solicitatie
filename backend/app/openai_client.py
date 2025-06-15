# app/openai_client.py
from openai import OpenAI
import yaml
from typing import Dict
from pathlib import Path
from app.config import Config


class OpenAIClient:
    """OpenAI API client built on the v-1 Responses API."""

    def __init__(self):
        # single persistent SDK client (thread-safe per OpenAI docs)
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.system_prompt = self._build_system_prompt()

    # --------------------------------------------------------------------- #
    #  Prompt helpers                                                       #
    # --------------------------------------------------------------------- #
    def _build_system_prompt(self) -> str:
        """
        Build the system prompt by loading it directly from a text file.
        Falls back to a default prompt if the file is not found.
        """
        try:
            # Assumes the file is now named 'system_prompt.txt' for clarity.
            # If you keep the old name, change it back to 'profile.yaml'.
            prompt_file_path = Path(__file__).parent.parent / "static" / "profile_prompt.txt"
            
            with open(prompt_file_path, "r", encoding="utf-8") as f:
                return f.read()

        except FileNotFoundError:
            print(f"Error: Prompt file not found at {prompt_file_path}. Using a default prompt.")
            # A simple, safe fallback prompt
            return "You are a helpful AI assistant for Sander Kaatee. Please be polite and professional."
        except Exception as e:
            print(f"An unexpected error occurred while loading the system prompt: {e}")
            return "You are a helpful AI assistant for Sander Kaatee. Please be polite and professional."
        
    # --------------------------------------------------------------------- #
    #  Public entry-point                                                   #
    # --------------------------------------------------------------------- #
    def get_chat_response(self, message: str) -> str:
        """
        Generate a response from the model.

        The v-1 Responses API uses:
          * `instructions`  – system prompt
          * `input`         – user message(s)
          * `max_output_tokens` instead of `max_tokens`
        """
        try:
            # enforce a hard limit on incoming message size
            trimmed_msg = message[: Config.MAX_MESSAGE_LENGTH]

            response = self.client.responses.create(
                model=Config.OPENAI_MODEL,              # e.g. "gpt-4o", "gpt-4.1"
                instructions=self.system_prompt,
                input=trimmed_msg,
                max_output_tokens=Config.MAX_TOKENS,    # renamed in Responses API
                temperature=Config.TEMPERATURE,
            )

            return response.output_text.strip()

        except Exception as e:
            print(f"OpenAI API error: {e}")
            return (
                "I apologize, but I'm having trouble connecting to the AI "
                "service. Please try again in a moment."
            )
