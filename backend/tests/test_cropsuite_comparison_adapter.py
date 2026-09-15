from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import UUID

import pytest

from via_backend.contexts.agroclimatic_evaluation.application import (
    CommonSupportStatus,
    ComparableCropResult,
    CropComparisonExecutionError,
    CropComparisonInput,
    CropComparisonRequest,
    CropComparisonResult,
    ICropComparisonEngine,
    InvalidComparisonOutputError,
    ScientificArtifactDescriptor,
    ScientificArtifactGrid,
    ScientificArtifactRole,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    ParcelSnapshot,
    SnapshotGeometry,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    CropSuiteComparisonAdapter,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.scientific_artifact_store import (
    FilesystemScientificArtifactStore,
)

EVALUATION_ID = UUID("00000000-0000-0000-0000-000000000010")


class StubComparisonRunner:
    def __init__(self, report: dict[str, Any]) -> None:
        self.report = report
        self.calls: list[dict[str, Any]] = []

    def __call__(self, **arguments: Any) -> dict[str, Any]:
        self.calls.append(arguments)
        return self.report


def _snapshot() -> ParcelSnapshot:
    return ParcelSnapshot(
        project_id=UUID("00000000-0000-0000-0000-000000000001"),
        parcel_id=UUID("00000000-0000-0000-0000-000000000002"),
        parcel_version=1,
        geometry=SnapshotGeometry.from_geojson(
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-77.5, -11.01],
                        [-77.49, -11.01],
                        [-77.49, -11.0],
                        [-77.5, -11.0],
                        [-77.5, -11.01],
                    ]
                ],
            }
        ),
        crs="EPSG:4326",
        captured_at=datetime(2026, 9, 14, tzinfo=UTC),
    )


def _artifact(
    tmp_path: Path,
    store: FilesystemScientificArtifactStore,
    crop_id: str,
) -> ScientificArtifactDescriptor:
    source = tmp_path / f"{crop_id}.tif"
    source.write_bytes(f"fake-{crop_id}".encode())

    published = store.publish(
        source,
        (
            f"evaluations/{EVALUATION_ID}/crops/"
            f"{crop_id}/crop_suitability.tif"
        ),
    )

    return ScientificArtifactDescriptor(
        role=ScientificArtifactRole.CROP_SUITABILITY,
        storage_reference=published.storage_reference,
        sha256=published.sha256,
        media_type="image/tiff",
        size_bytes=published.size_bytes,
        grid=ScientificArtifactGrid(
            crs="EPSG:4326",
            width=2,
            height=2,
            transform=(
                0.01,
                0.0,
                -77.5,
                0.0,
                -0.01,
                -11.0,
            ),
            nodata=-1.0,
        ),
    )


def _request(
    tmp_path: Path,
    store: FilesystemScientificArtifactStore,
) -> CropComparisonRequest:
    return CropComparisonRequest(
        evaluation_id=EVALUATION_ID,
        parcel_snapshot=_snapshot(),
        crops=(
            CropComparisonInput(
                crop_id="maize",
                artifact=_artifact(tmp_path, store, "maize"),
            ),
            CropComparisonInput(
                crop_id="potato",
                artifact=_artifact(tmp_path, store, "potato"),
            ),
        ),
    )


def _report() -> dict[str, Any]:
    return {
        "status": "comparable",
        "method": "area_weighted_mean_on_common_valid_cells",
        "area_crs": "EPSG:6933",
        "parcel_area_m2": 100.0,
        "common_valid_area_m2": 80.0,
        "common_coverage_fraction": 0.8,
        "eligible_crops": ["maize", "potato"],
        "excluded_without_coverage": [],
        "ranking": [
            {
                "crop_id": "maize",
                "mean": 80.0,
                "rank": 1,
            },
            {
                "crop_id": "potato",
                "mean": 70.0,
                "rank": 2,
            },
        ],
    }


def test_adapter_implements_comparison_port(
    tmp_path: Path,
) -> None:
    store = FilesystemScientificArtifactStore(
        tmp_path / "artifacts"
    )

    adapter = CropSuiteComparisonAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        artifact_store=store,
        runner=StubComparisonRunner(_report()),
    )

    assert isinstance(adapter, ICropComparisonEngine)


def test_adapter_maps_common_support_and_comparable_ranking(
    tmp_path: Path,
) -> None:
    store = FilesystemScientificArtifactStore(
        tmp_path / "artifacts"
    )
    runner = StubComparisonRunner(_report())

    adapter = CropSuiteComparisonAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        artifact_store=store,
        runner=runner,
    )

    result = adapter.compare(
        _request(tmp_path, store)
    )

    assert isinstance(result, CropComparisonResult)

    assert (
        result.common_support.status
        is CommonSupportStatus.COMPARABLE
    )
    assert result.common_support.parcel_area_m2 == 100.0
    assert result.common_support.common_valid_area_m2 == 80.0
    assert result.common_support.common_coverage_fraction == 0.8
    assert result.common_support.eligible_crops == (
        "maize",
        "potato",
    )
    assert (
        result.common_support.excluded_without_coverage
        == ()
    )

    assert result.comparable_crops == (
        ComparableCropResult(
            crop_id="maize",
            mean=80.0,
            rank=1,
        ),
        ComparableCropResult(
            crop_id="potato",
            mean=70.0,
            rank=2,
        ),
    )

    assert len(runner.calls) == 1
    assert tuple(
        crop["crop_id"]
        for crop in runner.calls[0]["crops"]
    ) == (
        "maize",
        "potato",
    )


def test_no_common_coverage_remains_distinct(
    tmp_path: Path,
) -> None:
    store = FilesystemScientificArtifactStore(
        tmp_path / "artifacts"
    )

    report = {
        "status": "no_common_coverage",
        "method": "area_weighted_mean_on_common_valid_cells",
        "area_crs": "EPSG:6933",
        "parcel_area_m2": 100.0,
        "common_valid_area_m2": 0.0,
        "common_coverage_fraction": 0.0,
        "excluded_without_coverage": [],
        "ranking": [],
    }

    adapter = CropSuiteComparisonAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        artifact_store=store,
        runner=StubComparisonRunner(report),
    )

    result = adapter.compare(
        _request(tmp_path, store)
    )

    assert (
        result.common_support.status
        is CommonSupportStatus.NO_COMMON_COVERAGE
    )
    assert result.common_support.common_valid_area_m2 == 0.0
    assert result.common_support.eligible_crops == (
        "maize",
        "potato",
    )
    assert result.comparable_crops == ()


def test_adapter_rejects_ranking_with_unknown_crop(
    tmp_path: Path,
) -> None:
    store = FilesystemScientificArtifactStore(
        tmp_path / "artifacts"
    )

    report = _report()
    report["ranking"] = [
        {
            "crop_id": "unknown",
            "mean": 80.0,
            "rank": 1,
        },
        {
            "crop_id": "potato",
            "mean": 70.0,
            "rank": 2,
        },
    ]

    adapter = CropSuiteComparisonAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        artifact_store=store,
        runner=StubComparisonRunner(report),
    )

    with pytest.raises(
        InvalidComparisonOutputError,
        match="non-eligible crop",
    ):
        adapter.compare(
            _request(tmp_path, store)
        )


def test_adapter_rejects_ranking_for_no_common_coverage(
    tmp_path: Path,
) -> None:
    store = FilesystemScientificArtifactStore(
        tmp_path / "artifacts"
    )

    report = {
        "status": "no_common_coverage",
        "method": "area_weighted_mean_on_common_valid_cells",
        "area_crs": "EPSG:6933",
        "parcel_area_m2": 100.0,
        "common_valid_area_m2": 0.0,
        "common_coverage_fraction": 0.0,
        "excluded_without_coverage": [],
        "ranking": [
            {
                "crop_id": "maize",
                "mean": 50.0,
                "rank": 1,
            },
        ],
    }

    adapter = CropSuiteComparisonAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        artifact_store=store,
        runner=StubComparisonRunner(report),
    )

    with pytest.raises(
        InvalidComparisonOutputError,
        match="non-comparable result cannot contain ranked crops",
    ):
        adapter.compare(
            _request(tmp_path, store)
        )


def test_adapter_accepts_deterministic_tied_ranking(
    tmp_path: Path,
) -> None:
    store = FilesystemScientificArtifactStore(
        tmp_path / "artifacts"
    )

    report = _report()
    report["ranking"] = [
        {
            "crop_id": "maize",
            "mean": 80.0,
            "rank": 1,
        },
        {
            "crop_id": "potato",
            "mean": 80.0,
            "rank": 1,
        },
    ]

    adapter = CropSuiteComparisonAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        artifact_store=store,
        runner=StubComparisonRunner(report),
    )

    result = adapter.compare(
        _request(tmp_path, store)
    )

    assert result.comparable_crops == (
        ComparableCropResult(
            crop_id="maize",
            mean=80.0,
            rank=1,
        ),
        ComparableCropResult(
            crop_id="potato",
            mean=80.0,
            rank=1,
        ),
    )


def test_modified_durable_artifact_fails_before_scientific_runner(
    tmp_path: Path,
) -> None:
    artifact_root = tmp_path / "artifacts"
    store = FilesystemScientificArtifactStore(
        artifact_root
    )
    runner = StubComparisonRunner(_report())

    request = _request(tmp_path, store)

    artifact = request.crops[0].artifact
    durable_path = artifact_root.joinpath(
        *artifact.storage_reference.split("/")
    )
    durable_path.write_bytes(b"tampered")

    adapter = CropSuiteComparisonAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        artifact_store=store,
        runner=runner,
    )

    with pytest.raises(
        CropComparisonExecutionError,
        match="artifact resolution failed",
    ):
        adapter.compare(request)

    assert runner.calls == []


def test_real_comparison_requires_explicit_scientific_python(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        ValueError,
        match="python_executable",
    ):
        CropSuiteComparisonAdapter(
            engine_root=tmp_path / "engine",
            workspace_root=tmp_path / "workspace",
            artifact_store=FilesystemScientificArtifactStore(
                tmp_path / "artifacts"
            ),
        )