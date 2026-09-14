"""Opt-in smoke test for the real CropSuiteLite comparison boundary."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from via_backend.contexts.agroclimatic_evaluation.application import (
    CommonSupportStatus,
    CropComparisonInput,
    CropComparisonRequest,
)
from via_backend.contexts.agroclimatic_evaluation.application.ports import (
    CropExecutionStatus,
    CropSuitabilityRequest,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    ParcelSnapshot,
    SnapshotGeometry,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    CropSuiteAdapter,
    CropSuiteComparisonAdapter,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.scientific_artifact_store import (
    FilesystemScientificArtifactStore,
)


@pytest.mark.scientific
def test_real_cropsuite_comparison_adapter_smoke() -> None:
    if os.environ.get("VIA_RUN_CROPSUITE_SMOKE") != "1":
        pytest.skip(
            "Set VIA_RUN_CROPSUITE_SMOKE=1 to run the scientific smoke test."
        )

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
    workspace_root = Path(workspace_value)
    python_executable = Path(python_value)
    artifacts_root = Path(artifacts_root_value)

    artifact_store = FilesystemScientificArtifactStore(
        artifacts_root
    )

    suitability_adapter = CropSuiteAdapter(
        engine_root=engine_root,
        workspace_root=workspace_root / "suitability",
        python_executable=python_executable,
        max_workers=1,
        artifact_store=artifact_store,
    )

    comparison_adapter = CropSuiteComparisonAdapter(
        engine_root=engine_root,
        workspace_root=workspace_root / "comparison",
        python_executable=python_executable,
        artifact_store=artifact_store,
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

    evaluation_id = uuid4()

    snapshot = ParcelSnapshot(
        project_id=uuid4(),
        parcel_id=uuid4(),
        parcel_version=1,
        geometry=geometry,
        crs="EPSG:4326",
        captured_at=datetime.now(UTC),
    )

    results = []

    for crop_id in ("maize", "barley"):
        result = suitability_adapter.evaluate(
            CropSuitabilityRequest(
                evaluation_id=evaluation_id,
                parcel_snapshot=snapshot,
                crop_id=crop_id,
            )
        )

        assert result.status in {
            CropExecutionStatus.SUCCEEDED,
            CropExecutionStatus.NO_COVERAGE,
        }
        assert len(result.artifacts) == 1

        results.append(result)

    comparison = comparison_adapter.compare(
        CropComparisonRequest(
            evaluation_id=evaluation_id,
            parcel_snapshot=snapshot,
            crops=tuple(
                CropComparisonInput(
                    crop_id=result.crop_id,
                    artifact=result.artifacts[0],
                )
                for result in results
            ),
        )
    )

    assert comparison.status in {
        CommonSupportStatus.COMPARABLE,
        CommonSupportStatus.NO_COMMON_COVERAGE,
    }

    assert comparison.parcel_area_m2 > 0
    assert comparison.common_valid_area_m2 >= 0
    assert 0 <= comparison.common_coverage_fraction <= 1

    assert comparison.method == (
        "area_weighted_mean_on_common_valid_cells"
    )
    assert comparison.area_crs == "EPSG:6933"

    requested = {"maize", "barley"}
    eligible = set(comparison.eligible_crops)
    excluded = set(comparison.excluded_without_coverage)

    assert eligible.isdisjoint(excluded)
    assert eligible | excluded == requested

    if comparison.status is CommonSupportStatus.COMPARABLE:
        assert comparison.common_valid_area_m2 > 0
        assert comparison.common_coverage_fraction > 0
        assert eligible

    if comparison.status is CommonSupportStatus.NO_COMMON_COVERAGE:
        assert comparison.common_valid_area_m2 == 0
        assert comparison.common_coverage_fraction == 0