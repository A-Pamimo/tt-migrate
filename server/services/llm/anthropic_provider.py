"""Anthropic (Claude) LLM provider implementation."""

import logging
from typing import AsyncIterator

from server.config import settings
from server.services.llm.base import LLMProvider
from server.services.llm.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class AnthropicProvider(LLMProvider):
    """Claude-based LLM provider using the Anthropic Python SDK."""

    def __init__(self) -> None:
        self._api_key = settings.ANTHROPIC_API_KEY
        self._model = settings.ANTHROPIC_MODEL

    @property
    def name(self) -> str:
        return "anthropic"

    async def refactor(self, source_code: str, diagnostics: str, prompt: str) -> str:
        """Generate refactored code via Claude."""
        if not self._api_key:
            raise ValueError("ANTHROPIC_API_KEY is not configured.")
        import anthropic

        client = anthropic.AsyncAnthropic(api_key=self._api_key)
        message = await client.messages.create(
            model=self._model,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        # Extract text from the response
        text_blocks = [
            block.text for block in message.content if hasattr(block, "text")
        ]
        return "\n".join(text_blocks)

    async def refactor_stream(
        self, source_code: str, diagnostics: str, prompt: str
    ) -> AsyncIterator[str]:
        """Stream refactored code chunks via Claude."""
        if not self._api_key:
            raise ValueError("ANTHROPIC_API_KEY is not configured.")
        import anthropic

        client = anthropic.AsyncAnthropic(api_key=self._api_key)
        async with client.messages.stream(
            model=self._model,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            async for text in stream.text_stream:
                yield text

    async def health_check(self) -> bool:
        """Check if the Anthropic provider is configured."""
        if not self._api_key:
            return False
        try:
            import anthropic

            client = anthropic.AsyncAnthropic(api_key=self._api_key)
            # A lightweight models list call to verify connectivity
            await client.messages.create(
                model=self._model,
                max_tokens=10,
                messages=[{"role": "user", "content": "hi"}],
            )
            return True
        except Exception:
            logger.warning("Anthropic health check failed", exc_info=True)
            return False
