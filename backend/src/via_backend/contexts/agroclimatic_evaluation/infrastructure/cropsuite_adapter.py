"""Infrastructure adapter for the existing CropSuiteLite multicrop service."""

from __future__ import annotations

import configparser
import json
import re
import shutil
import subprocess
import tempfile
from collections.abc import Callable, Mapping
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from ..application.ports import (
    CropExecutionStatus,
    CropLimitationEvidence,
    CropSuitabilityExecutionError,
    CropSuitabilityRequest,
    CropSuitabilityResult,
    IEnvironmentalInputIntegrityVerifier,
    InvalidEngineOutputError,
    LimitationEvidenceAvailability,
    LimitingFactorEvidence,
    ScientificArtifactDescriptor,
    ScientificArtifactGrid,
    ScientificArtifactRole,
    ScientificExecutionFailure,
    ScientificExecutionTrace,
    ScientificSourceFingerprint,
    SuitabilityScoreSummary,
)
from ..domain.water_regime import WaterRegime
from .scientific_artifact_store import (
    ScientificArtifactStorageError,
    ScientificArtifactStore,
)

EngineRunner = Callable[..., Mapping[str, Any]]
_SAFE_CROP_ID = re.compile(r"^[A-Za-z0-9_-]+$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_DEFAULT_SOURCE_CONFIG = "config_access_esm1_5_ssp126_2021_2040.ini"

_SCIENTIFIC_BRIDGE = """
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path

engine_root = Path(sys.argv[1]).resolve()
invocation_path = Path(sys.argv[2]).resolve()
result_path = Path(sys.argv[3]).resolve()

sys.path.insert(0, str(engine_root))

from src.multicrop import run_evaluation

payload = json.loads(invocation_path.read_text(encoding="utf-8"))
collect_artifact_metadata = bool(
    payload.pop("_via_collect_artifact_metadata", False)
)

for key in ("parcel_path", "output_root", "source_config", "catalog"):
    if key in payload and payload[key] is not None:
        payload[key] = Path(payload[key])

report = run_evaluation(**payload)

if collect_artifact_metadata:
    import numpy as np
    import rasterio
    from src.multicrop import cell_areas, load_geometry

    def sha256(path):
        digest = hashlib.sha256()
        with path.open("rb") as artifact:
            for chunk in iter(lambda: artifact.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def parse_limiting_factor_info(path):
        parsed = {}
        warnings = []
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = path.read_text(encoding="latin-1").splitlines()
        for line_number, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.casefold() == "value - limiting factor":
                continue
            parts = stripped.split(" - ", 1)
            if len(parts) != 2:
                warnings.append(
                    f"limiting_factor_inf_unparseable_line:{line_number}"
                )
                continue
            raw_code_text, label = parts
            try:
                raw_code = int(raw_code_text.strip())
            except ValueError:
                warnings.append(
                    f"limiting_factor_inf_invalid_code:{line_number}"
                )
                continue
            label = label.strip()
            if not label:
                warnings.append(
                    f"limiting_factor_inf_empty_label:{line_number}"
                )
                continue
            if raw_code in parsed:
                warnings.append(
                    f"limiting_factor_inf_duplicate_code:{raw_code}"
                )
                continue
            parsed[raw_code] = label
        return parsed, warnings

    def stable_factor_code(raw_code, label):
        fixed_climate_factors = {
            0: "temperature",
            1: "precipitation",
            2: "crop_failure_frequency",
            3: "photoperiod",
        }
        if raw_code in fixed_climate_factors:
            return fixed_climate_factors[raw_code]

        normalized = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
        parameter_aliases = {
            "base_saturation": "parameter_base_saturation",
            "base_saturation_percentage": "parameter_base_saturation",
            "saturation_of_bases": "parameter_base_saturation",
            "coarse_fragments": "parameter_coarse_fragments",
            "rock_fragments": "parameter_coarse_fragments",
            "gypsum": "parameter_gypsum",
            "gypsum_content": "parameter_gypsum",
            "ph": "parameter_ph",
            "soil_ph": "parameter_ph",
            "salinity": "parameter_salinity",
            "soil_salinity": "parameter_salinity",
            "texture": "parameter_texture",
            "soil_texture": "parameter_texture",
            "soil_organic_carbon": "parameter_soil_organic_carbon",
            "organic_carbon": "parameter_soil_organic_carbon",
            "sodicity": "parameter_sodicity",
            "soil_sodicity": "parameter_sodicity",
            "soildepth": "parameter_soildepth",
            "soil_depth": "parameter_soildepth",
            "slope": "parameter_slope",
            "terrain_slope": "parameter_slope",
        }
        if normalized in parameter_aliases:
            return parameter_aliases[normalized]
        if normalized:
            return f"parameter_{normalized}"
        return f"parameter_raw_{raw_code}"

    def collect_limitation_metadata(crop, parcel_path):
        result_directory = Path(crop["result_directory"]).resolve()
        raster_path = result_directory / "crop_limiting_factor.tif"
        info_path = result_directory / "limiting_factor.inf"
        if not raster_path.is_file():
            return {
                "availability": "unavailable",
                "reason": "crop_limiting_factor_artifact_missing",
                "warnings": [],
                "factors": [],
            }, None
        if not info_path.is_file():
            return {
                "availability": "unavailable",
                "reason": "limiting_factor_mapping_missing",
                "warnings": [],
                "factors": [],
            }, None

        mapping, warnings = parse_limiting_factor_info(info_path)
        raster_sha256 = sha256(raster_path)
        with rasterio.open(raster_path) as dataset:
            if dataset.crs is None:
                return {
                    "availability": "unavailable",
                    "reason": "crop_limiting_factor_crs_missing",
                    "warnings": warnings,
                    "factors": [],
                }, None
            nodata = dataset.nodata
            if nodata is not None:
                nodata = float(nodata)
                if not math.isfinite(nodata):
                    return {
                        "availability": "unavailable",
                        "reason": "crop_limiting_factor_nodata_invalid",
                        "warnings": warnings,
                        "factors": [],
                    }, None
            values = dataset.read(1).astype("float64", copy=False)
            parcel_geometry = load_geometry(parcel_path)
            areas, _parcel_area = cell_areas(
                parcel_geometry,
                dataset.shape,
                dataset.transform,
                dataset.crs,
            )
            areas = np.asarray(areas, dtype="float64")
            valid = np.isfinite(values) & np.isfinite(areas) & (areas > 0)
            if nodata is not None:
                valid &= values != nodata
            if not np.any(valid):
                transform = dataset.transform
                return {
                    "availability": "unavailable",
                    "reason": "no_valid_explanatory_area",
                    "warnings": warnings,
                    "factors": [],
                }, {
                    "sha256": raster_sha256,
                    "grid": {
                        "crs": dataset.crs.to_string(),
                        "width": dataset.width,
                        "height": dataset.height,
                        "transform": [
                            transform.a,
                            transform.b,
                            transform.c,
                            transform.d,
                            transform.e,
                            transform.f,
                        ],
                        "nodata": nodata,
                    },
                }

            total_valid_area = float(np.sum(areas[valid]))
            aggregates = {}
            for raw_value, area in zip(values[valid], areas[valid], strict=True):
                rounded = int(round(float(raw_value)))
                if not math.isclose(float(raw_value), rounded, abs_tol=1e-9):
                    warnings.append(
                        f"crop_limiting_factor_noninteger_value:{raw_value}"
                    )
                    continue
                entry = aggregates.setdefault(
                    rounded,
                    {"affected_cells": 0, "affected_area_m2": 0.0},
                )
                entry["affected_cells"] += 1
                entry["affected_area_m2"] += float(area)

            factors = []
            for raw_code in sorted(aggregates):
                aggregate = aggregates[raw_code]
                label = mapping.get(raw_code)
                if label is None:
                    label = f"unsupported_raw_code_{raw_code}"
                    factor_code = f"unknown_raw_{raw_code}"
                    warnings.append(
                        f"unsupported_limiting_factor_raw_code:{raw_code}"
                    )
                else:
                    factor_code = stable_factor_code(raw_code, label)
                affected_area = float(aggregate["affected_area_m2"])
                factors.append(
                    {
                        "factor_code": factor_code,
                        "label": label,
                        "raw_code": raw_code,
                        "affected_cells": int(aggregate["affected_cells"]),
                        "affected_area_m2": affected_area,
                        "affected_fraction": (
                            affected_area / total_valid_area
                            if total_valid_area > 0
                            else 0.0
                        ),
                        "dominant": False,
                        "source_sha256": raster_sha256,
                    }
                )

            if not factors:
                availability = "unavailable"
                reason = "no_supported_explanatory_cells"
            else:
                max_area = max(factor["affected_area_m2"] for factor in factors)
                tolerance = max(1e-9, abs(max_area) * 1e-12)
                for factor in factors:
                    factor["dominant"] = math.isclose(
                        factor["affected_area_m2"],
                        max_area,
                        rel_tol=1e-12,
                        abs_tol=tolerance,
                    )
                availability = "partial" if warnings else "available"
                reason = "limiting_factor_evidence_warnings" if warnings else None

            transform = dataset.transform
            artifact_metadata = {
                "sha256": raster_sha256,
                "grid": {
                    "crs": dataset.crs.to_string(),
                    "width": dataset.width,
                    "height": dataset.height,
                    "transform": [
                        transform.a,
                        transform.b,
                        transform.c,
                        transform.d,
                        transform.e,
                        transform.f,
                    ],
                    "nodata": nodata,
                },
            }
            return {
                "availability": availability,
                "reason": reason,
                "warnings": sorted(set(warnings)),
                "factors": factors,
            }, artifact_metadata

    for crop in report.get("crops", []):
        if crop.get("status") not in {"succeeded", "no_coverage"}:
            continue

        result_directory = Path(crop["result_directory"]).resolve()
        artifact_path = result_directory / "crop_suitability.tif"

        if not artifact_path.is_file():
            raise RuntimeError(
                "CropSuiteLite did not preserve crop_suitability.tif."
            )

        with rasterio.open(artifact_path) as dataset:
            if dataset.crs is None:
                raise RuntimeError(
                    "crop_suitability.tif does not declare a CRS."
                )

            nodata = dataset.nodata
            if nodata is not None:
                nodata = float(nodata)
                if not math.isfinite(nodata):
                    raise RuntimeError(
                        "crop_suitability.tif declares a non-finite nodata value."
                    )

            transform = dataset.transform

            crop["via_artifact"] = {
                "sha256": sha256(artifact_path),
                "grid": {
                    "crs": dataset.crs.to_string(),
                    "width": dataset.width,
                    "height": dataset.height,
                    "transform": [
                        transform.a,
                        transform.b,
                        transform.c,
                        transform.d,
                        transform.e,
                        transform.f,
                    ],
                    "nodata": nodata,
                },
            }

        try:
            limitation_evidence, limitation_artifact = collect_limitation_metadata(
                crop,
                payload["parcel_path"],
            )
        except Exception as error:
            limitation_evidence = {
                "availability": "unavailable",
                "reason": "limiting_factor_extraction_failed",
                "warnings": [
                    f"limiting_factor_extraction_failed:{type(error).__name__}"
                ],
                "factors": [],
            }
            limitation_artifact = None
        crop["via_limitation_evidence"] = limitation_evidence
        if limitation_artifact is not None:
            crop["via_limitation_artifact"] = limitation_artifact

result_path.write_text(
    json.dumps(report, ensure_ascii=False, allow_nan=False),
    encoding="utf-8",
)
""".strip()


class CropSuiteAdapter:
    """Map a VIA snapshot to the preserved blocking CropSuiteLite capability."""

    def __init__(
        self,
        *,
        engine_root: Path,
        workspace_root: Path,
        source_config: Path | None = None,
        catalog: Path | None = None,
        max_workers: int = 1,
        python_executable: Path | None = None,
        runner: EngineRunner | None = None,
        artifact_store: ScientificArtifactStore | None = None,
        input_integrity_verifier: IEnvironmentalInputIntegrityVerifier | None = None,
    ) -> None:
        if isinstance(max_workers, bool) or max_workers < 1:
            raise ValueError("max_workers must be a positive integer.")

        self._python_executable = (
            python_executable.resolve() if python_executable is not None else None
        )
        self._engine_root = engine_root.resolve()
        self._workspace_root = workspace_root.resolve()
        if _is_within(self._workspace_root, self._engine_root):
            raise ValueError(
                "CropSuite execution workspace must be outside the engine source tree."
            )

        self._source_config = (
            source_config.resolve()
            if source_config is not None
            else (self._engine_root / _DEFAULT_SOURCE_CONFIG).resolve()
        )
        self._catalog = catalog.resolve() if catalog else None
        self._max_workers = max_workers
        self._artifact_store = artifact_store
        self._runner = runner
        self._input_integrity_verifier = input_integrity_verifier

        if self._runner is None:
            if self._input_integrity_verifier is None:
                raise ValueError(
                    "input_integrity_verifier is required for real scientific execution."
                )
            if self._python_executable is None:
                raise ValueError(
                    "python_executable is required for real scientific execution."
                )
            if not self._python_executable.is_file():
                raise ValueError(
                    f"Scientific Python executable was not found at "
                    f"{self._python_executable}."
                )

    def evaluate(self, request: CropSuitabilityRequest) -> CropSuitabilityResult:
        if not _SAFE_CROP_ID.fullmatch(request.crop_id):
            raise CropSuitabilityExecutionError("Crop identifier is not safe for engine execution.")

        self._workspace_root.mkdir(parents=True, exist_ok=True)
        request_workspace = Path(
            tempfile.mkdtemp(
                prefix=(
                    f"{request.evaluation_id}_{request.crop_id}_"
                    f"{request.water_regime.value}_"
                ),
                dir=self._workspace_root,
            )
        )
        parcel_path = request_workspace / "parcel.geojson"
        parcel_path.write_text(
            json.dumps(
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": request.parcel_snapshot.geometry.to_geojson(),
                },
                ensure_ascii=False,
                allow_nan=False,
            ),
            encoding="utf-8",
        )

        scenario_config = _materialize_scenario_config(
            base_config=self._source_config,
            request_workspace=request_workspace,
            water_regime=request.water_regime,
        )

        arguments: dict[str, Any] = {
            "crops": (request.crop_id,),
            "parcel_path": parcel_path,
            "output_root": request_workspace / "outputs",
            "max_workers": self._max_workers,
            "source_config": scenario_config,
        }
        if self._catalog is not None:
            arguments["catalog"] = self._catalog

        try:
            if self._runner is not None:
                report = self._runner(**arguments)
            else:
                report = self._run_scientific_process(
                    arguments,
                    request_workspace=request_workspace,
                )
        except CropSuitabilityExecutionError:
            raise
        except Exception as error:
            message = (
                "CropSuiteLite did not produce an evaluation report: "
                f"{type(error).__name__}: {error}"
            )
            raise CropSuitabilityExecutionError(message) from error

        source_fingerprints: tuple[ScientificSourceFingerprint, ...] = ()
        if self._input_integrity_verifier is not None:
            source_fingerprints = _parse_source_fingerprints(report)
            self._input_integrity_verifier.verify(
                request.environmental_input_manifest,
                source_fingerprints,
            )

        result = _map_report(
            report,
            request.crop_id,
            request.water_regime,
            source_fingerprints=source_fingerprints,
        )

        if result.status is CropExecutionStatus.FAILED:
            return result

        if self._artifact_store is None:
            return result

        try:
            artifact = _publish_crop_suitability_artifact(
                report=report,
                crop_id=request.crop_id,
                evaluation_id=str(request.evaluation_id),
                water_regime=request.water_regime,
                request_workspace=request_workspace,
                artifact_store=self._artifact_store,
            )
        except ScientificArtifactStorageError as error:
            raise CropSuitabilityExecutionError(
                f"Scientific artifact publication failed: {error}"
            ) from error

        limitation_artifact: ScientificArtifactDescriptor | None = None
        limitation_evidence = result.limitation_evidence
        try:
            limitation_artifact = _publish_crop_limiting_factor_artifact(
                report=report,
                crop_id=request.crop_id,
                evaluation_id=str(request.evaluation_id),
                water_regime=request.water_regime,
                request_workspace=request_workspace,
                artifact_store=self._artifact_store,
            )
        except Exception as error:
            limitation_evidence = _degrade_limitation_publication(
                limitation_evidence,
                error,
            )
        else:
            if limitation_artifact is not None:
                limitation_evidence = _with_published_limitation_source(
                    limitation_evidence,
                    limitation_artifact,
                )

        artifacts = (
            (artifact, limitation_artifact)
            if limitation_artifact is not None
            else (artifact,)
        )
        return CropSuitabilityResult(
            crop_id=result.crop_id,
            status=result.status,
            suitability=result.suitability,
            failure=result.failure,
            trace=result.trace,
            artifacts=artifacts,
            water_regime=result.water_regime,
            limitation_evidence=limitation_evidence,
        )

    def _run_scientific_process(
        self,
        arguments: Mapping[str, Any],
        *,
        request_workspace: Path,
    ) -> Mapping[str, Any]:
        if self._python_executable is None:
            raise CropSuitabilityExecutionError(
                "Scientific Python executable is not configured."
            )

        invocation_path = request_workspace / "invocation.json"
        result_path = request_workspace / "process-report.json"
        log_path = request_workspace / "process.log"
        bridge_path = request_workspace / "run_cropsuite_bridge.py"

        payload: dict[str, Any] = {
            "crops": list(arguments["crops"]),
            "parcel_path": str(arguments["parcel_path"]),
            "output_root": str(arguments["output_root"]),
            "max_workers": arguments["max_workers"],
            "_via_collect_artifact_metadata": self._artifact_store is not None,
        }

        if "source_config" in arguments:
            payload["source_config"] = str(arguments["source_config"])
        if "catalog" in arguments:
            payload["catalog"] = str(arguments["catalog"])

        invocation_path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                allow_nan=False,
            ),
            encoding="utf-8",
        )

        bridge_path.write_text(
            _SCIENTIFIC_BRIDGE,
            encoding="utf-8",
        )

        with log_path.open("w", encoding="utf-8") as log:
            completed = subprocess.run(
                [
                    str(self._python_executable),
                    "-B",
                    str(bridge_path),
                    str(self._engine_root),
                    str(invocation_path),
                    str(result_path),
                ],
                cwd=request_workspace,
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=False,
            )

        if completed.returncode != 0:
            raise CropSuitabilityExecutionError(
                "Scientific Python process exited with code "
                f"{completed.returncode}."
            )

        if not result_path.is_file():
            raise CropSuitabilityExecutionError(
                "Scientific Python process did not produce a report."
            )

        try:
            report = json.loads(result_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise CropSuitabilityExecutionError(
                "Scientific Python process produced invalid JSON."
            ) from error

        if not isinstance(report, Mapping):
            raise CropSuitabilityExecutionError(
                "Scientific Python process report must be an object."
            )

        return cast(Mapping[str, Any], report)


def _parse_source_fingerprints(
    report: Mapping[str, Any],
) -> tuple[ScientificSourceFingerprint, ...]:
    raw = report.get("source_sha256")
    if not isinstance(raw, Mapping) or not raw:
        raise InvalidEngineOutputError(
            "Engine report field 'source_sha256' must be a non-empty object."
        )

    fingerprints: list[ScientificSourceFingerprint] = []
    for source_reference, sha256 in raw.items():
        if not isinstance(source_reference, str) or not source_reference:
            raise InvalidEngineOutputError(
                "Engine source_sha256 keys must be non-empty strings."
            )
        if not isinstance(sha256, str) or _SHA256.fullmatch(sha256) is None:
            raise InvalidEngineOutputError(
                "Engine source_sha256 values must be lowercase hexadecimal SHA-256."
            )
        fingerprints.append(ScientificSourceFingerprint(source_reference, sha256))

    return tuple(sorted(fingerprints, key=lambda item: item.source_reference))


def _map_report(
    report: Mapping[str, Any],
    crop_id: str,
    water_regime: WaterRegime = WaterRegime.RAINFED,
    *,
    source_fingerprints: tuple[ScientificSourceFingerprint, ...] = (),
) -> CropSuitabilityResult:
    selected = _sequence(report, "selected_crops")
    crops = _sequence(report, "crops")
    if list(selected) != [crop_id]:
        raise InvalidEngineOutputError(
            "Engine report did not preserve the requested crop identity."
        )
    if len(crops) != 1 or not isinstance(crops[0], Mapping):
        raise InvalidEngineOutputError("Engine report must contain exactly one per-crop outcome.")

    crop = cast(Mapping[str, Any], crops[0])
    if crop.get("id") != crop_id:
        raise InvalidEngineOutputError(
            "Engine outcome did not preserve the requested crop identity."
        )
    raw_status = crop.get("status")
    try:
        status = CropExecutionStatus(raw_status)
    except ValueError as error:
        raise InvalidEngineOutputError(
            f"Unknown per-crop engine status: {raw_status!r}."
        ) from error

    source_files_unchanged = _boolean(report, "source_files_unchanged")
    failure: ScientificExecutionFailure | None = None
    suitability: SuitabilityScoreSummary | None = None
    if not source_files_unchanged:
        status = CropExecutionStatus.FAILED
        failure = ScientificExecutionFailure(
            str(report.get("error") or "Scientific source files changed during execution.")
        )
    elif status is CropExecutionStatus.FAILED:
        error_message = crop.get("error")
        if not isinstance(error_message, str) or not error_message:
            raise InvalidEngineOutputError("A failed engine outcome must include an error message.")
        failure = ScientificExecutionFailure(error_message)
    else:
        scores = _mapping(crop, "scores")
        suitability = _map_summary(_mapping(scores, "crop_suitability"))
        if status is CropExecutionStatus.SUCCEEDED and suitability.valid_cells < 1:
            raise InvalidEngineOutputError("Succeeded engine outcome contains no valid cells.")
        if status is CropExecutionStatus.NO_COVERAGE and suitability.valid_cells != 0:
            raise InvalidEngineOutputError("No-coverage engine outcome contains valid cells.")

    trace = ScientificExecutionTrace(
        engine_identifier="CropSuiteLite",
        execution_reference=_string(report, "evaluation_id"),
        started_at=_timestamp(report, "created_at"),
        finished_at=_timestamp(report, "finished_at"),
        elapsed_seconds=_nonnegative_number(crop, "elapsed_seconds"),
        execution_mode=_string(report, "execution"),
        parcel_sha256=_string(report, "parcel_sha256"),
        parameter_sha256=_optional_string(crop, "parameter_sha256"),
        configuration_sha256=_optional_string(crop, "config_sha256"),
        source_files_unchanged=source_files_unchanged,
        source_fingerprints=source_fingerprints,
    )
    limitation_evidence = (
        _map_limitation_evidence(crop)
        if status is not CropExecutionStatus.FAILED
        else CropLimitationEvidence(
            availability=LimitationEvidenceAvailability.UNAVAILABLE,
            reason="crop_execution_failed",
        )
    )
    return CropSuitabilityResult(
        crop_id=crop_id,
        status=status,
        suitability=suitability,
        failure=failure,
        trace=trace,
        water_regime=water_regime,
        limitation_evidence=limitation_evidence,
    )


def _map_limitation_evidence(
    crop: Mapping[str, Any],
) -> CropLimitationEvidence:
    raw = crop.get("via_limitation_evidence")
    if raw is None:
        return CropLimitationEvidence(
            availability=LimitationEvidenceAvailability.UNAVAILABLE,
            reason="limitation_evidence_unavailable",
        )
    if not isinstance(raw, Mapping):
        return CropLimitationEvidence(
            availability=LimitationEvidenceAvailability.UNAVAILABLE,
            reason="invalid_limitation_evidence_metadata",
            warnings=("invalid_limitation_evidence_metadata:not_object",),
        )

    try:
        availability = LimitationEvidenceAvailability(raw.get("availability"))
        reason = raw.get("reason")
        if reason is not None and (not isinstance(reason, str) or not reason.strip()):
            raise ValueError("reason")
        raw_warnings = raw.get("warnings", [])
        raw_factors = raw.get("factors", [])
        if not isinstance(raw_warnings, list) or not all(
            isinstance(item, str) and item.strip() for item in raw_warnings
        ):
            raise ValueError("warnings")
        if not isinstance(raw_factors, list):
            raise ValueError("factors")

        factors: list[LimitingFactorEvidence] = []
        for item in raw_factors:
            if not isinstance(item, Mapping):
                raise ValueError("factor")
            raw_code = item.get("raw_code")
            affected_cells = item.get("affected_cells")
            affected_area_m2 = item.get("affected_area_m2")
            affected_fraction = item.get("affected_fraction")
            dominant = item.get("dominant")
            source_sha256 = item.get("source_sha256")
            factor_code = item.get("factor_code")
            label = item.get("label")
            if isinstance(raw_code, bool) or not isinstance(raw_code, int):
                raise ValueError("raw_code")
            if (
                isinstance(affected_cells, bool)
                or not isinstance(affected_cells, int)
                or affected_cells < 0
            ):
                raise ValueError("affected_cells")
            if (
                isinstance(affected_area_m2, bool)
                or not isinstance(affected_area_m2, (int, float))
                or affected_area_m2 < 0
            ):
                raise ValueError("affected_area_m2")
            if (
                isinstance(affected_fraction, bool)
                or not isinstance(affected_fraction, (int, float))
                or affected_fraction < 0
                or affected_fraction > 1
            ):
                raise ValueError("affected_fraction")
            if not isinstance(dominant, bool):
                raise ValueError("dominant")
            if (
                not isinstance(factor_code, str)
                or not factor_code.strip()
                or not isinstance(label, str)
                or not label.strip()
            ):
                raise ValueError("factor_identity")
            if (
                not isinstance(source_sha256, str)
                or _SHA256.fullmatch(source_sha256) is None
            ):
                raise ValueError("source_sha256")
            factors.append(
                LimitingFactorEvidence(
                    factor_code=factor_code,
                    label=label,
                    raw_code=raw_code,
                    affected_cells=affected_cells,
                    affected_area_m2=float(affected_area_m2),
                    affected_fraction=float(affected_fraction),
                    dominant=dominant,
                    source_storage_reference=None,
                    source_sha256=source_sha256,
                )
            )
    except (TypeError, ValueError):
        return CropLimitationEvidence(
            availability=LimitationEvidenceAvailability.UNAVAILABLE,
            reason="invalid_limitation_evidence_metadata",
            warnings=("invalid_limitation_evidence_metadata:contract",),
        )

    if availability is LimitationEvidenceAvailability.AVAILABLE and not factors:
        return CropLimitationEvidence(
            availability=LimitationEvidenceAvailability.UNAVAILABLE,
            reason="invalid_limitation_evidence_metadata",
            warnings=("invalid_limitation_evidence_metadata:available_without_factors",),
        )
    if availability is LimitationEvidenceAvailability.UNAVAILABLE:
        factors = []
    return CropLimitationEvidence(
        availability=availability,
        reason=cast(str | None, reason),
        warnings=tuple(sorted(set(cast(list[str], raw_warnings)))),
        factors=tuple(factors),
    )


def _with_published_limitation_source(
    evidence: CropLimitationEvidence,
    artifact: ScientificArtifactDescriptor,
) -> CropLimitationEvidence:
    if not evidence.factors:
        return evidence
    return CropLimitationEvidence(
        availability=evidence.availability,
        reason=evidence.reason,
        warnings=evidence.warnings,
        factors=tuple(
            LimitingFactorEvidence(
                factor_code=factor.factor_code,
                label=factor.label,
                raw_code=factor.raw_code,
                affected_cells=factor.affected_cells,
                affected_area_m2=factor.affected_area_m2,
                affected_fraction=factor.affected_fraction,
                dominant=factor.dominant,
                source_storage_reference=artifact.storage_reference,
                source_sha256=artifact.sha256,
            )
            for factor in evidence.factors
        ),
    )


def _degrade_limitation_publication(
    evidence: CropLimitationEvidence,
    error: Exception,
) -> CropLimitationEvidence:
    warning = f"crop_limiting_factor_publication_failed:{type(error).__name__}"
    if not evidence.factors:
        return CropLimitationEvidence(
            availability=evidence.availability,
            reason=evidence.reason,
            warnings=tuple(sorted(set((*evidence.warnings, warning)))),
            factors=(),
        )
    return CropLimitationEvidence(
        availability=LimitationEvidenceAvailability.PARTIAL,
        reason="crop_limiting_factor_artifact_publication_failed",
        warnings=tuple(sorted(set((*evidence.warnings, warning)))),
        factors=evidence.factors,
    )

def _publish_crop_suitability_artifact(
    *,
    report: Mapping[str, Any],
    crop_id: str,
    evaluation_id: str,
    water_regime: WaterRegime,
    request_workspace: Path,
    artifact_store: ScientificArtifactStore,
) -> ScientificArtifactDescriptor:
    crops = _sequence(report, "crops")
    if len(crops) != 1 or not isinstance(crops[0], Mapping):
        raise InvalidEngineOutputError(
            "Engine report must contain exactly one per-crop outcome."
        )

    crop = cast(Mapping[str, Any], crops[0])
    if crop.get("id") != crop_id:
        raise InvalidEngineOutputError(
            "Engine artifact did not preserve the requested crop identity."
        )

    result_directory = Path(_string(crop, "result_directory")).resolve()
    workspace = request_workspace.resolve()

    if not _is_within(result_directory, workspace):
        raise InvalidEngineOutputError(
            "Scientific artifact result directory escapes the request workspace."
        )

    source = (result_directory / "crop_suitability.tif").resolve()

    if not _is_within(source, workspace):
        raise InvalidEngineOutputError(
            "Scientific artifact path escapes the request workspace."
        )

    if not source.is_file():
        raise InvalidEngineOutputError(
            "Scientific crop suitability artifact does not exist."
        )

    artifact_metadata = _mapping(crop, "via_artifact")
    expected_sha256 = _string(artifact_metadata, "sha256")
    if not _SHA256.fullmatch(expected_sha256):
        raise InvalidEngineOutputError(
            "Scientific artifact SHA-256 must be lowercase hexadecimal."
        )

    raw_grid = _mapping(artifact_metadata, "grid")
    raw_transform = _sequence(raw_grid, "transform")
    if len(raw_transform) != 6:
        raise InvalidEngineOutputError(
            "Scientific artifact grid transform must contain six coefficients."
        )

    transform = tuple(
        _number(value, f"transform[{index}]")
        for index, value in enumerate(raw_transform)
    )

    grid = ScientificArtifactGrid(
        crs=_string(raw_grid, "crs"),
        width=_positive_integer(raw_grid, "width"),
        height=_positive_integer(raw_grid, "height"),
        transform=cast(
            tuple[float, float, float, float, float, float],
            transform,
        ),
        nodata=_optional_number(raw_grid, "nodata"),
    )

    storage_reference = (
        f"evaluations/{evaluation_id}/scenarios/{water_regime.value}/"
        f"crops/{crop_id}/crop_suitability.tif"
    )

    published = artifact_store.publish(
        source,
        storage_reference,
        expected_sha256=expected_sha256,
    )

    return ScientificArtifactDescriptor(
        role=ScientificArtifactRole.CROP_SUITABILITY,
        storage_reference=published.storage_reference,
        sha256=published.sha256,
        media_type="image/tiff",
        size_bytes=published.size_bytes,
        grid=grid,
    )


def _publish_crop_limiting_factor_artifact(
    *,
    report: Mapping[str, Any],
    crop_id: str,
    evaluation_id: str,
    water_regime: WaterRegime,
    request_workspace: Path,
    artifact_store: ScientificArtifactStore,
) -> ScientificArtifactDescriptor | None:
    crops = _sequence(report, "crops")
    if len(crops) != 1 or not isinstance(crops[0], Mapping):
        raise InvalidEngineOutputError(
            "Engine report must contain exactly one per-crop outcome."
        )
    crop = cast(Mapping[str, Any], crops[0])
    if crop.get("id") != crop_id:
        raise InvalidEngineOutputError(
            "Engine limiting-factor artifact did not preserve the requested crop identity."
        )
    raw_metadata = crop.get("via_limitation_artifact")
    if raw_metadata is None:
        return None
    if not isinstance(raw_metadata, Mapping):
        raise InvalidEngineOutputError(
            "Scientific limiting-factor artifact metadata must be an object."
        )

    result_directory = Path(_string(crop, "result_directory")).resolve()
    workspace = request_workspace.resolve()
    if not _is_within(result_directory, workspace):
        raise InvalidEngineOutputError(
            "Scientific limiting-factor result directory escapes the request workspace."
        )
    source = (result_directory / "crop_limiting_factor.tif").resolve()
    if not _is_within(source, workspace):
        raise InvalidEngineOutputError(
            "Scientific limiting-factor artifact path escapes the request workspace."
        )
    if not source.is_file():
        raise InvalidEngineOutputError(
            "Scientific crop limiting-factor artifact does not exist."
        )

    expected_sha256 = _string(raw_metadata, "sha256")
    if _SHA256.fullmatch(expected_sha256) is None:
        raise InvalidEngineOutputError(
            "Scientific limiting-factor artifact SHA-256 must be lowercase hexadecimal."
        )
    raw_grid = _mapping(raw_metadata, "grid")
    raw_transform = _sequence(raw_grid, "transform")
    if len(raw_transform) != 6:
        raise InvalidEngineOutputError(
            "Scientific limiting-factor artifact grid transform must contain six coefficients."
        )
    transform = tuple(
        _number(value, f"transform[{index}]")
        for index, value in enumerate(raw_transform)
    )
    grid = ScientificArtifactGrid(
        crs=_string(raw_grid, "crs"),
        width=_positive_integer(raw_grid, "width"),
        height=_positive_integer(raw_grid, "height"),
        transform=cast(
            tuple[float, float, float, float, float, float],
            transform,
        ),
        nodata=_optional_number(raw_grid, "nodata"),
    )
    storage_reference = (
        f"evaluations/{evaluation_id}/scenarios/{water_regime.value}/"
        f"crops/{crop_id}/crop_limiting_factor.tif"
    )
    published = artifact_store.publish(
        source,
        storage_reference,
        expected_sha256=expected_sha256,
    )
    return ScientificArtifactDescriptor(
        role=ScientificArtifactRole.CROP_LIMITING_FACTOR,
        storage_reference=published.storage_reference,
        sha256=published.sha256,
        media_type="image/tiff",
        size_bytes=published.size_bytes,
        grid=grid,
    )


def _materialize_scenario_config(
    *,
    base_config: Path,
    request_workspace: Path,
    water_regime: WaterRegime,
) -> Path:
    if not base_config.is_file():
        raise CropSuitabilityExecutionError(
            f"CropSuite base configuration was not found at {base_config}."
        )

    generated = request_workspace / "cropsuite-scenario.ini"
    shutil.copy2(base_config, generated)

    parser = configparser.ConfigParser(interpolation=None)
    try:
        with generated.open("r", encoding="utf-8") as source:
            parser.read_file(source)
    except (OSError, configparser.Error) as error:
        raise CropSuitabilityExecutionError(
            "CropSuite base configuration could not be parsed."
        ) from error

    if not parser.has_section("options"):
        parser.add_section("options")
    parser.set(
        "options",
        "irrigation",
        "0" if water_regime is WaterRegime.RAINFED else "1",
    )

    try:
        with generated.open("w", encoding="utf-8", newline="\n") as target:
            parser.write(target, space_around_delimiters=True)
    except OSError as error:
        raise CropSuitabilityExecutionError(
            "CropSuite scenario configuration could not be materialized."
        ) from error

    return generated

def _map_summary(summary: Mapping[str, Any]) -> SuitabilityScoreSummary:
    return SuitabilityScoreSummary(
        mean=_optional_number(summary, "mean"),
        minimum=_optional_number(summary, "minimum"),
        maximum=_optional_number(summary, "maximum"),
        valid_cells=_nonnegative_integer(summary, "valid_cells"),
        valid_area_m2=_nonnegative_number(summary, "valid_area_m2"),
        coverage_fraction=_fraction(summary, "coverage_fraction"),
        zero_suitability_area_m2=_nonnegative_number(summary, "zero_suitability_area_m2"),
    )


def _mapping(value: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    item = value.get(key)
    if not isinstance(item, Mapping):
        raise InvalidEngineOutputError(f"Engine report field {key!r} must be an object.")
    return item


def _sequence(value: Mapping[str, Any], key: str) -> list[Any] | tuple[Any, ...]:
    item = value.get(key)
    if not isinstance(item, (list, tuple)):
        raise InvalidEngineOutputError(f"Engine report field {key!r} must be an array.")
    return item


def _string(value: Mapping[str, Any], key: str) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item:
        raise InvalidEngineOutputError(f"Engine report field {key!r} must be a string.")
    return item


def _optional_string(value: Mapping[str, Any], key: str) -> str | None:
    item = value.get(key)
    if item is None:
        return None
    if not isinstance(item, str) or not item:
        raise InvalidEngineOutputError(f"Engine report field {key!r} must be a string or null.")
    return item


def _boolean(value: Mapping[str, Any], key: str) -> bool:
    item = value.get(key)
    if not isinstance(item, bool):
        raise InvalidEngineOutputError(f"Engine report field {key!r} must be boolean.")
    return item


def _timestamp(value: Mapping[str, Any], key: str) -> datetime:
    raw = _string(value, key)
    try:
        timestamp = datetime.fromisoformat(raw)
    except ValueError as error:
        raise InvalidEngineOutputError(f"Engine report field {key!r} is not ISO-8601.") from error
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise InvalidEngineOutputError(f"Engine report field {key!r} must be timezone-aware.")
    return timestamp


def _optional_number(value: Mapping[str, Any], key: str) -> float | None:
    item = value.get(key)
    if item is None:
        return None
    return _number(item, key)


def _nonnegative_number(value: Mapping[str, Any], key: str) -> float:
    number = _number(value.get(key), key)
    if number < 0:
        raise InvalidEngineOutputError(f"Engine report field {key!r} must be non-negative.")
    return number


def _fraction(value: Mapping[str, Any], key: str) -> float:
    number = _nonnegative_number(value, key)
    if number > 1:
        raise InvalidEngineOutputError(f"Engine report field {key!r} must be between 0 and 1.")
    return number

def _positive_integer(value: Mapping[str, Any], key: str) -> int:
    item = value.get(key)
    if isinstance(item, bool) or not isinstance(item, int) or item < 1:
        raise InvalidEngineOutputError(
            f"Engine report field {key!r} must be a positive integer."
        )
    return item

def _nonnegative_integer(value: Mapping[str, Any], key: str) -> int:
    item = value.get(key)
    if isinstance(item, bool) or not isinstance(item, int) or item < 0:
        raise InvalidEngineOutputError(
            f"Engine report field {key!r} must be a non-negative integer."
        )
    return item


def _number(item: Any, key: str) -> float:
    if isinstance(item, bool) or not isinstance(item, (int, float)):
        raise InvalidEngineOutputError(f"Engine report field {key!r} must be numeric.")
    number = float(item)
    if not (-float("inf") < number < float("inf")):
        raise InvalidEngineOutputError(f"Engine report field {key!r} must be finite.")
    return number


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True
