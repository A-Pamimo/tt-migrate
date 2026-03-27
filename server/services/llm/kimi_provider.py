"""KIMI (Moonshot AI) LLM provider implementation.

KIMI exposes an OpenAI-compatible chat-completions endpoint, so we reuse the
``openai`` SDK and simply point it at the Moonshot base URL.
"""

import logging
from typing import AsyncIterator

from server.config import settings
from server.services.llm.base import LLMProvider
from server.services.llm.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

_KIMI_BASE_URL = "https://api.moonshot.cn/v1"


class KimiProvider(LLMProvider):
    """Moonshot-AI KIMI provider using the OpenAI-compatible SDK."""

    def __init__(self) -> None:
        self._api_key = settings.KIMI_API_KEY
        self._model = settings.KIMI_MODEL

    @property
    def name(self) -> str:
        return "kimi"

    def _get_client(self):  # type: ignore[return]
        """Return an async OpenAI client pointed at the KIMI endpoint."""
        import openai

        return openai.AsyncOpenAI(
            api_key=self._api_key,
            base_url=_KIMI_BASE_URL,
        )

    async def refactor(self, source_code: str, diagnostics: str, prompt: str) -> str:
        """Generate refactored code via KIMI."""
        if not self._api_key:
            raise ValueError("KIMI_API_KEY is not configured.")

        client = self._get_client()
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
        """Stream refactored code chunks via KIMI."""
        if not self._api_key:
            raise ValueError("KIMI_API_KEY is not configured.")

        client = self._get_client()
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
        """Check if the KIMI provider is configured and reachable."""
        if not self._api_key:
            return False
        try:
            client = self._get_client()
            await client.models.list()
            return True
        except Exception:
            logger.warning("KIMI health check failed", exc_info=True)
            return False
