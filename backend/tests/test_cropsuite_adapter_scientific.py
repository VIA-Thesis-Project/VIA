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
    ParcelSnapshot,
    SnapshotGeometry,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.cropsuite_adapter import (
    CropSuiteAdapter,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.scientific_artifact_store import (
    FilesystemScientificArtifactStore,
)


@pytest.mark.scientific
def test_real_cropsuite_adapter_smoke() -> None:
    if os.environ.get("VIA_RUN_CROPSUITE_SMOKE") != "1":
        pytest.skip("Set VIA_RUN_CROPSUITE_SMOKE=1 to run the scientific smoke test.")
    engine_root_value = os.environ.get("VIA_CROPSUITE_ROOT")
    workspace_value = os.environ.get("VIA_CROPSUITE_WORKSPACE")
    python_value = os.environ.get("VIA_CROPSUITE_PYTHON")
    artifacts_root_value = os.environ.get("VIA_ARTIFACTS_ROOT")
    if (
        not engine_root_value
        or not workspace_value
        or not python_value
        or not artifacts_root_value
    ):
        pytest.fail(
            "Set VIA_CROPSUITE_ROOT, VIA_CROPSUITE_WORKSPACE, "
            "VIA_CROPSUITE_PYTHON and VIA_ARTIFACTS_ROOT."
        )

    engine_root = Path(engine_root_value)
    artifacts_root = Path(artifacts_root_value)
    adapter = CropSuiteAdapter(
        engine_root=engine_root,
        workspace_root=Path(workspace_value),
        python_executable=Path(python_value),
        max_workers=1,
        artifact_store=FilesystemScientificArtifactStore(artifacts_root),
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
