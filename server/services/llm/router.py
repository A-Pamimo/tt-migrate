"""LLM provider selection and fallback logic."""

import logging
from typing import AsyncIterator, Dict, Optional, Tuple

from server.config import settings
from server.services.llm.anthropic_provider import AnthropicProvider
from server.services.llm.base import LLMProvider
from server.services.llm.cache import get_cached, set_cached
from server.services.llm.google_provider import GoogleProvider
from server.services.llm.openai_provider import OpenAIProvider
from server.services.llm.prompts import build_refactor_prompt

logger = logging.getLogger(__name__)


class LLMRouter:
    """Routes LLM requests to providers with fallback support."""

    def __init__(self) -> None:
        self._providers: Dict[str, LLMProvider] = {
            "anthropic": AnthropicProvider(),
            "openai": OpenAIProvider(),
            "google": GoogleProvider(),
        }
        self._fallback_chain = settings.LLM_FALLBACK_CHAIN
        self._default_provider = settings.LLM_PROVIDER

    def get_provider(self, name: str) -> Optional[LLMProvider]:
        """Get a specific provider by name."""
        return self._providers.get(name)

    async def refactor(
        self,
        source_code: str,
        diagnostics: str,
        provider_name: Optional[str] = None,
    ) -> Tuple[str, str]:
        """Refactor code using the specified or default provider, with fallback.

        Returns:
            A tuple of (refactored_code, provider_name_used).
        """
        prompt = build_refactor_prompt(source_code, diagnostics)
        providers_to_try = self._get_provider_order(provider_name)

        for pname in providers_to_try:
            provider = self._providers.get(pname)
            if provider is None:
                continue

            # Check cache first
            cached = get_cached(source_code, diagnostics, pname)
            if cached is not None:
                logger.info("Cache hit for provider %s", pname)
                return cached, pname

            try:
                result = await provider.refactor(source_code, diagnostics, prompt)
                set_cached(source_code, diagnostics, pname, result)
                return result, pname
            except Exception:
                logger.warning(
                    "Provider %s failed, trying next in chain", pname, exc_info=True
                )
                continue

        raise RuntimeError(
            "All LLM providers failed. Tried: " + ", ".join(providers_to_try)
        )

    async def refactor_stream(
        self,
        source_code: str,
        diagnostics: str,
        provider_name: Optional[str] = None,
    ) -> AsyncIterator[Tuple[str, str]]:
        """Stream refactored code using the specified or default provider with fallback.

        Yields:
            Tuples of (chunk, provider_name_used).
        """
        prompt = build_refactor_prompt(source_code, diagnostics)
        providers_to_try = self._get_provider_order(provider_name)

        last_error: Optional[Exception] = None
        for pname in providers_to_try:
            provider = self._providers.get(pname)
            if provider is None:
                continue
            try:
                async for chunk in provider.refactor_stream(
                    source_code, diagnostics, prompt
                ):
                    yield chunk, pname
                return  # Success
            except Exception as exc:
                logger.warning(
                    "Streaming from %s failed, trying next", pname, exc_info=True
                )
                last_error = exc
                continue

        raise RuntimeError(
            f"All LLM providers failed for streaming. Last error: {last_error}"
        )

    def _get_provider_order(self, preferred: Optional[str] = None) -> list:
        """Build the ordered list of providers to try."""
        if preferred:
            # Put preferred first, then fallback chain (excluding preferred)
            order = [preferred] + [
                p for p in self._fallback_chain if p != preferred
            ]
        else:
            # Default provider first, then rest of fallback chain
            order = [self._default_provider] + [
                p for p in self._fallback_chain if p != self._default_provider
            ]
        return order


# Singleton instance
_router_instance: Optional[LLMRouter] = None


def get_llm_router() -> LLMRouter:
    """Get or create the singleton LLMRouter instance."""
    global _router_instance
    if _router_instance is None:
        _router_instance = LLMRouter()
    return _router_instance
