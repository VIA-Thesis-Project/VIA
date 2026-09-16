"""Opt-in smoke test for the real CropSuiteLite adapter boundary."""

from __future__ import annotations

import hashlib
import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from via_backend.contexts.agroclimatic_evaluation.application.ports import (
    CropExecutionStatus,
    CropSuitabilityRequest,
    ScientificArtifactRole,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    EnvironmentalInputManifest,
    EnvironmentalInputSnapshot,
    ParcelSnapshot,
    SnapshotGeometry,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.cropsuite_adapter import (
    CropSuiteAdapter,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.scientific_artifact_store import (
    FilesystemScientificArtifactStore,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.scientific_input_integrity import (
    ConfiguredEnvironmentalInputIntegrityVerifier,
    load_cropsuite_environmental_input_bindings,
)


@pytest.mark.scientific
def test_real_cropsuite_adapter_smoke() -> None:
    if os.environ.get("VIA_RUN_CROPSUITE_SMOKE") != "1":
        pytest.skip("Set VIA_RUN_CROPSUITE_SMOKE=1 to run the scientific smoke test.")
    engine_root_value = os.environ.get("VIA_CROPSUITE_ROOT")
    workspace_value = os.environ.get("VIA_CROPSUITE_WORKSPACE")
    python_value = os.environ.get("VIA_CROPSUITE_PYTHON")
    artifacts_root_value = os.environ.get("VIA_ARTIFACTS_ROOT")
    bindings_value = os.environ.get("VIA_CROPSUITE_INPUT_BINDINGS")
    if (
        not engine_root_value
        or not workspace_value
        or not python_value
        or not artifacts_root_value
        or not bindings_value
    ):
        pytest.fail(
            "Set VIA_CROPSUITE_ROOT, VIA_CROPSUITE_WORKSPACE, "
            "VIA_CROPSUITE_PYTHON, VIA_ARTIFACTS_ROOT and "
            "VIA_CROPSUITE_INPUT_BINDINGS."
        )

    engine_root = Path(engine_root_value)
    artifacts_root = Path(artifacts_root_value)
    bindings = load_cropsuite_environmental_input_bindings(Path(bindings_value))
    input_integrity_verifier = ConfiguredEnvironmentalInputIntegrityVerifier(bindings)
    adapter = CropSuiteAdapter(
        engine_root=engine_root,
        workspace_root=Path(workspace_value),
        python_executable=Path(python_value),
        max_workers=1,
        artifact_store=FilesystemScientificArtifactStore(artifacts_root),
        input_integrity_verifier=input_integrity_verifier,
    )
    geometry = SnapshotGeometry.from_geojson(
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [-77.499, -11.009],
                    [-77.491, -11.009],
                    [-77.491, -11.001],
                    [-77.499, -11.001],
                    [-77.499, -11.009],
                ]
            ],
        }
    )
    resolved_at = datetime.now(UTC)
    request = CropSuitabilityRequest(
        evaluation_id=uuid4(),
        parcel_snapshot=ParcelSnapshot(
            project_id=uuid4(),
            parcel_id=uuid4(),
            parcel_version=1,
            geometry=geometry,
            crs="EPSG:4326",
            captured_at=datetime.now(UTC),
        ),
        crop_id="maize",
        environmental_input_manifest=EnvironmentalInputManifest(
            resolved_at=resolved_at,
            inputs=tuple(
                EnvironmentalInputSnapshot(
                    input_key=f"smoke.input.{index}",
                    dataset_id=binding.dataset_id,
                    dataset_name=f"Configured smoke input {index}",
                    source="smoke-test",
                    variable=f"configured_{index}",
                    unit="unit",
                    dataset_version_id=binding.dataset_version_id,
                    version_identifier=f"configured-{index}",
                    checksum=binding.checksum,
                    storage_reference=binding.storage_reference,
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
                    registered_at=resolved_at,
                )
                for index, binding in enumerate(bindings)
            ),
        ),
    )

    result = adapter.evaluate(request)

    assert result.status in {
        CropExecutionStatus.SUCCEEDED,
        CropExecutionStatus.NO_COVERAGE,
    }
    assert result.trace.engine_identifier == "CropSuiteLite"
    assert len(result.artifacts) == 1

    artifact = result.artifacts[0]

    assert artifact.role is ScientificArtifactRole.CROP_SUITABILITY
    assert artifact.media_type == "image/tiff"
    assert artifact.size_bytes > 0
    assert len(artifact.sha256) == 64

    assert artifact.grid.width > 0
    assert artifact.grid.height > 0
    assert artifact.grid.crs
    assert len(artifact.grid.transform) == 6

    durable_path = artifacts_root.joinpath(
        *artifact.storage_reference.split("/")
    )

    assert durable_path.is_file()
    assert durable_path.stat().st_size == artifact.size_bytes

    durable_sha256 = hashlib.sha256(durable_path.read_bytes()).hexdigest()
    assert durable_sha256 == artifact.sha256
