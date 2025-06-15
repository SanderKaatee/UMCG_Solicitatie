# app/openai_client.py
from openai import OpenAI
import yaml
from typing import Dict, List
from pathlib import Path
from app.config import Config


class OpenAIClient:
    """OpenAI API client with conversation history support."""

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
            prompt_file_path = Path(__file__).parent.parent / "static" / "profile_prompt.txt"
            
            with open(prompt_file_path, "r", encoding="utf-8") as f:
                return f.read()

        except FileNotFoundError:
            print(f"Error: Prompt file not found at {prompt_file_path}. Using a default prompt.")
            return "You are a helpful AI assistant for Sander Kaatee. Please be polite and professional."
        except Exception as e:
            print(f"An unexpected error occurred while loading the system prompt: {e}")
            return "You are a helpful AI assistant for Sander Kaatee. Please be polite and professional."
    
    def _truncate_history(self, history: List[Dict[str, str]], max_messages: int = None) -> List[Dict[str, str]]:
        """
        Truncate conversation history to prevent exceeding context window.
        Keeps the most recent messages while ensuring we stay within limits.
        """
        if max_messages is None:
            max_messages = Config.MAX_CONVERSATION_MESSAGES
        
        # Always keep at least the last few messages for context
        if len(history) > max_messages:
            return history[-max_messages:]
        return history
    
    def _calculate_approximate_tokens(self, messages: List[Dict[str, str]]) -> int:
        """
        Rough approximation of token count (1 token ≈ 4 characters).
        This is a simple heuristic; actual token count may vary.
        """
        total_chars = sum(len(msg.get('content', '')) for msg in messages)
        return total_chars // 4
        
    # --------------------------------------------------------------------- #
    #  Public entry-points                                                  #
    # --------------------------------------------------------------------- #
    def get_chat_response(self, message: str) -> str:
        """
        Generate a response from the model (without history).
        Kept for backward compatibility.
        """
        return self.get_chat_response_with_history(message, [])
    
    def get_chat_response_with_history(self, message: str, history: List[Dict[str, str]]) -> str:
        """
        Generate a response from the model with conversation history.
        
        Args:
            message: The current user message
            history: List of previous messages in format [{"role": "user/assistant", "content": "..."}]
        
        Returns:
            The assistant's response
        """
        try:
            # Enforce a hard limit on incoming message size
            trimmed_msg = message[: Config.MAX_MESSAGE_LENGTH]
            
            # Truncate history to prevent context overflow
            truncated_history = self._truncate_history(history)
            
            # Build messages list for the API
            messages = []
            
            # Add system prompt
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })
            
            # Add conversation history
            for msg in truncated_history:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            
            # Add current message
            messages.append({
                "role": "user",
                "content": trimmed_msg
            })
            
            # Check if we're getting close to context limit
            approx_tokens = self._calculate_approximate_tokens(messages)
            if approx_tokens > Config.MAX_CONTEXT_TOKENS:
                # Remove older messages (keeping system prompt and recent messages)
                while len(messages) > 3 and approx_tokens > Config.MAX_CONTEXT_TOKENS:
                    messages.pop(1)  # Remove oldest non-system message
                    approx_tokens = self._calculate_approximate_tokens(messages)
            
            # Call OpenAI API with the new chat completions format
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages,
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"OpenAI API error: {e}")
            return (
                "I apologize, but I'm having trouble connecting to the AI "
                "service. Please try again in a moment."
            )