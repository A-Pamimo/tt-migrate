"""Environment-based configuration using pydantic-settings."""

from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "TT-Migrate API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # LLM Provider Configuration
    LLM_PROVIDER: str = "anthropic"  # anthropic | openai | google
    LLM_FALLBACK_CHAIN: List[str] = ["anthropic", "openai", "google"]

    # API Keys
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None

    # Model names
    ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"
    OPENAI_MODEL: str = "gpt-4"
    GOOGLE_MODEL: str = "gemini-pro"

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 60
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Cache
    LLM_CACHE_MAX_SIZE: int = 128
    LLM_CACHE_TTL_SECONDS: int = 3600

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
