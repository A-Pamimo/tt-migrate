"""Request/response schemas for the /refactor endpoint."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class LLMProviderEnum(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"


class RefactorRequest(BaseModel):
    """Request body for POST /api/v1/refactor."""

    code: str = Field(..., description="Original PyTorch source code")
    stream: bool = Field(
        default=False, description="Whether to use SSE streaming"
    )
    provider: Optional[LLMProviderEnum] = Field(
        default=None, description="Preferred LLM provider (uses default if not set)"
    )


class RefactorResponse(BaseModel):
    """Response body for POST /api/v1/refactor (non-streaming)."""

    refactored_code: str = Field(..., description="The ttnn-refactored code")
    provider_used: str = Field(..., description="Which LLM provider was used")
    original_code: str = Field(..., description="The original code submitted")
    explanation: Optional[str] = Field(
        default=None, description="Optional explanation of changes made"
    )
