"""YAML-backed corpus and taxonomy adapters."""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path
from typing import Any

import yaml

from ..application.knowledge_models import CorpusManifest, CorpusSource
from ..application.knowledge_services import Taxonomy


class ManifestValidationError(ValueError):
    """Raised when repository-owned declarative knowledge config is invalid."""


class YamlFilesystemKnowledgeSourceCatalog:
    def __init__(
        self,
        manifest_path: Path | None = None,
        source_dir: Path | None = None,
    ) -> None:
        self._manifest_path = manifest_path
        self._source_dir = source_dir

    def load_manifest(self) -> CorpusManifest:
        data = _load_yaml_mapping(self._manifest_path, "corpus.yaml")
        raw_sources = data.get("sources")
        if not isinstance(raw_sources, list) or not raw_sources:
            raise ManifestValidationError("corpus.yaml must contain a non-empty sources list.")
        sources = tuple(_parse_source(item) for item in raw_sources)
        source_ids = tuple(source.source_id for source in sources)
        if len(source_ids) != len(set(source_ids)):
            raise ManifestValidationError("corpus source_id values must be unique.")
        return CorpusManifest(
            corpus_version=_required_string(data, "corpus_version"),
            sources=sources,
        )

    def read_source(self, source: CorpusSource) -> bytes:
        if self._source_dir is None:
            raise RuntimeError(
                "VIA_KNOWLEDGE_SOURCE_DIR is required to read external knowledge sources."
            )
        relative = Path(source.relative_path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ManifestValidationError("Knowledge relative_path must stay below source dir.")
        root = self._source_dir.resolve(strict=False)
        resolved = (root / relative).resolve(strict=False)
        if resolved != root and root not in resolved.parents:
            raise ManifestValidationError(
                "Knowledge source resolves outside configured source dir."
            )
        return resolved.read_bytes()


def load_taxonomy(path: Path | None = None) -> Taxonomy:
    data = _load_yaml_mapping(path, "taxonomy.yaml")
    return Taxonomy(
        version=_required_string(data, "taxonomy_version"),
        factors=_term_mapping(data.get("factors"), "factors"),
        crops=_term_mapping(data.get("crops", {}), "crops"),
        water_regimes=_term_mapping(data.get("water_regimes", {}), "water_regimes"),
    )


def _parse_source(value: object) -> CorpusSource:
    if not isinstance(value, dict):
        raise ManifestValidationError("Each corpus source must be a mapping.")
    data: dict[str, Any] = value
    roles_value = data.get("source_roles", data.get("source_role"))
    roles = (
        (roles_value.strip(),)
        if isinstance(roles_value, str)
        else _string_tuple(roles_value, "source_roles")
    )
    if not roles or any(not role for role in roles):
        raise ManifestValidationError("Every source must declare at least one source role.")
    source_type = _required_string(data, "source_type").casefold()
    if source_type != "pdf":
        raise ManifestValidationError(f"Unsupported source_type {source_type!r}.")
    relative_path = _required_string(data, "relative_path")
    if Path(relative_path).is_absolute() or ".." in Path(relative_path).parts:
        raise ManifestValidationError("relative_path must be relative and cannot traverse parents.")
    return CorpusSource(
        source_id=_required_string(data, "source_id"),
        organization=_required_string(data, "organization"),
        title=_required_string(data, "title"),
        language=_required_string(data, "language"),
        country=_optional_string(data.get("country")),
        source_type=source_type,
        source_roles=roles,
        relative_path=relative_path,
        crops=_string_tuple(data.get("crops", []), "crops"),
        factors=_string_tuple(data.get("factors", []), "factors"),
        source_reference=_optional_string(data.get("source_reference")),
    )


def _load_yaml_mapping(path: Path | None, default_resource: str) -> dict[str, Any]:
    if path is None:
        resource = files("via_backend.resources.knowledge").joinpath(default_resource)
        text = resource.read_text(encoding="utf-8")
        source_name = resource.name
    else:
        text = path.read_text(encoding="utf-8")
        source_name = path.name
    loaded = yaml.safe_load(text)
    if not isinstance(loaded, dict):
        raise ManifestValidationError(f"{source_name} must contain a YAML mapping.")
    return loaded


def _term_mapping(value: object, label: str) -> dict[str, tuple[str, ...]]:
    if not isinstance(value, dict):
        raise ManifestValidationError(f"taxonomy {label} must be a mapping.")
    parsed: dict[str, tuple[str, ...]] = {}
    for raw_key, raw_terms in value.items():
        if not isinstance(raw_key, str) or not raw_key.strip():
            raise ManifestValidationError(f"taxonomy {label} keys must be non-empty strings.")
        parsed[raw_key.strip().casefold()] = _string_tuple(raw_terms, f"{label}.{raw_key}")
    return parsed


def _required_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ManifestValidationError(f"{key} must be a non-empty string.")
    return value.strip()


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ManifestValidationError("Optional string metadata must be non-empty when present.")
    return value.strip()


def _string_tuple(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ManifestValidationError(f"{label} must be a list of strings.")
    normalized = tuple(item.strip() for item in value if item.strip())
    if len(normalized) != len(set(normalized)):
        raise ManifestValidationError(f"{label} must not contain duplicates.")
    return normalized
