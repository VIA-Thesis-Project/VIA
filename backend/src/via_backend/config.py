"""Environment-backed configuration for the VIA application host."""

from __future__ import annotations

import os
from dataclasses import dataclass
from math import isfinite
from pathlib import Path
from typing import Literal, cast

RepositoryBackend = Literal["memory", "postgresql"]
CookieSameSite = Literal["lax", "strict", "none"]
ScientificStorageBackend = Literal["filesystem", "s3"]
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_HUAURA_AOI_BOUNDARY_PATH = (
    REPOSITORY_ROOT / "data" / "huaura" / "boundary" / "huaura_province.geojson"
)
DEFAULT_HUAURA_AOI_METADATA_PATH = (
    REPOSITORY_ROOT / "data" / "huaura" / "boundary" / "metadata.json"
)


@dataclass(frozen=True, slots=True)
class Settings:
    """Settings needed by the current backend composition root."""

    farm_management_repository: RepositoryBackend = "memory"
    environmental_information_repository: RepositoryBackend = "memory"
    agroclimatic_evaluation_repository: RepositoryBackend = "memory"
    database_url: str | None = None
    database_transaction_pooler: bool = False
    database_pool_size: int = 5
    database_max_overflow: int = 0
    database_pool_timeout_seconds: int = 30
    database_pool_recycle_seconds: int = 300
    cors_allowed_origins: tuple[str, ...] = ()
    auth_access_token_ttl_seconds: int = 900
    auth_refresh_token_ttl_seconds: int = 1_209_600
    auth_refresh_cookie_name: str = "__Secure-via_refresh"
    auth_refresh_cookie_secure: bool = True
    auth_refresh_cookie_samesite: CookieSameSite = "lax"
    huaura_aoi_boundary_path: Path = DEFAULT_HUAURA_AOI_BOUNDARY_PATH
    huaura_aoi_metadata_path: Path = DEFAULT_HUAURA_AOI_METADATA_PATH
    cropsuite_catalog: Path | None = None
    cropsuite_input_bindings: Path | None = None
    knowledge_source_dir: Path | None = None
    knowledge_manifest: Path | None = None
    knowledge_taxonomy: Path | None = None
    openai_api_key: str | None = None
    openai_embedding_model: str = "text-embedding-3-small"
    openai_embedding_dimensions: int = 1536
    openai_recommendation_model: str = "gpt-5.6-luna"
    rag_embedding_index_version: str = "openai-embedding-v2"
    rag_vector_top_k: int = 10
    rag_lexical_top_k: int = 10
    rag_final_top_k: int = 5
    rate_login_per_minute: int = 5
    rate_refresh_per_minute: int = 10
    rate_dataset_coverage_per_minute: int = 20
    rate_knowledge_per_user_per_minute: int = 30
    rate_recommendations_per_user_per_minute: int = 5
    max_active_evaluations_per_user: int = 2
    daily_evaluation_quota_per_user: int = 20
    daily_recommendation_quota_per_user: int = 10

    def __post_init__(self) -> None:
        selections = {
            "VIA_FARM_MANAGEMENT_REPOSITORY": self.farm_management_repository,
            "VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY": (self.environmental_information_repository),
            "VIA_AGROCLIMATIC_EVALUATION_REPOSITORY": self.agroclimatic_evaluation_repository,
        }
        for setting_name, selection in selections.items():
            if selection not in {"memory", "postgresql"}:
                raise ValueError(f"{setting_name} must be 'memory' or 'postgresql'.")
        if "postgresql" in selections.values() and not self.database_url:
            raise ValueError(
                "VIA_DATABASE_URL is required when PostgreSQL persistence is selected."
            )
        positive_integers = {
            "VIA_AUTH_ACCESS_TOKEN_TTL_SECONDS": self.auth_access_token_ttl_seconds,
            "VIA_AUTH_REFRESH_TOKEN_TTL_SECONDS": self.auth_refresh_token_ttl_seconds,
            "VIA_OPENAI_EMBEDDING_DIMENSIONS": self.openai_embedding_dimensions,
            "VIA_RAG_VECTOR_TOP_K": self.rag_vector_top_k,
            "VIA_RAG_LEXICAL_TOP_K": self.rag_lexical_top_k,
            "VIA_RAG_FINAL_TOP_K": self.rag_final_top_k,
            "VIA_RATE_LOGIN_PER_MINUTE": self.rate_login_per_minute,
            "VIA_RATE_REFRESH_PER_MINUTE": self.rate_refresh_per_minute,
            "VIA_RATE_DATASET_COVERAGE_PER_MINUTE": self.rate_dataset_coverage_per_minute,
            "VIA_RATE_KNOWLEDGE_PER_USER_PER_MINUTE": self.rate_knowledge_per_user_per_minute,
            "VIA_RATE_RECOMMENDATIONS_PER_USER_PER_MINUTE": (
                self.rate_recommendations_per_user_per_minute
            ),
            "VIA_MAX_ACTIVE_EVALUATIONS_PER_USER": self.max_active_evaluations_per_user,
            "VIA_DAILY_EVALUATION_QUOTA_PER_USER": self.daily_evaluation_quota_per_user,
            "VIA_DAILY_RECOMMENDATION_QUOTA_PER_USER": self.daily_recommendation_quota_per_user,
            "VIA_API_DATABASE_POOL_SIZE": self.database_pool_size,
            "VIA_API_DATABASE_POOL_TIMEOUT_SECONDS": self.database_pool_timeout_seconds,
            "VIA_API_DATABASE_POOL_RECYCLE_SECONDS": self.database_pool_recycle_seconds,
        }
        for setting_name, value in positive_integers.items():
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(f"{setting_name} must be a positive integer.")
        if (
            isinstance(self.database_max_overflow, bool)
            or not isinstance(self.database_max_overflow, int)
            or self.database_max_overflow < 0
        ):
            raise ValueError("VIA_API_DATABASE_MAX_OVERFLOW must be a non-negative integer.")
        required_strings = {
            "VIA_OPENAI_EMBEDDING_MODEL": self.openai_embedding_model,
            "VIA_OPENAI_RECOMMENDATION_MODEL": self.openai_recommendation_model,
            "VIA_RAG_EMBEDDING_INDEX_VERSION": self.rag_embedding_index_version,
        }
        for setting_name, value in required_strings.items():
            if not value.strip():
                raise ValueError(f"{setting_name} must be non-empty.")
        for origin in self.cors_allowed_origins:
            if origin == "*":
                raise ValueError("VIA_CORS_ALLOWED_ORIGINS must not contain '*'.")
            if not origin.startswith(("http://", "https://")):
                raise ValueError(
                    "VIA_CORS_ALLOWED_ORIGINS entries must use http:// or https://."
                )
        if not self.auth_refresh_cookie_name or self.auth_refresh_cookie_name != (
            self.auth_refresh_cookie_name.strip()
        ):
            raise ValueError("VIA_AUTH_REFRESH_COOKIE_NAME must be non-empty and trimmed.")
        if (
            self.auth_refresh_cookie_name.startswith("__Secure-")
            and not self.auth_refresh_cookie_secure
        ):
            raise ValueError(
                "VIA_AUTH_REFRESH_COOKIE_SECURE must be true when "
                "VIA_AUTH_REFRESH_COOKIE_NAME uses the __Secure- prefix."
            )
        if self.auth_refresh_cookie_name.startswith("__Host-"):
            if not self.auth_refresh_cookie_secure:
                raise ValueError(
                    "VIA_AUTH_REFRESH_COOKIE_SECURE must be true when "
                    "VIA_AUTH_REFRESH_COOKIE_NAME uses the __Host- prefix."
                )
            raise ValueError(
                "VIA_AUTH_REFRESH_COOKIE_NAME must not use the __Host- prefix while "
                "the refresh cookie Path is /api/v1/auth; __Host- requires Path=/ and "
                "no Domain attribute."
            )
        if self.auth_refresh_cookie_samesite not in {"lax", "strict", "none"}:
            raise ValueError(
                "VIA_AUTH_REFRESH_COOKIE_SAMESITE must be 'lax', 'strict', or 'none'."
            )
        if self.auth_refresh_cookie_samesite == "none" and not self.auth_refresh_cookie_secure:
            raise ValueError(
                "VIA_AUTH_REFRESH_COOKIE_SECURE must be true when SameSite=None."
            )
        if self.auth_refresh_cookie_samesite == "none" and not self.cors_allowed_origins:
            raise ValueError(
                "VIA_CORS_ALLOWED_ORIGINS must contain trusted origins when SameSite=None."
            )

    def require_production(self) -> Settings:
        """Require the durable persistence contract used by the production API."""
        selections = {
            "VIA_FARM_MANAGEMENT_REPOSITORY": self.farm_management_repository,
            "VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY": (
                self.environmental_information_repository
            ),
            "VIA_AGROCLIMATIC_EVALUATION_REPOSITORY": (
                self.agroclimatic_evaluation_repository
            ),
        }
        invalid = [
            f"{setting_name}=postgresql (got {selection!r})"
            for setting_name, selection in selections.items()
            if selection != "postgresql"
        ]
        if invalid:
            raise ValueError(
                "Production API requires PostgreSQL persistence: "
                + ", ".join(invalid)
                + "."
            )
        if not self.database_url:
            raise ValueError("Production API requires a non-empty VIA_DATABASE_URL.")
        return self

    @classmethod
    def from_env(cls) -> Settings:
        database_url = os.getenv("VIA_API_DATABASE_URL") or os.getenv("VIA_DATABASE_URL") or None
        default_backend = "postgresql" if database_url else "memory"
        farm_backend = os.getenv("VIA_FARM_MANAGEMENT_REPOSITORY") or default_backend
        environmental_backend = (
            os.getenv("VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY") or default_backend
        )
        evaluation_backend = os.getenv("VIA_AGROCLIMATIC_EVALUATION_REPOSITORY") or default_backend
        return cls(
            farm_management_repository=cast(RepositoryBackend, farm_backend.casefold()),
            environmental_information_repository=cast(
                RepositoryBackend, environmental_backend.casefold()
            ),
            agroclimatic_evaluation_repository=cast(
                RepositoryBackend, evaluation_backend.casefold()
            ),
            database_url=database_url,
            database_transaction_pooler=_environment_boolean(
                "VIA_API_DATABASE_TRANSACTION_POOLER", False
            ),
            database_pool_size=_environment_integer("VIA_API_DATABASE_POOL_SIZE", 5),
            database_max_overflow=_environment_integer("VIA_API_DATABASE_MAX_OVERFLOW", 0),
            database_pool_timeout_seconds=_environment_integer(
                "VIA_API_DATABASE_POOL_TIMEOUT_SECONDS", 30
            ),
            database_pool_recycle_seconds=_environment_integer(
                "VIA_API_DATABASE_POOL_RECYCLE_SECONDS", 300
            ),
            cors_allowed_origins=_environment_csv("VIA_CORS_ALLOWED_ORIGINS"),
            auth_access_token_ttl_seconds=_environment_integer(
                "VIA_AUTH_ACCESS_TOKEN_TTL_SECONDS", 900
            ),
            auth_refresh_token_ttl_seconds=_environment_integer(
                "VIA_AUTH_REFRESH_TOKEN_TTL_SECONDS", 1_209_600
            ),
            auth_refresh_cookie_name=os.getenv(
                "VIA_AUTH_REFRESH_COOKIE_NAME", "__Secure-via_refresh"
            ),
            auth_refresh_cookie_secure=_environment_boolean("VIA_AUTH_REFRESH_COOKIE_SECURE", True),
            auth_refresh_cookie_samesite=cast(
                CookieSameSite,
                os.getenv("VIA_AUTH_REFRESH_COOKIE_SAMESITE", "lax").casefold(),
            ),
            huaura_aoi_boundary_path=Path(
                os.getenv(
                    "VIA_HUAURA_AOI_BOUNDARY_PATH",
                    str(DEFAULT_HUAURA_AOI_BOUNDARY_PATH),
                )
            ),
            huaura_aoi_metadata_path=Path(
                os.getenv(
                    "VIA_HUAURA_AOI_METADATA_PATH",
                    str(DEFAULT_HUAURA_AOI_METADATA_PATH),
                )
            ),
            cropsuite_catalog=_optional_path("VIA_CROPSUITE_CATALOG"),
            cropsuite_input_bindings=_optional_path("VIA_CROPSUITE_INPUT_BINDINGS"),
            knowledge_source_dir=_optional_path("VIA_KNOWLEDGE_SOURCE_DIR"),
            knowledge_manifest=_optional_path_alias(
                "VIA_KNOWLEDGE_MANIFEST_PATH", "VIA_KNOWLEDGE_MANIFEST"
            ),
            knowledge_taxonomy=_optional_path_alias(
                "VIA_KNOWLEDGE_TAXONOMY_PATH", "VIA_KNOWLEDGE_TAXONOMY"
            ),
            openai_api_key=os.getenv("VIA_OPENAI_API_KEY") or None,
            openai_embedding_model=os.getenv(
                "VIA_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
            ),
            openai_embedding_dimensions=_environment_integer(
                "VIA_OPENAI_EMBEDDING_DIMENSIONS", 1536
            ),
            openai_recommendation_model=os.getenv(
                "VIA_OPENAI_RECOMMENDATION_MODEL", "gpt-5.6-luna"
            ),
            rag_embedding_index_version=os.getenv(
                "VIA_RAG_EMBEDDING_INDEX_VERSION", "openai-embedding-v2"
            ),
            rag_vector_top_k=_environment_integer("VIA_RAG_VECTOR_TOP_K", 10),
            rag_lexical_top_k=_environment_integer("VIA_RAG_LEXICAL_TOP_K", 10),
            rag_final_top_k=_environment_integer("VIA_RAG_FINAL_TOP_K", 5),
            rate_login_per_minute=_environment_integer("VIA_RATE_LOGIN_PER_MINUTE", 5),
            rate_refresh_per_minute=_environment_integer("VIA_RATE_REFRESH_PER_MINUTE", 10),
            rate_dataset_coverage_per_minute=_environment_integer(
                "VIA_RATE_DATASET_COVERAGE_PER_MINUTE", 20
            ),
            rate_knowledge_per_user_per_minute=_environment_integer(
                "VIA_RATE_KNOWLEDGE_PER_USER_PER_MINUTE", 30
            ),
            rate_recommendations_per_user_per_minute=_environment_integer(
                "VIA_RATE_RECOMMENDATIONS_PER_USER_PER_MINUTE", 5
            ),
            max_active_evaluations_per_user=_environment_integer(
                "VIA_MAX_ACTIVE_EVALUATIONS_PER_USER", 2
            ),
            daily_evaluation_quota_per_user=_environment_integer(
                "VIA_DAILY_EVALUATION_QUOTA_PER_USER", 20
            ),
            daily_recommendation_quota_per_user=_environment_integer(
                "VIA_DAILY_RECOMMENDATION_QUOTA_PER_USER", 10
            ),
        )


@dataclass(frozen=True, slots=True)
class WorkerSettings:
    """Settings for the PostgreSQL polling worker process."""

    database_url: str
    database_pool_size: int = 2
    database_max_overflow: int = 0
    database_pool_timeout_seconds: int = 30
    database_pool_recycle_seconds: int = 300
    cropsuite_root: Path | None = None
    cropsuite_python: Path | None = None
    cropsuite_workspace: Path | None = None
    artifacts_root: Path | None = None
    scientific_artifact_backend: ScientificStorageBackend = "filesystem"
    scientific_artifact_bucket: str | None = None
    scientific_artifact_endpoint: str | None = None
    scientific_artifact_region: str = "auto"
    scientific_artifact_access_key_id: str | None = None
    scientific_artifact_secret_access_key: str | None = None
    scientific_source_backend: ScientificStorageBackend | None = None
    scientific_source_dir: Path | None = None
    scientific_source_cache_dir: Path | None = None
    scientific_source_bucket: str | None = None
    scientific_source_endpoint: str | None = None
    scientific_source_region: str = "auto"
    scientific_source_access_key_id: str | None = None
    scientific_source_secret_access_key: str | None = None
    cropsuite_input_bindings: Path | None = None
    cropsuite_source_config: Path | None = None
    cropsuite_catalog: Path | None = None
    poll_interval_seconds: float = 5.0
    batch_size: int = 1
    cropsuite_max_workers: int = 1

    def __post_init__(self) -> None:
        if not self.database_url:
            raise ValueError(
                "VIA_WORKER_DATABASE_URL or VIA_DATABASE_URL is required for the worker."
            )
        for setting_name, value in (
            ("VIA_WORKER_DATABASE_POOL_SIZE", self.database_pool_size),
            (
                "VIA_WORKER_DATABASE_POOL_TIMEOUT_SECONDS",
                self.database_pool_timeout_seconds,
            ),
            (
                "VIA_WORKER_DATABASE_POOL_RECYCLE_SECONDS",
                self.database_pool_recycle_seconds,
            ),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(f"{setting_name} must be a positive integer.")
        if (
            isinstance(self.database_max_overflow, bool)
            or not isinstance(self.database_max_overflow, int)
            or self.database_max_overflow < 0
        ):
            raise ValueError(
                "VIA_WORKER_DATABASE_MAX_OVERFLOW must be a non-negative integer."
            )
        if self.scientific_source_backend not in {None, "filesystem", "s3"}:
            raise ValueError(
                "VIA_SCIENTIFIC_SOURCE_BACKEND must be 'filesystem' or 's3'."
            )
        if self.scientific_artifact_backend not in {"filesystem", "s3"}:
            raise ValueError(
                "VIA_SCIENTIFIC_ARTIFACT_BACKEND must be 'filesystem' or 's3'."
            )
        if self.scientific_source_backend == "filesystem":
            _require_worker_values(
                (
                    ("VIA_SCIENTIFIC_SOURCE_DIR", self.scientific_source_dir),
                    (
                        "VIA_SCIENTIFIC_SOURCE_CACHE_DIR",
                        self.scientific_source_cache_dir,
                    ),
                )
            )
        elif self.scientific_source_backend == "s3":
            _require_worker_values(
                (
                    (
                        "VIA_SCIENTIFIC_SOURCE_CACHE_DIR",
                        self.scientific_source_cache_dir,
                    ),
                    ("VIA_SCIENTIFIC_SOURCE_BUCKET", self.scientific_source_bucket),
                    ("VIA_SCIENTIFIC_SOURCE_ENDPOINT", self.scientific_source_endpoint),
                    (
                        "VIA_SCIENTIFIC_SOURCE_ACCESS_KEY_ID",
                        self.scientific_source_access_key_id,
                    ),
                    (
                        "VIA_SCIENTIFIC_SOURCE_SECRET_ACCESS_KEY",
                        self.scientific_source_secret_access_key,
                    ),
                )
            )
        if self.scientific_artifact_backend == "s3":
            _require_worker_values(
                (
                    ("VIA_SCIENTIFIC_ARTIFACT_BUCKET", self.scientific_artifact_bucket),
                    (
                        "VIA_SCIENTIFIC_ARTIFACT_ENDPOINT",
                        self.scientific_artifact_endpoint,
                    ),
                    (
                        "VIA_SCIENTIFIC_ARTIFACT_ACCESS_KEY_ID",
                        self.scientific_artifact_access_key_id,
                    ),
                    (
                        "VIA_SCIENTIFIC_ARTIFACT_SECRET_ACCESS_KEY",
                        self.scientific_artifact_secret_access_key,
                    ),
                )
            )
        if (
            isinstance(self.poll_interval_seconds, bool)
            or not isinstance(self.poll_interval_seconds, (int, float))
            or not isfinite(self.poll_interval_seconds)
            or self.poll_interval_seconds <= 0
        ):
            raise ValueError("VIA_WORKER_POLL_INTERVAL_SECONDS must be greater than zero.")
        if (
            isinstance(self.batch_size, bool)
            or not isinstance(self.batch_size, int)
            or self.batch_size < 1
        ):
            raise ValueError("VIA_WORKER_BATCH_SIZE must be a positive integer.")
        if (
            isinstance(self.cropsuite_max_workers, bool)
            or not isinstance(self.cropsuite_max_workers, int)
            or self.cropsuite_max_workers < 1
        ):
            raise ValueError("VIA_CROPSUITE_MAX_WORKERS must be a positive integer.")

    def require_scientific_execution(self) -> tuple[Path, Path, Path, Path, Path]:
        missing = [
            name
            for name, value in (
                ("VIA_CROPSUITE_ROOT", self.cropsuite_root),
                ("VIA_CROPSUITE_PYTHON", self.cropsuite_python),
                ("VIA_CROPSUITE_WORKSPACE", self.cropsuite_workspace),
                ("VIA_ARTIFACTS_ROOT", self.artifacts_root),
                ("VIA_CROPSUITE_INPUT_BINDINGS", self.cropsuite_input_bindings),
            )
            if value is None
        ]
        if missing:
            raise ValueError("Worker scientific execution requires " + ", ".join(missing) + ".")
        assert self.cropsuite_root is not None
        assert self.cropsuite_python is not None
        assert self.cropsuite_workspace is not None
        assert self.artifacts_root is not None
        assert self.cropsuite_input_bindings is not None
        _validate_scientific_path_topology(
            cropsuite_root=self.cropsuite_root,
            workspace=self.cropsuite_workspace,
            artifacts_root=self.artifacts_root,
            source_cache=self.scientific_source_cache_dir,
        )
        return (
            self.cropsuite_root,
            self.cropsuite_python,
            self.cropsuite_workspace,
            self.artifacts_root,
            self.cropsuite_input_bindings,
        )

    @classmethod
    def from_env(cls) -> WorkerSettings:
        return cls(
            database_url=(
                os.getenv("VIA_WORKER_DATABASE_URL")
                or os.getenv("VIA_DATABASE_URL")
                or ""
            ),
            database_pool_size=_environment_integer("VIA_WORKER_DATABASE_POOL_SIZE", 2),
            database_max_overflow=_environment_integer(
                "VIA_WORKER_DATABASE_MAX_OVERFLOW", 0
            ),
            database_pool_timeout_seconds=_environment_integer(
                "VIA_WORKER_DATABASE_POOL_TIMEOUT_SECONDS", 30
            ),
            database_pool_recycle_seconds=_environment_integer(
                "VIA_WORKER_DATABASE_POOL_RECYCLE_SECONDS", 300
            ),
            cropsuite_root=_optional_path("VIA_CROPSUITE_ROOT"),
            cropsuite_python=_optional_path("VIA_CROPSUITE_PYTHON"),
            cropsuite_workspace=_optional_path("VIA_CROPSUITE_WORKSPACE"),
            artifacts_root=_optional_path("VIA_ARTIFACTS_ROOT"),
            scientific_artifact_backend=cast(
                ScientificStorageBackend,
                os.getenv("VIA_SCIENTIFIC_ARTIFACT_BACKEND", "filesystem").casefold(),
            ),
            scientific_artifact_bucket=os.getenv("VIA_SCIENTIFIC_ARTIFACT_BUCKET") or None,
            scientific_artifact_endpoint=os.getenv("VIA_SCIENTIFIC_ARTIFACT_ENDPOINT") or None,
            scientific_artifact_region=os.getenv("VIA_SCIENTIFIC_ARTIFACT_REGION", "auto"),
            scientific_artifact_access_key_id=(
                os.getenv("VIA_SCIENTIFIC_ARTIFACT_ACCESS_KEY_ID") or None
            ),
            scientific_artifact_secret_access_key=(
                os.getenv("VIA_SCIENTIFIC_ARTIFACT_SECRET_ACCESS_KEY") or None
            ),
            scientific_source_backend=_optional_scientific_storage_backend(
                "VIA_SCIENTIFIC_SOURCE_BACKEND"
            ),
            scientific_source_dir=_optional_path("VIA_SCIENTIFIC_SOURCE_DIR"),
            scientific_source_cache_dir=_optional_path("VIA_SCIENTIFIC_SOURCE_CACHE_DIR"),
            scientific_source_bucket=os.getenv("VIA_SCIENTIFIC_SOURCE_BUCKET") or None,
            scientific_source_endpoint=os.getenv("VIA_SCIENTIFIC_SOURCE_ENDPOINT") or None,
            scientific_source_region=os.getenv("VIA_SCIENTIFIC_SOURCE_REGION", "auto"),
            scientific_source_access_key_id=(
                os.getenv("VIA_SCIENTIFIC_SOURCE_ACCESS_KEY_ID") or None
            ),
            scientific_source_secret_access_key=(
                os.getenv("VIA_SCIENTIFIC_SOURCE_SECRET_ACCESS_KEY") or None
            ),
            cropsuite_input_bindings=_optional_path("VIA_CROPSUITE_INPUT_BINDINGS"),
            cropsuite_source_config=_optional_path("VIA_CROPSUITE_SOURCE_CONFIG"),
            cropsuite_catalog=_optional_path("VIA_CROPSUITE_CATALOG"),
            poll_interval_seconds=_environment_float("VIA_WORKER_POLL_INTERVAL_SECONDS", 5.0),
            batch_size=_environment_integer("VIA_WORKER_BATCH_SIZE", 1),
            cropsuite_max_workers=_environment_integer("VIA_CROPSUITE_MAX_WORKERS", 1),
        )


def _validate_scientific_path_topology(
    *,
    cropsuite_root: Path,
    workspace: Path,
    artifacts_root: Path,
    source_cache: Path | None = None,
) -> None:
    engine = cropsuite_root.resolve(strict=False)
    execution_workspace = workspace.resolve(strict=False)
    durable_artifacts = artifacts_root.resolve(strict=False)
    scientific_source_cache = (
        source_cache.resolve(strict=False) if source_cache is not None else None
    )

    if _is_same_or_within(execution_workspace, engine):
        raise ValueError("VIA_CROPSUITE_WORKSPACE must be outside VIA_CROPSUITE_ROOT.")
    if _is_same_or_within(durable_artifacts, engine):
        raise ValueError("VIA_ARTIFACTS_ROOT must be outside VIA_CROPSUITE_ROOT.")
    if durable_artifacts == execution_workspace:
        raise ValueError(
            "VIA_ARTIFACTS_ROOT must be distinct from VIA_CROPSUITE_WORKSPACE."
        )
    if _is_same_or_within(durable_artifacts, execution_workspace):
        raise ValueError(
            "VIA_ARTIFACTS_ROOT must not be inside VIA_CROPSUITE_WORKSPACE."
        )
    if scientific_source_cache is not None:
        if _is_same_or_within(scientific_source_cache, engine):
            raise ValueError(
                "VIA_SCIENTIFIC_SOURCE_CACHE_DIR must be outside VIA_CROPSUITE_ROOT."
            )
        if _is_same_or_within(scientific_source_cache, execution_workspace):
            raise ValueError(
                "VIA_SCIENTIFIC_SOURCE_CACHE_DIR must be outside VIA_CROPSUITE_WORKSPACE."
            )


def _is_same_or_within(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def _optional_path(name: str) -> Path | None:
    value = os.getenv(name)
    return Path(value) if value else None


def _optional_path_alias(*names: str) -> Path | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return Path(value)
    return None


def _optional_scientific_storage_backend(name: str) -> ScientificStorageBackend | None:
    value = os.getenv(name)
    if not value:
        return None
    return cast(ScientificStorageBackend, value.casefold())


def _require_worker_values(values: tuple[tuple[str, object | None], ...]) -> None:
    missing = [name for name, value in values if value is None or value == ""]
    if missing:
        raise ValueError("Worker storage configuration requires " + ", ".join(missing) + ".")


def _environment_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError as error:
        raise ValueError(f"{name} must be numeric.") from error


def _environment_integer(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError as error:
        raise ValueError(f"{name} must be an integer.") from error


def _environment_boolean(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    normalized = raw.strip().casefold()
    if normalized in {"true", "1", "yes", "on"}:
        return True
    if normalized in {"false", "0", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean.")


def _environment_csv(name: str) -> tuple[str, ...]:
    raw = os.getenv(name, "")
    values = tuple(item.strip() for item in raw.split(",") if item.strip())
    if len(values) != len(set(values)):
        raise ValueError(f"{name} must not contain duplicate values.")
    return values
