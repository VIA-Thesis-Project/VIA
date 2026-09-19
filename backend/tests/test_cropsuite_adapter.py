"""Fast contract tests for the CropSuiteLite infrastructure boundary."""

from __future__ import annotations

import configparser
import hashlib
import json
import sys
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest

from via_backend.contexts.agroclimatic_evaluation.application.ports import (
    CropExecutionStatus,
    CropSuitabilityExecutionError,
    CropSuitabilityRequest,
    EnvironmentalInputIntegrityError,
    ICropSuitabilityEngine,
    InvalidEngineOutputError,
    LimitationEvidenceAvailability,
    ScientificArtifactRole,
    ScientificSourceFingerprint,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    EnvironmentalInputManifest,
    EnvironmentalInputSnapshot,
    ParcelSnapshot,
    SnapshotGeometry,
    WaterRegime,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.cropsuite_adapter import (
    CropSuiteAdapter,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.scientific_artifact_store import (
    FilesystemScientificArtifactStore,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.scientific_input_integrity import (
    ConfiguredEnvironmentalInputIntegrityVerifier,
    CropSuiteEnvironmentalInputBinding,
)

SOURCE_A = "a" * 64
SOURCE_B = "b" * 64
SOURCE_C = "c" * 64


def _write_base_config(engine_root: Path) -> Path:
    engine_root.mkdir(parents=True, exist_ok=True)
    source_config = engine_root / "config_access_esm1_5_ssp126_2021_2040.ini"
    source_config.write_text(
        "[options]\nirrigation = 0\nunchanged = keep-me\n",
        encoding="utf-8",
    )
    return source_config


@pytest.fixture(autouse=True)
def _default_base_config(tmp_path: Path) -> None:
    _write_base_config(tmp_path / "engine")


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


def _request(
    kind: str = "Polygon",
    crop_id: str = "maize",
    *,
    water_regime: WaterRegime = WaterRegime.RAINFED,
) -> CropSuitabilityRequest:
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
        water_regime=water_regime,
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
        "source_sha256": {
            "/science/z-source.tif": SOURCE_B,
            "/science/a-source.tif": SOURCE_A,
        },
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


def _integrity_verifier(
    manifest: EnvironmentalInputManifest,
    *,
    source_sha256: tuple[str, ...] = (SOURCE_A,),
) -> ConfiguredEnvironmentalInputIntegrityVerifier:
    snapshot = manifest.inputs[0]
    return ConfiguredEnvironmentalInputIntegrityVerifier(
        (
            CropSuiteEnvironmentalInputBinding(
                dataset_id=snapshot.dataset_id,
                dataset_version_id=snapshot.dataset_version_id,
                storage_reference=snapshot.storage_reference,
                checksum=snapshot.checksum,
                source_sha256=source_sha256,
            ),
        )
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


def test_integrity_verifier_receives_manifest_and_sorted_source_fingerprints(
    tmp_path: Path,
) -> None:
    request = _request()
    received: list[
        tuple[
            EnvironmentalInputManifest,
            tuple[ScientificSourceFingerprint, ...],
        ]
    ] = []
    delegate = _integrity_verifier(request.environmental_input_manifest)

    class RecordingVerifier:
        def verify(
            self,
            manifest: EnvironmentalInputManifest,
            source_fingerprints: tuple[ScientificSourceFingerprint, ...],
        ) -> None:
            received.append((manifest, source_fingerprints))
            delegate.verify(manifest, source_fingerprints)

    adapter = CropSuiteAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        runner=StubRunner(_report()),
        input_integrity_verifier=RecordingVerifier(),
    )

    result = adapter.evaluate(request)

    assert received == [
        (
            request.environmental_input_manifest,
            (
                ScientificSourceFingerprint("/science/a-source.tif", SOURCE_A),
                ScientificSourceFingerprint("/science/z-source.tif", SOURCE_B),
            ),
        )
    ]
    assert result.trace.source_fingerprints == received[0][1]


def test_low_level_runner_without_integrity_verifier_keeps_empty_source_trace(
    tmp_path: Path,
) -> None:
    result = _adapter(tmp_path, StubRunner(_report())).evaluate(_request())

    assert result.trace.source_fingerprints == ()


@pytest.mark.parametrize(
    "source_sha256",
    [
        None,
        {},
        {"": SOURCE_A},
        {"/science/source.tif": "A" * 64},
        {"/science/source.tif": "abc"},
    ],
)
def test_integrity_gate_rejects_missing_or_malformed_source_fingerprints(
    tmp_path: Path,
    source_sha256: object,
) -> None:
    request = _request()
    report = _report()
    if source_sha256 is None:
        report.pop("source_sha256")
    else:
        report["source_sha256"] = source_sha256
    adapter = CropSuiteAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        runner=StubRunner(report),
        input_integrity_verifier=_integrity_verifier(request.environmental_input_manifest),
    )

    with pytest.raises(InvalidEngineOutputError, match="source_sha256"):
        adapter.evaluate(request)


def test_integrity_mismatch_fails_before_result_mapping(tmp_path: Path) -> None:
    request = _request()
    report = _report("no_coverage", mean=None, valid_cells=0)
    report["source_sha256"] = {"/science/unexpected.tif": SOURCE_C}
    report["crops"] = []
    adapter = CropSuiteAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        runner=StubRunner(report),
        input_integrity_verifier=_integrity_verifier(request.environmental_input_manifest),
    )

    with pytest.raises(EnvironmentalInputIntegrityError, match="missing expected"):
        adapter.evaluate(request)


def test_integrity_verifier_allows_extra_engine_sources(tmp_path: Path) -> None:
    request = _request()
    report = _report()
    report["source_sha256"] = {
        "/science/environment.tif": SOURCE_A,
        "/science/config.ini": SOURCE_B,
        "/science/maize.inf": SOURCE_C,
    }
    adapter = CropSuiteAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        runner=StubRunner(report),
        input_integrity_verifier=_integrity_verifier(request.environmental_input_manifest),
    )

    result = adapter.evaluate(request)

    assert result.status is CropExecutionStatus.SUCCEEDED


def test_source_file_mutation_remains_explicit_scientific_failure(tmp_path: Path) -> None:
    request = _request()
    report = _report()
    report["source_files_unchanged"] = False
    report["error"] = "Scientific source files changed during execution."
    adapter = CropSuiteAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        runner=StubRunner(report),
        input_integrity_verifier=_integrity_verifier(request.environmental_input_manifest),
    )

    result = adapter.evaluate(request)

    assert result.status is CropExecutionStatus.FAILED
    assert result.suitability is None
    assert result.failure is not None
    assert "changed during execution" in result.failure.message


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
    _write_base_config(engine_root)
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


def test_adapter_materializes_isolated_water_regime_configs(tmp_path: Path) -> None:
    engine_root = tmp_path / "engine"
    base_config = _write_base_config(engine_root)
    before = base_config.read_bytes()
    generated_hashes: list[str] = []
    config_paths: list[Path] = []

    def runner(**arguments: Any) -> dict[str, Any]:
        source_config = Path(arguments["source_config"])
        config_paths.append(source_config)
        configuration_sha256 = hashlib.sha256(source_config.read_bytes()).hexdigest()
        generated_hashes.append(configuration_sha256)
        report = _report()
        report["crops"][0]["config_sha256"] = configuration_sha256
        return report

    adapter = CropSuiteAdapter(
        engine_root=engine_root,
        workspace_root=tmp_path / "workspace",
        runner=runner,
    )
    rainfed_request = _request(water_regime=WaterRegime.RAINFED)
    irrigated_request = replace(
        rainfed_request,
        water_regime=WaterRegime.IRRIGATED,
    )

    rainfed = adapter.evaluate(rainfed_request)
    irrigated = adapter.evaluate(irrigated_request)

    assert len(config_paths) == 2
    assert config_paths[0] != config_paths[1]

    irrigation_values: list[str] = []
    for generated in config_paths:
        parser = configparser.ConfigParser(interpolation=None)
        parser.read(generated, encoding="utf-8")
        irrigation_values.append(parser.get("options", "irrigation"))
        assert parser.get("options", "unchanged") == "keep-me"

    assert irrigation_values == ["0", "1"]
    assert base_config.read_bytes() == before
    assert generated_hashes[0] != generated_hashes[1]
    assert rainfed.trace.configuration_sha256 == generated_hashes[0]
    assert irrigated.trace.configuration_sha256 == generated_hashes[1]
    assert rainfed.water_regime is WaterRegime.RAINFED
    assert irrigated.water_regime is WaterRegime.IRRIGATED


def test_real_execution_requires_explicit_scientific_python(tmp_path: Path) -> None:
    manifest = _environmental_input_manifest()
    with pytest.raises(ValueError, match="python_executable"):
        CropSuiteAdapter(
            engine_root=tmp_path / "engine",
            workspace_root=tmp_path / "workspace",
            input_integrity_verifier=_integrity_verifier(manifest),
        )


def test_real_execution_requires_integrity_verifier(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="input_integrity_verifier"):
        CropSuiteAdapter(
            engine_root=tmp_path / "engine",
            workspace_root=tmp_path / "workspace",
            python_executable=Path(sys.executable),
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
        "source_sha256": {
            "/science/environment.tif": (
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            )
        },
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
    request = _request()
    adapter = CropSuiteAdapter(
        engine_root=engine_root,
        workspace_root=workspace_root,
        python_executable=Path(sys.executable),
        max_workers=1,
        input_integrity_verifier=_integrity_verifier(request.environmental_input_manifest),
    )

    result = adapter.evaluate(request)

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


def test_scenario_artifact_paths_do_not_collide(tmp_path: Path) -> None:
    content = b"scenario-geotiff-content"
    checksum = hashlib.sha256(content).hexdigest()

    def runner(**arguments: Any) -> dict[str, Any]:
        output_root = Path(arguments["output_root"])
        result_directory = output_root / "engine-result"
        result_directory.mkdir(parents=True)
        (result_directory / "crop_suitability.tif").write_bytes(content)

        report = _report()
        crop = report["crops"][0]
        crop["result_directory"] = str(result_directory)
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
        artifact_store=FilesystemScientificArtifactStore(tmp_path / "artifacts"),
    )
    rainfed_request = _request(water_regime=WaterRegime.RAINFED)
    irrigated_request = replace(
        rainfed_request,
        water_regime=WaterRegime.IRRIGATED,
    )

    rainfed = adapter.evaluate(rainfed_request)
    irrigated = adapter.evaluate(irrigated_request)

    assert rainfed.artifacts[0].storage_reference == (
        f"evaluations/{rainfed_request.evaluation_id}/scenarios/rainfed/"
        "crops/maize/crop_suitability.tif"
    )
    assert irrigated.artifacts[0].storage_reference == (
        f"evaluations/{rainfed_request.evaluation_id}/scenarios/irrigated/"
        "crops/maize/crop_suitability.tif"
    )
    assert rainfed.artifacts[0].storage_reference != irrigated.artifacts[0].storage_reference


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


def _write_limitation_engine(
    engine_root: Path,
    *,
    values: list[list[int]],
    areas: list[list[float]],
    info_lines: tuple[str, ...] = (
        "value - limiting factor",
        "0 - temperature",
        "1 - precipitation",
        "2 - climate variability",
        "3 - photoperiod",
        "4 - base saturation",
    ),
    include_limitation_artifact: bool = True,
    vary_by_irrigation: bool = False,
) -> None:
    source_root = engine_root / "src"
    source_root.mkdir(parents=True, exist_ok=True)
    (source_root / "__init__.py").write_text("", encoding="utf-8")
    source = f'''\
from pathlib import Path
import configparser
import numpy as np
import rasterio
from rasterio.transform import from_origin

VALUES = np.array({values!r}, dtype="int16")
AREAS = np.array({areas!r}, dtype="float64")
INFO_LINES = {list(info_lines)!r}
INCLUDE_LIMITATION_ARTIFACT = {include_limitation_artifact!r}
VARY_BY_IRRIGATION = {vary_by_irrigation!r}


def load_geometry(path):
    return Path(path)


def cell_areas(geometry, shape, transform, crs):
    del geometry, transform, crs
    assert tuple(shape) == tuple(AREAS.shape)
    return AREAS.copy(), float(AREAS.sum())


def _write_raster(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=data.shape[0],
        width=data.shape[1],
        count=1,
        dtype="int16",
        crs="EPSG:4326",
        transform=from_origin(-77.5, -11.0, 0.01, 0.01),
        nodata=-1,
    ) as dataset:
        dataset.write(data, 1)


def run_evaluation(
    crops,
    parcel_path,
    output_root=None,
    source_config=None,
    catalog=None,
    max_workers=2,
    progress=None,
):
    del parcel_path, catalog, max_workers, progress
    output_root = Path(output_root)
    result_directory = output_root / "engine-result"
    values = VALUES.copy()
    if VARY_BY_IRRIGATION:
        parser = configparser.ConfigParser()
        parser.read(source_config, encoding="utf-8")
        irrigation = parser.getint("options", "irrigation")
        values[:] = 1 if irrigation else 0

    _write_raster(
        result_directory / "crop_suitability.tif",
        np.full(values.shape, 72, dtype="int16"),
    )
    if INCLUDE_LIMITATION_ARTIFACT:
        _write_raster(result_directory / "crop_limiting_factor.tif", values)
        (result_directory / "limiting_factor.inf").write_text(
            "\\n".join(INFO_LINES) + "\\n",
            encoding="utf-8",
        )

    return {{
        "evaluation_id": "fake_scientific_process",
        "created_at": "2026-09-17T12:00:00+00:00",
        "finished_at": "2026-09-17T12:00:01+00:00",
        "selected_crops": list(crops),
        "execution": "sequential_isolated_processes",
        "parcel_sha256": "parcel-sha256",
        "source_sha256": {{
            "/science/environment.tif": "{'a' * 64}"
        }},
        "source_files_unchanged": True,
        "crops": [{{
            "id": crops[0],
            "status": "succeeded",
            "parameter_sha256": "parameter-sha256",
            "config_sha256": "configuration-sha256",
            "elapsed_seconds": 0.1,
            "result_directory": str(result_directory),
            "scores": {{
                "crop_suitability": {{
                    "mean": 72.0,
                    "minimum": 72.0,
                    "maximum": 72.0,
                    "valid_cells": int(values.size),
                    "valid_area_m2": float(AREAS[AREAS > 0].sum()),
                    "coverage_fraction": 1.0,
                    "zero_suitability_area_m2": 0.0,
                }}
            }},
        }}],
    }}
'''
    (source_root / "multicrop.py").write_text(source, encoding="utf-8")


def _real_limitation_adapter(tmp_path: Path, request: CropSuitabilityRequest) -> CropSuiteAdapter:
    return CropSuiteAdapter(
        engine_root=tmp_path / "engine",
        workspace_root=tmp_path / "workspace",
        python_executable=Path(sys.executable),
        max_workers=1,
        input_integrity_verifier=_integrity_verifier(request.environmental_input_manifest),
        artifact_store=FilesystemScientificArtifactStore(tmp_path / "artifacts"),
    )


def test_real_execution_extracts_same_run_limiting_factor_evidence(tmp_path: Path) -> None:
    request = _request()
    _write_limitation_engine(
        tmp_path / "engine",
        values=[[0, 1, 2], [3, 4, -1]],
        areas=[[10.0, 20.0, 30.0], [40.0, 50.0, 999.0]],
    )

    result = _real_limitation_adapter(tmp_path, request).evaluate(request)

    assert result.status is CropExecutionStatus.SUCCEEDED
    assert result.limitation_evidence.availability is LimitationEvidenceAvailability.AVAILABLE
    assert result.limitation_evidence.warnings == ()
    factors = {factor.raw_code: factor for factor in result.limitation_evidence.factors}
    assert {code: factor.factor_code for code, factor in factors.items()} == {
        0: "temperature",
        1: "precipitation",
        2: "crop_failure_frequency",
        3: "photoperiod",
        4: "parameter_base_saturation",
    }
    assert factors[4].affected_area_m2 == pytest.approx(50.0)
    assert factors[4].affected_fraction == pytest.approx(50.0 / 150.0)
    assert factors[4].dominant is True
    assert sum(f.affected_fraction for f in factors.values()) == pytest.approx(1.0)
    assert all(f.source_sha256 == factors[4].source_sha256 for f in factors.values())
    assert len(factors[4].source_sha256) == 64
    assert factors[4].source_storage_reference == (
        f"evaluations/{request.evaluation_id}/scenarios/rainfed/"
        "crops/maize/crop_limiting_factor.tif"
    )
    assert {artifact.role for artifact in result.artifacts} == {
        ScientificArtifactRole.CROP_SUITABILITY,
        ScientificArtifactRole.CROP_LIMITING_FACTOR,
    }


def test_real_execution_uses_canonical_parameter_codes_from_inf_labels(
    tmp_path: Path,
) -> None:
    request = _request()
    expected = {
        4: ("base saturation", "parameter_base_saturation"),
        5: ("coarse fragments", "parameter_coarse_fragments"),
        6: ("gypsum", "parameter_gypsum"),
        7: ("soil ph", "parameter_ph"),
        8: ("salinity", "parameter_salinity"),
        9: ("texture", "parameter_texture"),
        10: ("soil organic carbon", "parameter_soil_organic_carbon"),
        11: ("sodicity", "parameter_sodicity"),
        12: ("soildepth", "parameter_soildepth"),
        13: ("slope", "parameter_slope"),
    }
    _write_limitation_engine(
        tmp_path / "engine",
        values=[list(expected)],
        areas=[[1.0] * len(expected)],
        info_lines=(
            "value - limiting factor",
            "0 - temperature",
            "1 - precipitation",
            "2 - climate variability",
            "3 - photoperiod",
            *(f"{code} - {label}" for code, (label, _) in expected.items()),
        ),
    )

    result = _real_limitation_adapter(tmp_path, request).evaluate(request)

    factors = {factor.raw_code: factor for factor in result.limitation_evidence.factors}
    assert {code: factor.factor_code for code, factor in factors.items()} == {
        code: factor_code for code, (_, factor_code) in expected.items()
    }
    assert {code: factor.label for code, factor in factors.items()} == {
        code: label for code, (label, _) in expected.items()
    }


def test_real_inf_header_does_not_warn_for_fixed_precipitation_code(tmp_path: Path) -> None:
    request = _request()
    _write_limitation_engine(
        tmp_path / "engine",
        values=[[1]],
        areas=[[25.0]],
        info_lines=(
            "value - limiting factor",
            "0 - temperature",
            "1 - precipitation",
            "2 - climate variability",
            "3 - photoperiod",
        ),
    )

    result = _real_limitation_adapter(tmp_path, request).evaluate(request)

    evidence = result.limitation_evidence
    assert evidence.availability is LimitationEvidenceAvailability.AVAILABLE
    assert evidence.reason is None
    assert evidence.warnings == ()
    assert len(evidence.factors) == 1
    assert evidence.factors[0].raw_code == 1
    assert evidence.factors[0].factor_code == "precipitation"


@pytest.mark.parametrize("raw_code", [4, 12, 19])
def test_real_inf_dynamic_code_is_derived_from_same_run_label(
    tmp_path: Path,
    raw_code: int,
) -> None:
    request = _request()
    _write_limitation_engine(
        tmp_path / "engine",
        values=[[raw_code]],
        areas=[[25.0]],
        info_lines=(
            "value - limiting factor",
            "0 - temperature",
            "1 - precipitation",
            "2 - climate variability",
            "3 - photoperiod",
            f"{raw_code} - soildepth",
        ),
    )

    result = _real_limitation_adapter(tmp_path, request).evaluate(request)

    evidence = result.limitation_evidence
    assert evidence.availability is LimitationEvidenceAvailability.AVAILABLE
    assert evidence.reason is None
    assert evidence.warnings == ()
    assert len(evidence.factors) == 1
    assert evidence.factors[0].raw_code == raw_code
    assert evidence.factors[0].factor_code == "parameter_soildepth"
    assert evidence.factors[0].label == "soildepth"


def test_real_inf_invalid_mapping_code_remains_a_real_warning(tmp_path: Path) -> None:
    request = _request()
    _write_limitation_engine(
        tmp_path / "engine",
        values=[[1]],
        areas=[[25.0]],
        info_lines=(
            "value - limiting factor",
            "0 - temperature",
            "1 - precipitation",
            "2 - climate variability",
            "3 - photoperiod",
            "invalid - soildepth",
        ),
    )

    result = _real_limitation_adapter(tmp_path, request).evaluate(request)

    evidence = result.limitation_evidence
    assert evidence.availability is LimitationEvidenceAvailability.PARTIAL
    assert evidence.reason == "limiting_factor_evidence_warnings"
    assert evidence.warnings == ("limiting_factor_inf_invalid_code:6",)


def test_real_execution_allows_tied_dominant_limiting_factors(tmp_path: Path) -> None:
    request = _request()
    _write_limitation_engine(
        tmp_path / "engine",
        values=[[0, 1]],
        areas=[[25.0, 25.0]],
    )

    result = _real_limitation_adapter(tmp_path, request).evaluate(request)

    assert [
        factor.raw_code
        for factor in result.limitation_evidence.factors
        if factor.dominant
    ] == [0, 1]


def test_real_execution_preserves_unknown_raw_limiting_factor(tmp_path: Path) -> None:
    request = _request()
    _write_limitation_engine(
        tmp_path / "engine",
        values=[[99]],
        areas=[[25.0]],
        info_lines=("0 - temperature",),
    )

    result = _real_limitation_adapter(tmp_path, request).evaluate(request)

    evidence = result.limitation_evidence
    assert evidence.availability is LimitationEvidenceAvailability.PARTIAL
    assert evidence.reason == "limiting_factor_evidence_warnings"
    assert evidence.warnings == ("unsupported_limiting_factor_raw_code:99",)
    assert len(evidence.factors) == 1
    factor = evidence.factors[0]
    assert factor.raw_code == 99
    assert factor.factor_code == "unknown_raw_99"
    assert factor.label == "unsupported_raw_code_99"


def test_missing_limiting_factor_artifact_does_not_fail_suitability(tmp_path: Path) -> None:
    request = _request()
    _write_limitation_engine(
        tmp_path / "engine",
        values=[[0]],
        areas=[[25.0]],
        include_limitation_artifact=False,
    )

    result = _real_limitation_adapter(tmp_path, request).evaluate(request)

    assert result.status is CropExecutionStatus.SUCCEEDED
    assert result.suitability is not None
    assert result.limitation_evidence.availability is LimitationEvidenceAvailability.UNAVAILABLE
    assert result.limitation_evidence.reason == "crop_limiting_factor_artifact_missing"
    assert [artifact.role for artifact in result.artifacts] == [
        ScientificArtifactRole.CROP_SUITABILITY
    ]


def test_rainfed_and_irrigated_limitation_evidence_are_independent(tmp_path: Path) -> None:
    rainfed_request = _request(water_regime=WaterRegime.RAINFED)
    irrigated_request = replace(rainfed_request, water_regime=WaterRegime.IRRIGATED)
    _write_limitation_engine(
        tmp_path / "engine",
        values=[[0]],
        areas=[[25.0]],
        vary_by_irrigation=True,
    )
    adapter = _real_limitation_adapter(tmp_path, rainfed_request)

    rainfed = adapter.evaluate(rainfed_request)
    irrigated = adapter.evaluate(irrigated_request)

    assert rainfed.limitation_evidence.factors[0].factor_code == "temperature"
    assert irrigated.limitation_evidence.factors[0].factor_code == "precipitation"
    assert rainfed.limitation_evidence.factors[0].source_storage_reference != (
        irrigated.limitation_evidence.factors[0].source_storage_reference
    )
