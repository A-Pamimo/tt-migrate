"""OpenAI (GPT-4) LLM provider implementation."""

import logging
from typing import AsyncIterator

from server.config import settings
from server.services.llm.base import LLMProvider
from server.services.llm.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """GPT-4-based LLM provider using the OpenAI Python SDK."""

    def __init__(self) -> None:
        self._api_key = settings.OPENAI_API_KEY
        self._model = settings.OPENAI_MODEL

    @property
    def name(self) -> str:
        return "openai"

    async def refactor(self, source_code: str, diagnostics: str, prompt: str) -> str:
        """Generate refactored code via GPT-4."""
        import openai

        client = openai.AsyncOpenAI(api_key=self._api_key)
        response = await client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=4096,
        )
        return response.choices[0].message.content or ""

    async def refactor_stream(
        self, source_code: str, diagnostics: str, prompt: str
    ) -> AsyncIterator[str]:
        """Stream refactored code chunks via GPT-4."""
        import openai

        client = openai.AsyncOpenAI(api_key=self._api_key)
        stream = await client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=4096,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content

    async def health_check(self) -> bool:
        """Check if the OpenAI provider is configured."""
        if not self._api_key:
            return False
        try:
            import openai

            client = openai.AsyncOpenAI(api_key=self._api_key)
            await client.models.list()
            return True
        except Exception:
            logger.warning("OpenAI health check failed", exc_info=True)
            return False
