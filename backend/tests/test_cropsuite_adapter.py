"""Fast contract tests for the CropSuiteLite infrastructure boundary."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest

from via_backend.contexts.agroclimatic_evaluation.application.ports import (
    CropExecutionStatus,
    CropSuitabilityExecutionError,
    CropSuitabilityRequest,
    ICropSuitabilityEngine,
    InvalidEngineOutputError,
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


class StubRunner:
    def __init__(self, report: dict[str, Any]) -> None:
        self.report = report
        self.calls: list[dict[str, Any]] = []

    def __call__(self, **arguments: Any) -> dict[str, Any]:
        self.calls.append(arguments)
        return self.report


def _geometry(kind: str = "Polygon") -> SnapshotGeometry:
    polygon = [
        [[-77.5, -11.01], [-77.49, -11.01], [-77.49, -11.0], [-77.5, -11.0], [-77.5, -11.01]]
    ]
    coordinates: Any = polygon if kind == "Polygon" else [polygon]
    return SnapshotGeometry.from_geojson({"type": kind, "coordinates": coordinates})


def _environmental_input_manifest() -> EnvironmentalInputManifest:
    now = datetime(2026, 9, 12, 12, tzinfo=UTC)
    return EnvironmentalInputManifest(
        resolved_at=now,
        inputs=(
            EnvironmentalInputSnapshot(
                input_key="soil.ph",
                dataset_id=uuid4(),
                dataset_name="Soil pH",
                source="test",
                variable="ph",
                unit="pH",
                dataset_version_id=uuid4(),
                version_identifier="test-v1",
                checksum="sha256:test",
                storage_reference="test://soil-ph",
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
                registered_at=now,
            ),
        ),
    )


def _request(kind: str = "Polygon", crop_id: str = "maize") -> CropSuitabilityRequest:
    return CropSuitabilityRequest(
        evaluation_id=uuid4(),
        parcel_snapshot=ParcelSnapshot(
            project_id=uuid4(),
            parcel_id=uuid4(),
            parcel_version=3,
            geometry=_geometry(kind),
            crs="EPSG:4326",
            captured_at=datetime(2026, 9, 12, 12, tzinfo=UTC),
        ),
        crop_id=crop_id,
        environmental_input_manifest=_environmental_input_manifest(),
    )


def _summary(*, mean: float | None, valid_cells: int) -> dict[str, Any]:
    return {
        "mean": mean,
        "minimum": mean,
        "maximum": mean,
        "valid_cells": valid_cells,
        "valid_area_m2": 25.0 if valid_cells else 0.0,
        "coverage_fraction": 0.5 if valid_cells else 0.0,
        "zero_suitability_area_m2": 25.0 if mean == 0 else 0.0,
    }


def _report(
    status: str = "succeeded",
    *,
    mean: float | None = 72.5,
    valid_cells: int = 2,
) -> dict[str, Any]:
    crop: dict[str, Any] = {
        "id": "maize",
        "status": status,
        "parameter_sha256": "parameter-sha256",
        "config_sha256": "configuration-sha256",
        "elapsed_seconds": 1.25,
    }
    if status == "failed":
        crop["error"] = "RuntimeError: scientific process exited with code 1"
    else:
        crop["scores"] = {"crop_suitability": _summary(mean=mean, valid_cells=valid_cells)}
    return {
        "evaluation_id": "evaluation_engine_reference",
        "created_at": "2026-09-12T12:00:00+00:00",
        "finished_at": "2026-09-12T12:00:02+00:00",
        "selected_crops": ["maize"],
        "execution": "sequential_isolated_processes",
        "parcel_sha256": "parcel-sha256",
        "source_files_unchanged": True,
        "crops": [crop],
    }


def _adapter(tmp_path: Path, runner: StubRunner) -> CropSuiteAdapter:
    return CropSuiteAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        max_workers=1,
        runner=runner,
    )


def test_adapter_implements_application_port() -> None:
    adapter = CropSuiteAdapter(
        engine_root=Path("engine"),
        workspace_root=Path("workspace"),
        runner=StubRunner(_report()),
    )

    assert isinstance(adapter, ICropSuitabilityEngine)


@pytest.mark.parametrize("geometry_type", ["Polygon", "MultiPolygon"])
def test_adapter_preserves_crop_and_snapshot_geometry(tmp_path: Path, geometry_type: str) -> None:
    runner = StubRunner(_report())
    request = _request(geometry_type)

    result = _adapter(tmp_path, runner).evaluate(request)

    call = runner.calls[0]
    parcel = json.loads(Path(call["parcel_path"]).read_text(encoding="utf-8"))
    assert call["crops"] == ("maize",)
    assert call["max_workers"] == 1
    assert parcel["geometry"] == request.parcel_snapshot.geometry.to_geojson()
    assert parcel["geometry"]["type"] == geometry_type
    assert Path(call["parcel_path"]).is_relative_to(tmp_path / "workspace")
    assert Path(call["output_root"]).is_relative_to(tmp_path / "workspace")
    assert result.crop_id == "maize"


def test_valid_zero_score_is_a_successful_scientific_outcome(tmp_path: Path) -> None:
    result = _adapter(tmp_path, StubRunner(_report(mean=0.0, valid_cells=1))).evaluate(_request())

    assert result.status is CropExecutionStatus.SUCCEEDED
    assert result.suitability is not None
    assert result.suitability.mean == 0.0
    assert result.suitability.zero_suitability_area_m2 == 25.0
    assert result.failure is None


def test_no_coverage_is_not_collapsed_into_zero_or_failure(tmp_path: Path) -> None:
    result = _adapter(
        tmp_path,
        StubRunner(_report("no_coverage", mean=None, valid_cells=0)),
    ).evaluate(_request())

    assert result.status is CropExecutionStatus.NO_COVERAGE
    assert result.suitability is not None
    assert result.suitability.mean is None
    assert result.suitability.valid_cells == 0
    assert result.failure is None


def test_engine_reported_failure_is_explicit(tmp_path: Path) -> None:
    result = _adapter(tmp_path, StubRunner(_report("failed"))).evaluate(_request())

    assert result.status is CropExecutionStatus.FAILED
    assert result.suitability is None
    assert result.failure is not None
    assert "exited with code 1" in result.failure.message


def test_runner_failure_is_distinguishable_from_scientific_result(tmp_path: Path) -> None:
    def failing_runner(**arguments: Any) -> dict[str, Any]:
        del arguments
        raise OSError("cannot launch")

    adapter = CropSuiteAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        runner=failing_runner,
    )

    with pytest.raises(CropSuitabilityExecutionError, match="cannot launch"):
        adapter.evaluate(_request())


def test_missing_or_invalid_engine_outputs_fail_explicitly(tmp_path: Path) -> None:
    report = _report()
    report["crops"] = []

    with pytest.raises(InvalidEngineOutputError, match="exactly one"):
        _adapter(tmp_path, StubRunner(report)).evaluate(_request())


def test_workspace_cannot_be_inside_scientific_source_tree(tmp_path: Path) -> None:
    engine_root = tmp_path / "CropSuiteLite"

    with pytest.raises(ValueError, match="outside the engine source tree"):
        CropSuiteAdapter(
            engine_root=engine_root,
            workspace_root=engine_root / "results",
            runner=StubRunner(_report()),
        )


def test_adapter_artifacts_do_not_modify_source_crop_parameters(tmp_path: Path) -> None:
    engine_root = tmp_path / "CropSuiteLite"
    catalog = engine_root / "plant_params" / "available"
    catalog.mkdir(parents=True)
    parameter = catalog / "maize.inf"
    parameter.write_text("name=maize\ngrowing_cycle=120\n", encoding="utf-8")
    before = hashlib.sha256(parameter.read_bytes()).hexdigest()
    runner = StubRunner(_report())
    adapter = CropSuiteAdapter(
        engine_root=engine_root,
        workspace_root=tmp_path / "workspace",
        catalog=catalog,
        runner=runner,
    )

    adapter.evaluate(_request())

    assert hashlib.sha256(parameter.read_bytes()).hexdigest() == before
    assert runner.calls[0]["catalog"] == catalog.resolve()

def test_real_execution_requires_explicit_scientific_python(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="python_executable"):
        CropSuiteAdapter(
            engine_root=tmp_path / "engine",
            workspace_root=tmp_path / "workspace",
        )


def test_real_execution_uses_explicit_scientific_python(tmp_path: Path) -> None:
    engine_root = tmp_path / "engine"
    source_root = engine_root / "src"
    source_root.mkdir(parents=True)

    (source_root / "__init__.py").write_text("", encoding="utf-8")
    (source_root / "multicrop.py").write_text(
        """
from pathlib import Path
import sys


def run_evaluation(
    crops,
    parcel_path,
    output_root=None,
    source_config=None,
    catalog=None,
    max_workers=2,
    progress=None,
):
    del parcel_path, source_config, catalog, max_workers, progress

    output_root = Path(output_root)
    output_root.parent.joinpath("scientific-python.txt").write_text(
        sys.executable,
        encoding="utf-8",
    )

    return {
        "evaluation_id": "fake_scientific_process",
        "created_at": "2026-09-12T12:00:00+00:00",
        "finished_at": "2026-09-12T12:00:01+00:00",
        "selected_crops": list(crops),
        "execution": "sequential_isolated_processes",
        "parcel_sha256": "parcel-sha256",
        "source_files_unchanged": True,
        "crops": [
            {
                "id": crops[0],
                "status": "succeeded",
                "parameter_sha256": "parameter-sha256",
                "config_sha256": "configuration-sha256",
                "elapsed_seconds": 0.1,
                "scores": {
                    "crop_suitability": {
                        "mean": 72.5,
                        "minimum": 72.5,
                        "maximum": 72.5,
                        "valid_cells": 2,
                        "valid_area_m2": 25.0,
                        "coverage_fraction": 0.5,
                        "zero_suitability_area_m2": 0.0,
                    }
                },
            }
        ],
    }
""".strip(),
        encoding="utf-8",
    )

    workspace_root = tmp_path / "workspace"
    adapter = CropSuiteAdapter(
        engine_root=engine_root,
        workspace_root=workspace_root,
        python_executable=Path(sys.executable),
        max_workers=1,
    )

    result = adapter.evaluate(_request())

    marker = next(workspace_root.rglob("scientific-python.txt"))

    assert result.status is CropExecutionStatus.SUCCEEDED
    assert result.suitability is not None
    assert result.suitability.mean == 72.5
    assert Path(marker.read_text(encoding="utf-8")).resolve() == Path(sys.executable).resolve()

@pytest.mark.parametrize(
    ("status", "mean", "valid_cells"),
    [
        ("succeeded", 72.5, 2),
        ("no_coverage", None, 0),
    ],
)
def test_adapter_publishes_durable_crop_suitability_artifact(
    tmp_path: Path,
    status: str,
    mean: float | None,
    valid_cells: int,
) -> None:
    content = b"fake-geotiff-content"
    checksum = hashlib.sha256(content).hexdigest()

    def runner(**arguments: Any) -> dict[str, Any]:
        output_root = Path(arguments["output_root"])
        result_directory = output_root / "engine-result"
        result_directory.mkdir(parents=True)

        source = result_directory / "crop_suitability.tif"
        source.write_bytes(content)

        report = _report(
            status,
            mean=mean,
            valid_cells=valid_cells,
        )
        crop = report["crops"][0]
        crop["result_directory"] = str(result_directory)
        crop["via_artifact"] = {
            "sha256": checksum,
            "grid": {
                "crs": "EPSG:4326",
                "width": 2,
                "height": 1,
                "transform": [0.1, 0.0, -77.0, 0.0, -0.1, -11.0],
                "nodata": -1.0,
            },
        }
        return report

    artifact_root = tmp_path / "artifacts"
    adapter = CropSuiteAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        max_workers=1,
        runner=runner,
        artifact_store=FilesystemScientificArtifactStore(artifact_root),
    )

    result = adapter.evaluate(_request())

    assert len(result.artifacts) == 1

    artifact = result.artifacts[0]
    assert artifact.role is ScientificArtifactRole.CROP_SUITABILITY
    assert artifact.sha256 == checksum
    assert artifact.media_type == "image/tiff"
    assert artifact.size_bytes == len(content)
    assert artifact.grid.crs == "EPSG:4326"

    durable_path = artifact_root.joinpath(
        *artifact.storage_reference.split("/")
    )
    assert durable_path.read_bytes() == content

def test_adapter_rejects_artifact_outside_request_workspace(
    tmp_path: Path,
) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    source = outside / "crop_suitability.tif"
    source.write_bytes(b"content")

    checksum = hashlib.sha256(b"content").hexdigest()

    def runner(**arguments: Any) -> dict[str, Any]:
        del arguments

        report = _report()
        crop = report["crops"][0]
        crop["result_directory"] = str(outside)
        crop["via_artifact"] = {
            "sha256": checksum,
            "grid": {
                "crs": "EPSG:4326",
                "width": 1,
                "height": 1,
                "transform": [1.0, 0.0, 0.0, 0.0, -1.0, 0.0],
                "nodata": -1.0,
            },
        }
        return report

    adapter = CropSuiteAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        runner=runner,
        artifact_store=FilesystemScientificArtifactStore(
            tmp_path / "artifacts"
        ),
    )

    with pytest.raises(
        InvalidEngineOutputError,
        match="escapes the request workspace",
    ):
        adapter.evaluate(_request())
