"""Environment-backed configuration for the VIA application host."""

from __future__ import annotations

import os
from dataclasses import dataclass
from math import isfinite
from pathlib import Path
from typing import Literal, cast

RepositoryBackend = Literal["memory", "postgresql"]


@dataclass(frozen=True, slots=True)
class Settings:
    """Settings needed by the current backend composition root."""

    farm_management_repository: RepositoryBackend = "memory"
    environmental_information_repository: RepositoryBackend = "memory"
    agroclimatic_evaluation_repository: RepositoryBackend = "memory"
    database_url: str | None = None
    cors_allowed_origins: tuple[str, ...] = ()
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
            "VIA_OPENAI_EMBEDDING_DIMENSIONS": self.openai_embedding_dimensions,
            "VIA_RAG_VECTOR_TOP_K": self.rag_vector_top_k,
            "VIA_RAG_LEXICAL_TOP_K": self.rag_lexical_top_k,
            "VIA_RAG_FINAL_TOP_K": self.rag_final_top_k,
        }
        for setting_name, value in positive_integers.items():
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(f"{setting_name} must be a positive integer.")
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
        database_url = os.getenv("VIA_DATABASE_URL") or None
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
            cors_allowed_origins=_environment_csv("VIA_CORS_ALLOWED_ORIGINS"),
            cropsuite_catalog=_optional_path("VIA_CROPSUITE_CATALOG"),
            cropsuite_input_bindings=_optional_path(
                "VIA_CROPSUITE_INPUT_BINDINGS"
            ),
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
        )


@dataclass(frozen=True, slots=True)
class WorkerSettings:
    """Settings for the PostgreSQL polling worker process."""

    database_url: str
    cropsuite_root: Path | None = None
    cropsuite_python: Path | None = None
    cropsuite_workspace: Path | None = None
    artifacts_root: Path | None = None
    cropsuite_input_bindings: Path | None = None
    cropsuite_source_config: Path | None = None
    cropsuite_catalog: Path | None = None
    poll_interval_seconds: float = 5.0
    batch_size: int = 1
    cropsuite_max_workers: int = 1

    def __post_init__(self) -> None:
        if not self.database_url:
            raise ValueError("VIA_DATABASE_URL is required for the worker.")
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
            database_url=os.getenv("VIA_DATABASE_URL") or "",
            cropsuite_root=_optional_path("VIA_CROPSUITE_ROOT"),
            cropsuite_python=_optional_path("VIA_CROPSUITE_PYTHON"),
            cropsuite_workspace=_optional_path("VIA_CROPSUITE_WORKSPACE"),
            artifacts_root=_optional_path("VIA_ARTIFACTS_ROOT"),
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
) -> None:
    engine = cropsuite_root.resolve(strict=False)
    execution_workspace = workspace.resolve(strict=False)
    durable_artifacts = artifacts_root.resolve(strict=False)

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


def _environment_csv(name: str) -> tuple[str, ...]:
    raw = os.getenv(name, "")
    values = tuple(item.strip() for item in raw.split(",") if item.strip())
    if len(values) != len(set(values)):
        raise ValueError(f"{name} must not contain duplicate values.")
    return values
