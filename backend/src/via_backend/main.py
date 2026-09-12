"""FastAPI application composition root."""

from fastapi import FastAPI

from via_backend.interfaces.http.health import router as health_router


def create_app() -> FastAPI:
    """Build the VIA API and register its technical interfaces."""
    application = FastAPI(title="VIA Backend", version="0.1.0")
    application.include_router(health_router)
    return application


app = create_app()
