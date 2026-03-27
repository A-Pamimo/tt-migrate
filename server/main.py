"""FastAPI application initialization."""

from fastapi import FastAPI

from server.api.middleware.cors import setup_cors
from server.api.routes import analyze, compatibility, export, health, refactor
from server.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Analyze PyTorch code for compatibility with Tenstorrent's ttnn library.",
)

# Setup CORS middleware
setup_cors(app)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(analyze.router, prefix="/api/v1", tags=["analyze"])
app.include_router(refactor.router, prefix="/api/v1", tags=["refactor"])
app.include_router(export.router, prefix="/api/v1", tags=["export"])
app.include_router(compatibility.router, prefix="/api/v1", tags=["compatibility"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "server.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
