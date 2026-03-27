"""Per-user rate limiting middleware."""

import time
from collections import defaultdict
from typing import Dict, List, Tuple

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from server.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory sliding window rate limiter keyed by client IP."""

    def __init__(self, app: "ASGIApp") -> None:  # noqa: F821
        super().__init__(app)
        # Maps client_key -> list of request timestamps
        self._requests: Dict[str, List[float]] = defaultdict(list)
        self._max_requests = settings.RATE_LIMIT_REQUESTS
        self._window_seconds = settings.RATE_LIMIT_WINDOW_SECONDS

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        client_key = self._get_client_key(request)
        now = time.time()
        cutoff = now - self._window_seconds

        # Prune old entries
        timestamps = self._requests[client_key]
        self._requests[client_key] = [t for t in timestamps if t > cutoff]

        if len(self._requests[client_key]) >= self._max_requests:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "retry_after_seconds": self._window_seconds,
                },
            )

        self._requests[client_key].append(now)
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self._max_requests)
        response.headers["X-RateLimit-Remaining"] = str(
            self._max_requests - len(self._requests[client_key])
        )
        return response

    @staticmethod
    def _get_client_key(request: Request) -> str:
        """Extract a client identifier from the request."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        if request.client:
            return request.client.host
        return "unknown"
