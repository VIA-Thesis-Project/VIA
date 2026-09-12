"""FastAPI application composition root."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from sqlalchemy import Engine

from via_backend.config import Settings
from via_backend.contexts.farm_management.application import FarmManagementService
from via_backend.contexts.farm_management.infrastructure import (
    InMemoryParcelRepository,
    InMemoryProjectRepository,
    PostgreSQLParcelRepository,
    PostgreSQLProjectRepository,
    create_database,
)
from via_backend.contexts.farm_management.interfaces import create_router
from via_backend.interfaces.http.health import router as health_router


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the VIA API and register its technical interfaces."""
    settings = settings or Settings.from_env()
    engine: Engine | None = None

    if settings.farm_management_repository == "postgresql":
        assert settings.database_url is not None
        engine, sessions = create_database(settings.database_url)
        projects = PostgreSQLProjectRepository(sessions)
        parcels = PostgreSQLParcelRepository(sessions)
    else:
        projects = InMemoryProjectRepository()
        parcels = InMemoryParcelRepository()

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        try:
            yield
        finally:
            if engine is not None:
                engine.dispose()

    application = FastAPI(
        title="VIA Backend", version="0.1.0", lifespan=lifespan
    )
    farm_management = FarmManagementService(
        projects=projects,
        parcels=parcels,
    )
    application.state.settings = settings
    application.include_router(health_router)
    application.include_router(create_router(farm_management))
    return application


app = create_app()
