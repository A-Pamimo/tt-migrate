"""CORS configuration middleware."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.config import settings


def setup_cors(app: FastAPI) -> None:
    """Add CORS middleware to the FastAPI application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
