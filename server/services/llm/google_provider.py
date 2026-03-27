"""Google (Gemini) LLM provider implementation."""

import logging
from typing import AsyncIterator

from server.config import settings
from server.services.llm.base import LLMProvider
from server.services.llm.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class GoogleProvider(LLMProvider):
    """Gemini-based LLM provider using the Google Generative AI SDK."""

    def __init__(self) -> None:
        self._api_key = settings.GOOGLE_API_KEY
        self._model = settings.GOOGLE_MODEL

    @property
    def name(self) -> str:
        return "google"

    async def refactor(self, source_code: str, diagnostics: str, prompt: str) -> str:
        """Generate refactored code via Gemini."""
        if not self._api_key:
            raise ValueError("GOOGLE_API_KEY is not configured.")
        import google.generativeai as genai

        genai.configure(api_key=self._api_key)
        model = genai.GenerativeModel(
            model_name=self._model,
            system_instruction=SYSTEM_PROMPT,
        )
        response = await model.generate_content_async(prompt)
        return response.text or ""

    async def refactor_stream(
        self, source_code: str, diagnostics: str, prompt: str
    ) -> AsyncIterator[str]:
        """Stream refactored code chunks via Gemini."""
        if not self._api_key:
            raise ValueError("GOOGLE_API_KEY is not configured.")
        import google.generativeai as genai

        genai.configure(api_key=self._api_key)
        model = genai.GenerativeModel(
            model_name=self._model,
            system_instruction=SYSTEM_PROMPT,
        )
        response = await model.generate_content_async(prompt, stream=True)
        async for chunk in response:
            if chunk.text:
                yield chunk.text

    async def health_check(self) -> bool:
        """Check if the Google provider is configured."""
        if not self._api_key:
            return False
        try:
            import google.generativeai as genai

            genai.configure(api_key=self._api_key)
            model = genai.GenerativeModel(model_name=self._model)
            # Simple test call
            await model.generate_content_async("test")
            return True
        except Exception:
            logger.warning("Google health check failed", exc_info=True)
            return False
