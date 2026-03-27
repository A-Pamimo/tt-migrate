"""GET /api/v1/health endpoint."""

from fastapi import APIRouter

from server.config import settings

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """Return basic health status of the API."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "service": settings.APP_NAME,
    }
