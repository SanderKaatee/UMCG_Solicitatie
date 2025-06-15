# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # Rate limiting
    RATE_LIMIT_REQUESTS = 5
    RATE_LIMIT_WINDOW = 60  # seconds
    
    # OpenAI settings
    OPENAI_MODEL = 'gpt-4o-mini'
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    STREAM = True
    
    # Security & Context Management
    MAX_MESSAGE_LENGTH = 1000
    MAX_CONTEXT_LENGTH = 3000  # Deprecated, use MAX_CONTEXT_TOKENS instead
    MAX_CONTEXT_TOKENS = 3500  # Approximate token limit for context
    MAX_CONVERSATION_MESSAGES = 10  # Maximum number of messages to keep in history