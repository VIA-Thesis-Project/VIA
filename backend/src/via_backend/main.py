"""FastAPI application composition root."""

from fastapi import FastAPI

from via_backend.contexts.farm_management.application import FarmManagementService
from via_backend.contexts.farm_management.infrastructure import (
    InMemoryParcelRepository,
    InMemoryProjectRepository,
)
from via_backend.contexts.farm_management.interfaces import create_router
from via_backend.interfaces.http.health import router as health_router


def create_app() -> FastAPI:
    """Build the VIA API and register its technical interfaces."""
    application = FastAPI(title="VIA Backend", version="0.1.0")
    farm_management = FarmManagementService(
        projects=InMemoryProjectRepository(),
        parcels=InMemoryParcelRepository(),
    )
    application.include_router(health_router)
    application.include_router(create_router(farm_management))
    return application


app = create_app()
