"""Abstract LLM provider interface."""

from abc import ABC, abstractmethod
from typing import AsyncIterator


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def refactor(self, source_code: str, diagnostics: str, prompt: str) -> str:
        """Generate refactored code in a single response.

        Args:
            source_code: The original PyTorch source code.
            diagnostics: JSON-serialized diagnostics from the analyzer.
            prompt: The fully assembled prompt.

        Returns:
            The refactored code as a string.
        """
        ...

    @abstractmethod
    async def refactor_stream(
        self, source_code: str, diagnostics: str, prompt: str
    ) -> AsyncIterator[str]:
        """Generate refactored code as a stream of chunks.

        Args:
            source_code: The original PyTorch source code.
            diagnostics: JSON-serialized diagnostics from the analyzer.
            prompt: The fully assembled prompt.

        Yields:
            Chunks of the refactored code.
        """
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is available and configured.

        Returns:
            True if the provider is ready, False otherwise.
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name."""
        ...
