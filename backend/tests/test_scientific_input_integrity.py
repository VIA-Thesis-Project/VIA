"""Focused tests for configured scientific environmental-input integrity."""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

import pytest

from via_backend.contexts.agroclimatic_evaluation.application import (
    EnvironmentalInputIntegrityError,
    ScientificSourceFingerprint,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    EnvironmentalInputManifest,
    EnvironmentalInputSnapshot,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    ConfiguredEnvironmentalInputIntegrityVerifier,
    CropSuiteEnvironmentalInputBinding,
    load_cropsuite_environmental_input_bindings,
)

NOW = datetime(2026, 9, 16, 12, tzinfo=UTC)
DATASET_ID = UUID("10000000-0000-0000-0000-000000000001")
DATASET_VERSION_ID = UUID("20000000-0000-0000-0000-000000000001")
SOURCE_A = "a" * 64
SOURCE_B = "b" * 64
SOURCE_C = "c" * 64


def _snapshot(
    *,
    input_key: str = "soil.ph",
    dataset_id: UUID = DATASET_ID,
    dataset_version_id: UUID = DATASET_VERSION_ID,
    storage_reference: str = "catalog://soil/ph/v1",
    checksum: str = "opaque:dataset-version-checksum",
) -> EnvironmentalInputSnapshot:
    return EnvironmentalInputSnapshot(
        input_key=input_key,
        dataset_id=dataset_id,
        dataset_name="Soil pH",
        source="Catalog",
        variable="ph",
        unit="pH",
        dataset_version_id=dataset_version_id,
        version_identifier="v1",
        checksum=checksum,
        storage_reference=storage_reference,
        crs="EPSG:4326",
        resolution_x=0.01,
        resolution_y=0.01,
        resolution_unit="degree",
        extent_west=-78.0,
        extent_south=-13.0,
        extent_east=-76.0,
        extent_north=-10.0,
        valid_from=None,
        valid_to=None,
        scenario=None,
        registered_at=NOW,
    )


def _manifest(*inputs: EnvironmentalInputSnapshot) -> EnvironmentalInputManifest:
    return EnvironmentalInputManifest(resolved_at=NOW, inputs=inputs or (_snapshot(),))


def _binding(
    *,
    dataset_id: UUID = DATASET_ID,
    dataset_version_id: UUID = DATASET_VERSION_ID,
    storage_reference: str = "catalog://soil/ph/v1",
    checksum: str = "opaque:dataset-version-checksum",
    source_sha256: tuple[str, ...] = (SOURCE_A,),
) -> CropSuiteEnvironmentalInputBinding:
    return CropSuiteEnvironmentalInputBinding(
        dataset_id=dataset_id,
        dataset_version_id=dataset_version_id,
        storage_reference=storage_reference,
        checksum=checksum,
        source_sha256=source_sha256,
    )


def _fingerprints(*hashes: str) -> tuple[ScientificSourceFingerprint, ...]:
    return tuple(
        ScientificSourceFingerprint(f"/scientific/source-{index}.tif", source_hash)
        for index, source_hash in enumerate(hashes)
    )


def test_exact_manifest_binding_and_sources_pass() -> None:
    verifier = ConfiguredEnvironmentalInputIntegrityVerifier((_binding(),))

    verifier.verify(_manifest(), _fingerprints(SOURCE_A))


def test_unknown_dataset_version_is_integrity_error() -> None:
    manifest = _manifest(
        replace(
            _snapshot(),
            dataset_version_id=UUID("20000000-0000-0000-0000-000000000002"),
        )
    )
    verifier = ConfiguredEnvironmentalInputIntegrityVerifier((_binding(),))

    with pytest.raises(EnvironmentalInputIntegrityError, match="No scientific input binding"):
        verifier.verify(manifest, _fingerprints(SOURCE_A))


@pytest.mark.parametrize(
    "snapshot",
    [
        replace(_snapshot(), dataset_id=UUID("10000000-0000-0000-0000-000000000002")),
        replace(_snapshot(), storage_reference="catalog://soil/ph/other"),
        replace(_snapshot(), checksum="opaque:different"),
    ],
)
def test_exact_dataset_identity_mismatch_is_integrity_error(
    snapshot: EnvironmentalInputSnapshot,
) -> None:
    verifier = ConfiguredEnvironmentalInputIntegrityVerifier((_binding(),))

    with pytest.raises(EnvironmentalInputIntegrityError, match="identity mismatch"):
        verifier.verify(_manifest(snapshot), _fingerprints(SOURCE_A))


def test_missing_required_source_hash_is_integrity_error() -> None:
    verifier = ConfiguredEnvironmentalInputIntegrityVerifier(
        (_binding(source_sha256=(SOURCE_A, SOURCE_B)),)
    )

    with pytest.raises(EnvironmentalInputIntegrityError, match=SOURCE_B):
        verifier.verify(_manifest(), _fingerprints(SOURCE_A, SOURCE_C))


def test_multiple_required_hashes_and_extra_engine_sources_are_allowed() -> None:
    verifier = ConfiguredEnvironmentalInputIntegrityVerifier(
        (_binding(source_sha256=(SOURCE_A, SOURCE_B)),)
    )

    verifier.verify(
        _manifest(),
        _fingerprints(SOURCE_C, SOURCE_B, SOURCE_A),
    )


def test_same_dataset_version_can_serve_distinct_input_keys() -> None:
    verifier = ConfiguredEnvironmentalInputIntegrityVerifier((_binding(),))
    manifest = _manifest(
        _snapshot(input_key="soil.ph"),
        _snapshot(input_key="soil.ph.root-zone"),
    )

    verifier.verify(manifest, _fingerprints(SOURCE_A))


@pytest.mark.parametrize(
    "source_sha256",
    [(), ("A" * 64,), ("a" * 63,), (SOURCE_A, SOURCE_A)],
)
def test_binding_rejects_invalid_source_hash_configuration(
    source_sha256: tuple[str, ...],
) -> None:
    with pytest.raises(ValueError, match="source_sha256"):
        _binding(source_sha256=source_sha256)


def test_verifier_rejects_duplicate_dataset_version_bindings() -> None:
    with pytest.raises(ValueError, match="Duplicate dataset_version_id"):
        ConfiguredEnvironmentalInputIntegrityVerifier((_binding(), _binding()))


def test_binding_loader_accepts_explicit_schema(tmp_path: Path) -> None:
    path = tmp_path / "bindings.json"
    path.write_text(
        json.dumps(
            {
                "bindings": [
                    {
                        "dataset_id": str(DATASET_ID),
                        "dataset_version_id": str(DATASET_VERSION_ID),
                        "storage_reference": "catalog://soil/ph/v1",
                        "checksum": "opaque:dataset-version-checksum",
                        "source_sha256": [SOURCE_A, SOURCE_B],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    assert load_cropsuite_environmental_input_bindings(path) == (
        _binding(source_sha256=(SOURCE_A, SOURCE_B)),
    )


@pytest.mark.parametrize(
    "payload, match",
    [
        ({"bindings": []}, "non-empty"),
        ({"bindings": [], "extra": True}, "unsupported fields"),
        (
            {
                "bindings": [
                    {
                        "dataset_id": "not-a-uuid",
                        "dataset_version_id": str(DATASET_VERSION_ID),
                        "storage_reference": "catalog://soil/ph/v1",
                        "checksum": "opaque",
                        "source_sha256": [SOURCE_A],
                    }
                ]
            },
            "valid UUID",
        ),
        (
            {
                "bindings": [
                    {
                        "dataset_id": str(DATASET_ID),
                        "dataset_version_id": str(DATASET_VERSION_ID),
                        "storage_reference": "catalog://soil/ph/v1",
                        "checksum": "opaque",
                        "source_sha256": [SOURCE_A],
                        "unexpected": "field",
                    }
                ]
            },
            "unsupported fields",
        ),
    ],
)
def test_binding_loader_rejects_invalid_schema(
    tmp_path: Path,
    payload: object,
    match: str,
) -> None:
    path = tmp_path / "bindings.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match=match):
        load_cropsuite_environmental_input_bindings(path)


def test_binding_loader_rejects_duplicate_dataset_version(tmp_path: Path) -> None:
    item = {
        "dataset_id": str(DATASET_ID),
        "dataset_version_id": str(DATASET_VERSION_ID),
        "storage_reference": "catalog://soil/ph/v1",
        "checksum": "opaque",
        "source_sha256": [SOURCE_A],
    }
    path = tmp_path / "bindings.json"
    path.write_text(json.dumps({"bindings": [item, item]}), encoding="utf-8")

    with pytest.raises(ValueError, match="Duplicate dataset_version_id"):
        load_cropsuite_environmental_input_bindings(path)
