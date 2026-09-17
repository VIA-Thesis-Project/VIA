"""Infrastructure adapter for CropSuiteLite common-support comparison."""

from __future__ import annotations

import json
import math
import re
import subprocess
import tempfile
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, cast

from ..application.ports import (
    CommonSupportResult,
    CommonSupportStatus,
    ComparableCropResult,
    CropComparisonExecutionError,
    CropComparisonRequest,
    CropComparisonResult,
    ICropComparisonEngine,
    InvalidComparisonOutputError,
    ScientificArtifactRole,
)
from ..domain.comparison import normalize_common_support_measurements
from ..domain.errors import DomainValidationError
from .scientific_artifact_store import (
    ScientificArtifactStorageError,
    ScientificArtifactStore,
)

ComparisonRunner = Callable[..., Mapping[str, Any]]

_SAFE_CROP_ID = re.compile(r"^[A-Za-z0-9_-]+$")

_COMPARISON_BRIDGE = """
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

engine_root = Path(sys.argv[1]).resolve()
invocation_path = Path(sys.argv[2]).resolve()
result_path = Path(sys.argv[3]).resolve()

sys.path.insert(0, str(engine_root))

import numpy as np
import rasterio
from shapely.ops import transform as geometry_transform

from src.multicrop import (
    AREA_PROJECT,
    cell_areas,
    compare_crops,
    load_geometry,
)

payload = json.loads(invocation_path.read_text(encoding="utf-8"))

parcel = load_geometry(Path(payload["parcel_path"]))
parcel_area = float(geometry_transform(AREA_PROJECT, parcel).area)

if not math.isfinite(parcel_area) or parcel_area <= 0:
    raise RuntimeError("Parcel must have positive finite area.")

arrays = {}
areas = None
template = None

for entry in payload["crops"]:
    crop_id = entry["crop_id"]
    artifact_path = Path(entry["path"]).resolve()
    expected = entry["grid"]

    if not artifact_path.is_file():
        raise RuntimeError("Scientific comparison artifact is missing.")

    with rasterio.open(artifact_path) as dataset:
        if dataset.crs is None:
            raise RuntimeError(
                "Scientific comparison artifact does not declare a CRS."
            )

        if dataset.crs.to_string() != expected["crs"]:
            raise RuntimeError(
                "Scientific comparison artifact CRS does not match persisted metadata."
            )

        if dataset.width != expected["width"] or dataset.height != expected["height"]:
            raise RuntimeError(
                "Scientific comparison artifact dimensions do not match "
                "persisted metadata."
            )

        actual_transform = [
            dataset.transform.a,
            dataset.transform.b,
            dataset.transform.c,
            dataset.transform.d,
            dataset.transform.e,
            dataset.transform.f,
        ]

        if actual_transform != expected["transform"]:
            raise RuntimeError(
                "Scientific comparison artifact transform does not match "
                "persisted metadata."
            )

        actual_nodata = dataset.nodata
        expected_nodata = expected["nodata"]

        if actual_nodata is not None:
            actual_nodata = float(actual_nodata)
            if not math.isfinite(actual_nodata):
                raise RuntimeError(
                    "Scientific comparison artifact declares non-finite nodata."
                )

        if actual_nodata != expected_nodata:
            raise RuntimeError(
                "Scientific comparison artifact nodata does not match "
                "persisted metadata."
            )

        signature = (
            dataset.shape,
            dataset.transform,
            dataset.crs,
        )

        if template is None:
            template = signature
            areas, measured_parcel_area = cell_areas(
                parcel,
                dataset.shape,
                dataset.transform,
                dataset.crs,
            )
            parcel_area = float(measured_parcel_area)
        elif signature != template:
            raise RuntimeError(
                "Scientific comparison artifacts do not share an identical grid."
            )

        arrays[crop_id] = dataset.read(1, masked=True)

comparison = compare_crops(
    arrays,
    areas,
    parcel_area,
)

comparison.setdefault("common_valid_area_m2", 0.0)
comparison.setdefault("common_coverage_fraction", 0.0)

excluded = list(comparison.get("excluded_without_coverage", []))
excluded_set = set(excluded)

comparison["eligible_crops"] = [
    crop_id
    for crop_id in arrays
    if crop_id not in excluded_set
]
comparison["parcel_area_m2"] = parcel_area

result_path.write_text(
    json.dumps(
        comparison,
        ensure_ascii=False,
        allow_nan=False,
    ),
    encoding="utf-8",
)
""".strip()


class CropSuiteComparisonAdapter(ICropComparisonEngine):
    """Compare persisted CropSuiteLite rasters on common valid support."""

    def __init__(
        self,
        *,
        engine_root: Path,
        workspace_root: Path,
        artifact_store: ScientificArtifactStore,
        python_executable: Path | None = None,
        runner: ComparisonRunner | None = None,
    ) -> None:
        self._engine_root = engine_root.resolve()
        self._workspace_root = workspace_root.resolve()
        self._artifact_store = artifact_store
        self._runner = runner
        self._python_executable = (
            python_executable.resolve()
            if python_executable is not None
            else None
        )

        if _is_within(self._workspace_root, self._engine_root):
            raise ValueError(
                "Crop comparison workspace must be outside "
                "the scientific source tree."
            )

        if self._runner is None:
            if self._python_executable is None:
                raise ValueError(
                    "python_executable is required for real scientific comparison."
                )

            if not self._python_executable.is_file():
                raise ValueError(
                    "Scientific Python executable was not found."
                )

    def compare(
        self,
        request: CropComparisonRequest,
    ) -> CropComparisonResult:
        crop_ids = tuple(entry.crop_id for entry in request.crops)

        if len(crop_ids) != len(set(crop_ids)):
            raise CropComparisonExecutionError(
                "Crop comparison request contains duplicate crop identifiers."
            )

        self._workspace_root.mkdir(parents=True, exist_ok=True)

        request_workspace = Path(
            tempfile.mkdtemp(
                prefix=f"{request.evaluation_id}_comparison_",
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

        comparison_crops: list[dict[str, Any]] = []

        try:
            for entry in request.crops:
                if not _SAFE_CROP_ID.fullmatch(entry.crop_id):
                    raise CropComparisonExecutionError(
                        "Crop identifier is not safe for scientific comparison."
                    )

                artifact = entry.artifact

                if artifact.role is not ScientificArtifactRole.CROP_SUITABILITY:
                    raise CropComparisonExecutionError(
                        "Crop comparison requires crop-suitability artifacts."
                    )

                resolved = self._artifact_store.resolve(
                    artifact.storage_reference,
                    expected_sha256=artifact.sha256,
                    expected_size_bytes=artifact.size_bytes,
                )

                comparison_crops.append(
                    {
                        "crop_id": entry.crop_id,
                        "path": resolved.path,
                        "grid": {
                            "crs": artifact.grid.crs,
                            "width": artifact.grid.width,
                            "height": artifact.grid.height,
                            "transform": list(artifact.grid.transform),
                            "nodata": artifact.grid.nodata,
                        },
                    }
                )
        except ScientificArtifactStorageError as error:
            raise CropComparisonExecutionError(
                "Scientific comparison artifact resolution failed: "
                f"{error}"
            ) from error

        arguments: dict[str, Any] = {
            "parcel_path": parcel_path,
            "crops": tuple(comparison_crops),
        }

        try:
            if self._runner is not None:
                report = self._runner(**arguments)
            else:
                report = self._run_scientific_process(
                    arguments,
                    request_workspace=request_workspace,
                )
        except CropComparisonExecutionError:
            raise
        except Exception as error:
            raise CropComparisonExecutionError(
                "CropSuiteLite comparison could not be executed: "
                f"{type(error).__name__}: {error}"
            ) from error

        return _map_comparison_report(
            report,
            requested_crop_ids=crop_ids,
        )

    def _run_scientific_process(
        self,
        arguments: Mapping[str, Any],
        *,
        request_workspace: Path,
    ) -> Mapping[str, Any]:
        if self._python_executable is None:
            raise CropComparisonExecutionError(
                "Scientific Python executable is not configured."
            )

        invocation_path = request_workspace / "comparison-invocation.json"
        result_path = request_workspace / "comparison-report.json"
        log_path = request_workspace / "comparison.log"
        bridge_path = request_workspace / "run_comparison_bridge.py"

        crops = []

        for entry in cast(tuple[dict[str, Any], ...], arguments["crops"]):
            crops.append(
                {
                    "crop_id": entry["crop_id"],
                    "path": str(entry["path"]),
                    "grid": entry["grid"],
                }
            )

        invocation_path.write_text(
            json.dumps(
                {
                    "parcel_path": str(arguments["parcel_path"]),
                    "crops": crops,
                },
                ensure_ascii=False,
                allow_nan=False,
            ),
            encoding="utf-8",
        )

        bridge_path.write_text(
            _COMPARISON_BRIDGE,
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
            raise CropComparisonExecutionError(
                "Scientific comparison process exited with code "
                f"{completed.returncode}."
            )

        if not result_path.is_file():
            raise CropComparisonExecutionError(
                "Scientific comparison process did not produce a report."
            )

        try:
            report = json.loads(
                result_path.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError as error:
            raise CropComparisonExecutionError(
                "Scientific comparison process produced invalid JSON."
            ) from error

        if not isinstance(report, Mapping):
            raise CropComparisonExecutionError(
                "Scientific comparison report must be an object."
            )

        return cast(Mapping[str, Any], report)


def _map_comparison_report(
    report: Mapping[str, Any],
    *,
    requested_crop_ids: tuple[str, ...],
) -> CropComparisonResult:
    raw_status = report.get("status")

    try:
        status = CommonSupportStatus(raw_status)
    except ValueError as error:
        raise InvalidComparisonOutputError(
            f"Unknown crop comparison status: {raw_status!r}."
        ) from error

    parcel_area = _positive_number(report, "parcel_area_m2")
    common_area = _nonnegative_number(
        report,
        "common_valid_area_m2",
    )
    coverage = _number(
        report,
        "common_coverage_fraction",
    )

    try:
        common_area, coverage = normalize_common_support_measurements(
            parcel_area_m2=parcel_area,
            common_valid_area_m2=common_area,
            common_coverage_fraction=coverage,
        )
    except DomainValidationError as error:
        raise InvalidComparisonOutputError(str(error)) from error

    excluded = _string_sequence(
        report,
        "excluded_without_coverage",
    )

    if len(excluded) != len(set(excluded)):
        raise InvalidComparisonOutputError(
            "Excluded crop identifiers contain duplicates."
        )

    requested = set(requested_crop_ids)

    if any(crop_id not in requested for crop_id in excluded):
        raise InvalidComparisonOutputError(
            "Comparison excluded an unknown crop identifier."
        )

    excluded_set = set(excluded)
    eligible = tuple(
        crop_id
        for crop_id in requested_crop_ids
        if crop_id not in excluded_set
    )

    method = _optional_string(report, "method")
    area_crs = _optional_string(report, "area_crs")

    if status is CommonSupportStatus.NO_SUCCESSFUL_CROPS:
        if requested_crop_ids:
            raise InvalidComparisonOutputError(
                "No-successful-crops is only valid without comparison artifacts."
            )

        if common_area != 0.0 or coverage != 0.0 or excluded:
            raise InvalidComparisonOutputError(
                "No-successful-crops comparison contains support data."
            )

        method = None
        area_crs = None

    else:
        if method != "area_weighted_mean_on_common_valid_cells":
            raise InvalidComparisonOutputError(
                "Unexpected crop comparison method."
            )

        if area_crs != "EPSG:6933":
            raise InvalidComparisonOutputError(
                "Unexpected crop comparison area CRS."
            )

    if status is CommonSupportStatus.COMPARABLE:
        if common_area <= 0:
            raise InvalidComparisonOutputError(
                "Comparable crops must have positive common valid area."
            )

        if not eligible:
            raise InvalidComparisonOutputError(
                "Comparable result must contain eligible crops."
            )

    if status is CommonSupportStatus.NO_COMMON_COVERAGE:
        if common_area != 0.0 or coverage != 0.0:
            raise InvalidComparisonOutputError(
                "No-common-coverage result must have zero common support."
            )

    comparable_crops = _map_comparable_crops(
        report,
        status=status,
        eligible_crops=eligible,
    )

    common_support = CommonSupportResult(
        status=status,
        method=method,
        area_crs=area_crs,
        parcel_area_m2=parcel_area,
        common_valid_area_m2=common_area,
        common_coverage_fraction=coverage,
        eligible_crops=eligible,
        excluded_without_coverage=excluded,
    )

    return CropComparisonResult(
        common_support=common_support,
        comparable_crops=comparable_crops,
    )

def _map_comparable_crops(
    report: Mapping[str, Any],
    *,
    status: CommonSupportStatus,
    eligible_crops: tuple[str, ...],
) -> tuple[ComparableCropResult, ...]:
    raw_ranking = report.get("ranking")

    if not isinstance(raw_ranking, list):
        raise InvalidComparisonOutputError(
            "Crop comparison ranking must be an array."
        )

    if status is not CommonSupportStatus.COMPARABLE:
        if raw_ranking:
            raise InvalidComparisonOutputError(
                "A non-comparable result cannot contain ranked crops."
            )
        return ()

    if len(raw_ranking) != len(eligible_crops):
        raise InvalidComparisonOutputError(
            "Comparable ranking must contain every eligible crop exactly once."
        )

    results: list[ComparableCropResult] = []
    seen: set[str] = set()

    for item in raw_ranking:
        if not isinstance(item, Mapping):
            raise InvalidComparisonOutputError(
                "Each crop comparison ranking entry must be an object."
            )

        crop_id = item.get("crop_id")
        if not isinstance(crop_id, str) or not crop_id:
            raise InvalidComparisonOutputError(
                "Comparable crop identifier must be a non-empty string."
            )

        if crop_id not in eligible_crops:
            raise InvalidComparisonOutputError(
                "Crop comparison ranking contains a non-eligible crop."
            )

        if crop_id in seen:
            raise InvalidComparisonOutputError(
                "Crop comparison ranking contains duplicate crop identifiers."
            )

        mean = _number(item, "mean")
        if not 0.0 <= mean <= 100.0:
            raise InvalidComparisonOutputError(
                "Comparable crop mean must be between 0 and 100."
            )

        raw_rank = item.get("rank")
        if (
            isinstance(raw_rank, bool)
            or not isinstance(raw_rank, int)
            or raw_rank < 1
        ):
            raise InvalidComparisonOutputError(
                "Comparable crop rank must be a positive integer."
            )

        seen.add(crop_id)
        results.append(
            ComparableCropResult(
                crop_id=crop_id,
                mean=mean,
                rank=raw_rank,
            )
        )

    if seen != set(eligible_crops):
        raise InvalidComparisonOutputError(
            "Crop comparison ranking does not match eligible crops."
        )

    _validate_comparable_ranking(results)

    return tuple(results)

def _validate_comparable_ranking(
    crops: list[ComparableCropResult],
) -> None:
    previous: ComparableCropResult | None = None
    expected_rank = 0

    for position, crop in enumerate(crops, start=1):
        if previous is None:
            expected_rank = 1
        else:
            if crop.mean > previous.mean:
                raise InvalidComparisonOutputError(
                    "Comparable crop means are not ordered descending."
                )

            if (
                crop.mean == previous.mean
                and crop.crop_id < previous.crop_id
            ):
                raise InvalidComparisonOutputError(
                    "Equal-mean comparable crops are not ordered deterministically."
                )

            if not math.isclose(
                crop.mean,
                previous.mean,
                rel_tol=0.0,
                abs_tol=1e-9,
            ):
                expected_rank = position

        if crop.rank != expected_rank:
            raise InvalidComparisonOutputError(
                "Crop comparison contains an inconsistent scientific rank."
            )

        previous = crop

def _positive_number(
    mapping: Mapping[str, Any],
    key: str,
) -> float:
    value = _number(mapping, key)

    if value <= 0:
        raise InvalidComparisonOutputError(
            f"{key} must be positive."
        )

    return value


def _nonnegative_number(
    mapping: Mapping[str, Any],
    key: str,
) -> float:
    value = _number(mapping, key)

    if value < 0:
        raise InvalidComparisonOutputError(
            f"{key} must be nonnegative."
        )

    return value


def _number(
    mapping: Mapping[str, Any],
    key: str,
) -> float:
    value = mapping.get(key)

    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
    ):
        raise InvalidComparisonOutputError(
            f"{key} must be a finite number."
        )

    return float(value)


def _string_sequence(
    mapping: Mapping[str, Any],
    key: str,
) -> tuple[str, ...]:
    value = mapping.get(key)

    if not isinstance(value, list):
        raise InvalidComparisonOutputError(
            f"{key} must be an array."
        )

    result = []

    for item in value:
        if not isinstance(item, str) or not item:
            raise InvalidComparisonOutputError(
                f"{key} must contain non-empty strings."
            )

        result.append(item)

    return tuple(result)


def _optional_string(
    mapping: Mapping[str, Any],
    key: str,
) -> str | None:
    value = mapping.get(key)

    if value is None:
        return None

    if not isinstance(value, str) or not value:
        raise InvalidComparisonOutputError(
            f"{key} must be a non-empty string when present."
        )

    return value


def _is_within(
    path: Path,
    parent: Path,
) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False

    return True
