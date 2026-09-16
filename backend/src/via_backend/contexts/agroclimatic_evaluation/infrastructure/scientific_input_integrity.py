"""Configured binding between exact dataset versions and CropSuite source hashes."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast
from uuid import UUID

from ..application.ports import (
    EnvironmentalInputIntegrityError,
    IEnvironmentalInputIntegrityVerifier,
    ScientificSourceFingerprint,
)
from ..domain.environmental_inputs import EnvironmentalInputManifest

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ROOT_FIELDS = frozenset({"bindings"})
_BINDING_FIELDS = frozenset(
    {
        "dataset_id",
        "dataset_version_id",
        "storage_reference",
        "checksum",
        "source_sha256",
    }
)


@dataclass(frozen=True, slots=True)
class CropSuiteEnvironmentalInputBinding:
    """Deployment mapping from one exact DatasetVersion to expected source hashes."""

    dataset_id: UUID
    dataset_version_id: UUID
    storage_reference: str
    checksum: str
    source_sha256: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.dataset_id, UUID):
            raise ValueError("dataset_id must be a UUID.")
        if not isinstance(self.dataset_version_id, UUID):
            raise ValueError("dataset_version_id must be a UUID.")
        _require_trimmed_text(self.storage_reference, "storage_reference")
        _require_trimmed_text(self.checksum, "checksum")

        hashes = tuple(self.source_sha256)
        if not hashes:
            raise ValueError("source_sha256 must contain at least one SHA-256 value.")
        for item in hashes:
            if not isinstance(item, str) or _SHA256.fullmatch(item) is None:
                raise ValueError(
                    "source_sha256 values must be 64-character lowercase hexadecimal SHA-256."
                )
        if len(set(hashes)) != len(hashes):
            raise ValueError("source_sha256 must not contain duplicate hashes.")

        object.__setattr__(self, "source_sha256", hashes)


class ConfiguredEnvironmentalInputIntegrityVerifier(IEnvironmentalInputIntegrityVerifier):
    """Verify manifests using deployment-configured exact dataset-version bindings."""

    def __init__(self, bindings: Iterable[CropSuiteEnvironmentalInputBinding]) -> None:
        configured = tuple(bindings)
        if not configured:
            raise ValueError("At least one environmental input binding is required.")

        by_version: dict[UUID, CropSuiteEnvironmentalInputBinding] = {}
        for binding in configured:
            if binding.dataset_version_id in by_version:
                raise ValueError(
                    "Duplicate dataset_version_id binding: "
                    f"{binding.dataset_version_id}."
                )
            by_version[binding.dataset_version_id] = binding

        self._bindings = configured
        self._by_version = by_version

    @property
    def bindings(self) -> tuple[CropSuiteEnvironmentalInputBinding, ...]:
        return self._bindings

    def verify(
        self,
        manifest: EnvironmentalInputManifest,
        source_fingerprints: tuple[ScientificSourceFingerprint, ...],
    ) -> None:
        actual_hashes = {fingerprint.sha256 for fingerprint in source_fingerprints}

        for snapshot in manifest.inputs:
            binding = self._by_version.get(snapshot.dataset_version_id)
            if binding is None:
                raise EnvironmentalInputIntegrityError(
                    "No scientific input binding exists for dataset version "
                    f"{snapshot.dataset_version_id} (input {snapshot.input_key!r})."
                )

            expected_identity = (
                ("dataset_id", binding.dataset_id, snapshot.dataset_id),
                (
                    "dataset_version_id",
                    binding.dataset_version_id,
                    snapshot.dataset_version_id,
                ),
                (
                    "storage_reference",
                    binding.storage_reference,
                    snapshot.storage_reference,
                ),
                ("checksum", binding.checksum, snapshot.checksum),
            )
            for field_name, expected, actual in expected_identity:
                if expected != actual:
                    raise EnvironmentalInputIntegrityError(
                        "Scientific input binding identity mismatch for input "
                        f"{snapshot.input_key!r}: {field_name}."
                    )

            missing_hashes = tuple(
                source_hash
                for source_hash in binding.source_sha256
                if source_hash not in actual_hashes
            )
            if missing_hashes:
                raise EnvironmentalInputIntegrityError(
                    "Scientific input binding is missing expected CropSuite source SHA-256 "
                    f"for input {snapshot.input_key!r}: {', '.join(missing_hashes)}."
                )


def load_cropsuite_environmental_input_bindings(
    path: Path,
) -> tuple[CropSuiteEnvironmentalInputBinding, ...]:
    """Load and strictly validate deployment environmental-input binding JSON."""

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ValueError(f"Cannot read CropSuite input bindings file {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"CropSuite input bindings file {path} is invalid JSON.") from error

    root = _require_mapping(raw, "binding file")
    _require_exact_fields(root, _ROOT_FIELDS, "binding file")
    raw_bindings = root.get("bindings")
    if not isinstance(raw_bindings, list) or not raw_bindings:
        raise ValueError("CropSuite input bindings must contain a non-empty 'bindings' array.")

    bindings: list[CropSuiteEnvironmentalInputBinding] = []
    seen_versions: set[UUID] = set()
    for index, raw_binding in enumerate(raw_bindings):
        item = _require_mapping(raw_binding, f"bindings[{index}]")
        _require_exact_fields(item, _BINDING_FIELDS, f"bindings[{index}]")

        dataset_id = _parse_uuid(item.get("dataset_id"), f"bindings[{index}].dataset_id")
        dataset_version_id = _parse_uuid(
            item.get("dataset_version_id"),
            f"bindings[{index}].dataset_version_id",
        )
        if dataset_version_id in seen_versions:
            raise ValueError(
                "Duplicate dataset_version_id binding: "
                f"{dataset_version_id}."
            )
        seen_versions.add(dataset_version_id)

        source_sha256 = item.get("source_sha256")
        if not isinstance(source_sha256, list):
            raise ValueError(f"bindings[{index}].source_sha256 must be an array.")

        binding = CropSuiteEnvironmentalInputBinding(
            dataset_id=dataset_id,
            dataset_version_id=dataset_version_id,
            storage_reference=_require_json_string(
                item.get("storage_reference"),
                f"bindings[{index}].storage_reference",
            ),
            checksum=_require_json_string(
                item.get("checksum"),
                f"bindings[{index}].checksum",
            ),
            source_sha256=tuple(cast(list[Any], source_sha256)),
        )
        bindings.append(binding)

    return tuple(bindings)


def load_configured_environmental_input_integrity_verifier(
    path: Path,
) -> ConfiguredEnvironmentalInputIntegrityVerifier:
    """Build the configured verifier from one deployment binding file."""

    return ConfiguredEnvironmentalInputIntegrityVerifier(
        load_cropsuite_environmental_input_bindings(path)
    )


def _require_trimmed_text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError(f"{name} must be a non-empty trimmed string.")
    return value


def _require_json_string(value: object, name: str) -> str:
    return _require_trimmed_text(value, name)


def _parse_uuid(value: object, name: str) -> UUID:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a UUID string.")
    try:
        return UUID(value)
    except ValueError as error:
        raise ValueError(f"{name} must be a valid UUID.") from error


def _require_mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a JSON object.")
    if not all(isinstance(key, str) for key in value):
        raise ValueError(f"{name} must use string field names.")
    return cast(Mapping[str, Any], value)


def _require_exact_fields(
    value: Mapping[str, Any],
    expected: frozenset[str],
    name: str,
) -> None:
    actual = set(value)
    missing = expected - actual
    extra = actual - expected
    if missing:
        raise ValueError(f"{name} is missing fields: {', '.join(sorted(missing))}.")
    if extra:
        raise ValueError(f"{name} contains unsupported fields: {', '.join(sorted(extra))}.")
