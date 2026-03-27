"""In-memory LRU response caching for LLM calls."""

import hashlib
from typing import Optional, Tuple

from cachetools import TTLCache

from server.config import settings

_cache: TTLCache = TTLCache(
    maxsize=settings.LLM_CACHE_MAX_SIZE,
    ttl=settings.LLM_CACHE_TTL_SECONDS,
)


def _make_key(source_code: str, diagnostics: str, provider: str) -> str:
    """Create a deterministic cache key from inputs."""
    raw = f"{provider}::{source_code}::{diagnostics}"
    return hashlib.sha256(raw.encode()).hexdigest()


def get_cached(source_code: str, diagnostics: str, provider: str) -> Optional[str]:
    """Look up a cached refactoring result.

    Returns the cached refactored code string, or None if not cached.
    """
    key = _make_key(source_code, diagnostics, provider)
    return _cache.get(key)


def set_cached(
    source_code: str, diagnostics: str, provider: str, result: str
) -> None:
    """Store a refactoring result in the cache."""
    key = _make_key(source_code, diagnostics, provider)
    _cache[key] = result


def clear_cache() -> None:
    """Clear the entire cache."""
    _cache.clear()
