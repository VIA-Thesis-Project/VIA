"""Side-effect-free FastAPI application composition."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Engine

from via_backend.config import Settings
from via_backend.contexts.agroclimatic_evaluation.application import (
    AgroclimaticEvaluationService,
    EvaluationCapabilitiesService,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    FilesystemCropCapabilityCatalog,
    FilesystemScientificInputBindingCatalog,
    InMemoryEvaluationRepository,
    PostgreSQLEvaluationRepository,
)
from via_backend.contexts.agroclimatic_evaluation.interfaces import (
    create_capabilities_router,
)
from via_backend.contexts.agroclimatic_evaluation.interfaces import (
    create_router as create_agroclimatic_evaluation_router,
)
from via_backend.contexts.decision_support.application.knowledge_services import (
    HybridKnowledgeRetriever,
    RecommendationApplicationService,
    RecommendationContextBuilder,
    configured_embedding_index,
)
from via_backend.contexts.decision_support.infrastructure import (
    OpenAIEmbeddingProvider,
    OpenAIRecommendationGenerator,
    PostgreSQLKnowledgeCorpusRepository,
    PostgreSQLRecommendationRepository,
    YamlFilesystemKnowledgeSourceCatalog,
    load_taxonomy,
)
from via_backend.contexts.decision_support.interfaces import (
    create_router as create_decision_support_router,
)
from via_backend.contexts.environmental_information.application import (
    EnvironmentalInformationService,
)
from via_backend.contexts.environmental_information.infrastructure import (
    InMemoryDatasetRepository,
    InMemoryDatasetVersionRepository,
    PostGISCoverageCalculator,
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
from via_backend.contexts.identity_access.application import AuthenticationService
from via_backend.contexts.identity_access.infrastructure import (
    Argon2PasswordHasher,
    InMemoryAuthSessionRepository,
    InMemoryUserRepository,
    PostgreSQLAuthSessionRepository,
    PostgreSQLUserRepository,
    SecretsOpaqueTokenGenerator,
    Sha256TokenHasher,
    SystemClock,
)
from via_backend.contexts.identity_access.interfaces import (
    AuthHttpSettings,
)
from via_backend.contexts.identity_access.interfaces import (
    create_router as create_identity_access_router,
)
from via_backend.infrastructure import SessionFactory, create_database
from via_backend.interfaces.http.health import router as health_router


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the VIA API and register its technical interfaces."""
    settings = settings or Settings.from_env()
    engine: Engine | None = None
    sessions: SessionFactory | None = None

    if (
        settings.farm_management_repository == "postgresql"
        or settings.environmental_information_repository == "postgresql"
        or settings.agroclimatic_evaluation_repository == "postgresql"
    ):
        assert settings.database_url is not None
        engine, sessions = create_database(settings.database_url)

    if settings.farm_management_repository == "postgresql":
        assert engine is not None
        assert sessions is not None
        projects = PostgreSQLProjectRepository(sessions)
        parcels = PostgreSQLParcelRepository(sessions)
    else:
        projects = InMemoryProjectRepository()
        parcels = InMemoryParcelRepository()

    if settings.environmental_information_repository == "postgresql":
        assert engine is not None
        assert sessions is not None
        datasets = PostgreSQLDatasetRepository(sessions)
        dataset_versions = PostgreSQLDatasetVersionRepository(sessions)
        coverage = PostGISCoverageCalculator(sessions)
    else:
        datasets = InMemoryDatasetRepository()
        dataset_versions = InMemoryDatasetVersionRepository()
        coverage = None

    if settings.agroclimatic_evaluation_repository == "postgresql":
        assert engine is not None
        assert sessions is not None
        evaluations = PostgreSQLEvaluationRepository(sessions)
    else:
        evaluations = InMemoryEvaluationRepository()

    if sessions is not None:
        identity_users = PostgreSQLUserRepository(sessions)
        auth_sessions = PostgreSQLAuthSessionRepository(sessions)
    else:
        identity_users = InMemoryUserRepository()
        auth_sessions = InMemoryAuthSessionRepository()

    authentication = AuthenticationService(
        users=identity_users,
        sessions=auth_sessions,
        password_hasher=Argon2PasswordHasher(),
        token_generator=SecretsOpaqueTokenGenerator(),
        token_hasher=Sha256TokenHasher(),
        clock=SystemClock(),
        access_token_ttl_seconds=settings.auth_access_token_ttl_seconds,
        refresh_token_ttl_seconds=settings.auth_refresh_token_ttl_seconds,
    )

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
    if settings.cors_allowed_origins:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=list(settings.cors_allowed_origins),
            allow_credentials=True,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["Content-Type", "Authorization"],
        )
    farm_management = FarmManagementService(
        projects=projects,
        parcels=parcels,
    )
    environmental_information = EnvironmentalInformationService(
        datasets=datasets,
        versions=dataset_versions,
        coverage=coverage,
    )
    agroclimatic_evaluation = AgroclimaticEvaluationService(
        evaluations=evaluations
    )
    application.state.settings = settings
    application.include_router(health_router)
    application.include_router(
        create_identity_access_router(
            authentication,
            AuthHttpSettings(
                refresh_cookie_name=settings.auth_refresh_cookie_name,
                refresh_cookie_secure=settings.auth_refresh_cookie_secure,
                refresh_cookie_samesite=settings.auth_refresh_cookie_samesite,
                trusted_origins=settings.cors_allowed_origins,
            ),
        ),
        prefix="/api/v1",
    )
    application.include_router(create_farm_management_router(farm_management))
    application.include_router(
        create_environmental_information_router(environmental_information)
    )
    application.include_router(
        create_agroclimatic_evaluation_router(agroclimatic_evaluation),
        prefix="/api/v1",
    )
    capability_catalog = (
        FilesystemCropCapabilityCatalog(settings.cropsuite_catalog)
        if settings.cropsuite_catalog is not None
        else None
    )
    scientific_input_binding_catalog = (
        FilesystemScientificInputBindingCatalog(
            settings.cropsuite_input_bindings
        )
        if settings.cropsuite_input_bindings is not None
        else None
    )
    application.include_router(
        create_capabilities_router(
            EvaluationCapabilitiesService(
                capability_catalog,
                scientific_input_binding_catalog,
            )
        ),
        prefix="/api/v1",
    )
    if sessions is not None:
        knowledge_catalog = YamlFilesystemKnowledgeSourceCatalog(
            settings.knowledge_manifest,
            settings.knowledge_source_dir,
        )
        corpus_manifest = knowledge_catalog.load_manifest()
        taxonomy = load_taxonomy(settings.knowledge_taxonomy)
        embedding_provider = OpenAIEmbeddingProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_embedding_model,
            dimensions=settings.openai_embedding_dimensions,
        )
        knowledge_repository = PostgreSQLKnowledgeCorpusRepository(sessions)
        retriever = HybridKnowledgeRetriever(
            repository=knowledge_repository,
            embeddings=embedding_provider,
            taxonomy=taxonomy,
            embedding_index=configured_embedding_index(
                embedding_provider,
                settings.rag_embedding_index_version,
            ),
            corpus_version=corpus_manifest.corpus_version,
            vector_top_k=settings.rag_vector_top_k,
            lexical_top_k=settings.rag_lexical_top_k,
            final_top_k=settings.rag_final_top_k,
        )
        recommendation_service = RecommendationApplicationService(
            retriever=retriever,
            generator=OpenAIRecommendationGenerator(
                api_key=settings.openai_api_key,
                model=settings.openai_recommendation_model,
            ),
            repository=PostgreSQLRecommendationRepository(sessions),
        )
        application.include_router(
            create_decision_support_router(
                RecommendationContextBuilder(agroclimatic_evaluation),
                recommendation_service,
            ),
            prefix="/api/v1",
        )
    return application


def create_production_app() -> FastAPI:
    """Build the production API after enforcing durable persistence settings."""
    settings = Settings.from_env().require_production()
    return create_app(settings)
