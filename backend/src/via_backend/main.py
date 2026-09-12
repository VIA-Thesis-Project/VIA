"""FastAPI application composition root."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from sqlalchemy import Engine

from via_backend.config import Settings
from via_backend.contexts.environmental_information.application import (
    EnvironmentalInformationService,
)
from via_backend.contexts.environmental_information.infrastructure import (
    InMemoryDatasetRepository,
    InMemoryDatasetVersionRepository,
    PostgreSQLDatasetRepository,
    PostgreSQLDatasetVersionRepository,
)
from via_backend.contexts.environmental_information.interfaces import (
    create_router as create_environmental_information_router,
)
from via_backend.contexts.farm_management.application import FarmManagementService
from via_backend.contexts.farm_management.infrastructure import (
    InMemoryParcelRepository,
    InMemoryProjectRepository,
    PostgreSQLParcelRepository,
    PostgreSQLProjectRepository,
)
from via_backend.contexts.farm_management.interfaces import (
    create_router as create_farm_management_router,
)
from via_backend.infrastructure import create_database
from via_backend.interfaces.http.health import router as health_router


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the VIA API and register its technical interfaces."""
    settings = settings or Settings.from_env()
    engine: Engine | None = None

    if (
        settings.farm_management_repository == "postgresql"
        or settings.environmental_information_repository == "postgresql"
    ):
        assert settings.database_url is not None
        engine, sessions = create_database(settings.database_url)

    if settings.farm_management_repository == "postgresql":
        assert engine is not None
        projects = PostgreSQLProjectRepository(sessions)
        parcels = PostgreSQLParcelRepository(sessions)
    else:
        projects = InMemoryProjectRepository()
        parcels = InMemoryParcelRepository()

    if settings.environmental_information_repository == "postgresql":
        assert engine is not None
        datasets = PostgreSQLDatasetRepository(sessions)
        dataset_versions = PostgreSQLDatasetVersionRepository(sessions)
    else:
        datasets = InMemoryDatasetRepository()
        dataset_versions = InMemoryDatasetVersionRepository()

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
    environmental_information = EnvironmentalInformationService(
        datasets=datasets,
        versions=dataset_versions,
    )
    application.state.settings = settings
    application.include_router(health_router)
    application.include_router(create_farm_management_router(farm_management))
    application.include_router(
        create_environmental_information_router(environmental_information)
    )
    return application


app = create_app()
