"""Opt-in smoke test for the real CropSuiteLite adapter boundary."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from via_backend.contexts.agroclimatic_evaluation.application.ports import (
    CropExecutionStatus,
    CropSuitabilityRequest,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    ParcelSnapshot,
    SnapshotGeometry,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.cropsuite_adapter import (
    CropSuiteAdapter,
)


@pytest.mark.scientific
def test_real_cropsuite_adapter_smoke() -> None:
    if os.environ.get("VIA_RUN_CROPSUITE_SMOKE") != "1":
        pytest.skip("Set VIA_RUN_CROPSUITE_SMOKE=1 to run the scientific smoke test.")
    engine_root_value = os.environ.get("VIA_CROPSUITE_ROOT")
    workspace_value = os.environ.get("VIA_CROPSUITE_WORKSPACE")
    python_value = os.environ.get("VIA_CROPSUITE_PYTHON")
    if not engine_root_value or not workspace_value or not python_value:
        pytest.fail(
            "Set VIA_CROPSUITE_ROOT, VIA_CROPSUITE_WORKSPACE "
            "and VIA_CROPSUITE_PYTHON."
        )

    engine_root = Path(engine_root_value)
    adapter = CropSuiteAdapter(
        engine_root=engine_root,
        workspace_root=Path(workspace_value),
        python_executable=Path(python_value),
        max_workers=1,
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
