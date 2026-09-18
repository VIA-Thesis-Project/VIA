"""Synchronous application orchestration for persisted evaluations."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from via_backend.contexts.environmental_information.application.public import (
    GetPublishedDatasetVersion,
    PublishedDatasetVersionReader,
)

from ..domain.comparison import (
    CommonSupport,
    ComparableCrop,
)
from ..domain.comparison import (
    CommonSupportStatus as DomainCommonSupportStatus,
)
from ..domain.environmental_inputs import EnvironmentalInputManifest, EnvironmentalInputSnapshot
from ..domain.errors import EvaluationConflictError
from ..domain.models import Evaluation, EvaluationStatus
from ..domain.outcomes import (
    CropLimitationEvidence,
    CropOutcome,
    CropOutcomeStatus,
    LimitationEvidenceAvailability,
    LimitingFactorEvidence,
    ScientificArtifact,
    ScientificArtifactGrid,
    ScientificArtifactRole,
    ScientificTrace,
    SuitabilitySummary,
)
from ..domain.outcomes import (
    ScientificSourceFingerprint as DomainScientificSourceFingerprint,
)
from ..domain.repositories import EvaluationRepository
from ..domain.water_regime import WaterRegime
from .commands import ExecuteEvaluation
from .ports import (
    CommonSupportResult,
    ComparableCropResult,
    CropComparisonExecutionError,
    CropComparisonInput,
    CropComparisonRequest,
    CropSuitabilityRequest,
    CropSuitabilityResult,
    ICropComparisonEngine,
    ICropSuitabilityEngine,
    InvalidEngineOutputError,
    ScientificArtifactDescriptor,
)
from .ports import (
    ScientificArtifactGrid as PortScientificArtifactGrid,
)
from .ports import (
    ScientificArtifactRole as PortScientificArtifactRole,
)
from .results import EvaluationResult
from .service import ResourceConflictError, ResourceNotFoundError


class EnvironmentalInputResolutionError(RuntimeError):
    """Raised when an exact caller-selected environmental version cannot be resolved."""


class AgroclimaticEvaluationExecutionService:
    """Execute requested crops and summarize them through Application-owned ports."""

    def __init__(
        self,
        evaluations: EvaluationRepository,
        engine: ICropSuitabilityEngine,
        comparison_engine: ICropComparisonEngine,
        environmental_information: PublishedDatasetVersionReader,
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._evaluations = evaluations
        self._engine = engine
        self._comparison_engine = comparison_engine
        self._environmental_information = environmental_information
        self._clock = clock or (lambda: datetime.now(UTC))

    def execute_evaluation(
        self,
        command: ExecuteEvaluation,
    ) -> EvaluationResult:
        evaluation = self._evaluations.get(command.evaluation_id)

        if evaluation is None:
            raise ResourceNotFoundError(
                f"Evaluation {command.evaluation_id} was not found."
            )

        if evaluation.status is not EvaluationStatus.QUEUED:
            raise ResourceConflictError(
                f"Evaluation {evaluation.id} cannot execute from "
                f"{evaluation.status.value}."
            )

        preparing = evaluation.prepare()

        try:
            self._evaluations.save(
                preparing,
                expected_status=EvaluationStatus.QUEUED,
            )
        except EvaluationConflictError as error:
            raise ResourceConflictError(str(error)) from error

        current = preparing

        try:
            manifest = self._resolve_environmental_inputs(current)
            running = current.attach_environmental_input_manifest(manifest).start_running()

            self._evaluations.save(
                running,
                expected_status=EvaluationStatus.PREPARING,
            )

            current = running

            for crop_id, water_regime in current.execution_matrix:
                result = self._engine.evaluate(
                    CropSuitabilityRequest(
                        evaluation_id=current.id,
                        parcel_snapshot=current.parcel_snapshot,
                        crop_id=crop_id,
                        environmental_input_manifest=manifest,
                        water_regime=water_regime,
                    )
                )

                if result.crop_id != crop_id or result.water_regime is not water_regime:
                    raise InvalidEngineOutputError(
                        "Engine result did not preserve the requested scenario identity."
                    )

                outcome = _to_outcome(result)

                updated = current.record_outcome(outcome)

                self._evaluations.add_outcome(
                    current.id,
                    outcome,
                )

                current = updated

            summarizing = current.start_summarizing()

            self._evaluations.save(
                summarizing,
                expected_status=EvaluationStatus.RUNNING,
            )

            current = summarizing

            summarized = current
            for water_regime in current.requested_water_regimes:
                comparison_result = self._comparison_engine.compare(
                    _comparison_request(summarized, water_regime)
                )

                summarized = summarized.record_comparison(
                    common_support=_to_common_support(
                        comparison_result.common_support
                    ),
                    comparable_crops=tuple(
                        _to_comparable_crop(crop)
                        for crop in comparison_result.comparable_crops
                    ),
                    water_regime=water_regime,
                )

            succeeded = summarized.succeed()

            self._evaluations.save(
                succeeded,
                expected_status=EvaluationStatus.SUMMARIZING,
            )

            return EvaluationResult.from_domain(succeeded)

        except Exception as error:
            self._persist_failure(current, error)
            raise

    def _resolve_environmental_inputs(
        self,
        evaluation: Evaluation,
    ) -> EnvironmentalInputManifest:
        if not evaluation.environmental_input_references:
            raise EnvironmentalInputResolutionError(
                "Queued evaluation has no environmental input references."
            )

        snapshots: list[EnvironmentalInputSnapshot] = []
        for reference in evaluation.environmental_input_references:
            published = self._environmental_information.get_published_dataset_version(
                GetPublishedDatasetVersion(
                    dataset_id=reference.dataset_id,
                    dataset_version_id=reference.dataset_version_id,
                )
            )
            if published is None:
                raise EnvironmentalInputResolutionError(
                    "Exact environmental dataset version could not be resolved: "
                    f"dataset_id={reference.dataset_id}, "
                    f"dataset_version_id={reference.dataset_version_id}."
                )
            snapshots.append(
                EnvironmentalInputSnapshot(
                    input_key=reference.input_key,
                    dataset_id=published.dataset_id,
                    dataset_name=published.dataset_name,
                    source=published.source,
                    variable=published.variable,
                    unit=published.unit,
                    dataset_version_id=published.dataset_version_id,
                    version_identifier=published.version_identifier,
                    checksum=published.checksum,
                    storage_reference=published.storage_reference,
                    crs=published.crs,
                    resolution_x=published.resolution_x,
                    resolution_y=published.resolution_y,
                    resolution_unit=published.resolution_unit,
                    extent_west=published.extent_west,
                    extent_south=published.extent_south,
                    extent_east=published.extent_east,
                    extent_north=published.extent_north,
                    valid_from=published.valid_from,
                    valid_to=published.valid_to,
                    scenario=published.scenario,
                    registered_at=published.registered_at,
                )
            )
        return EnvironmentalInputManifest(
            resolved_at=self._clock(),
            inputs=tuple(snapshots),
        )

    def _persist_failure(
        self,
        evaluation: Evaluation,
        error: Exception,
    ) -> None:
        failed = evaluation.fail(
            f"{type(error).__name__}: {error}"
        )

        try:
            self._evaluations.save(
                failed,
                expected_status=evaluation.status,
            )
        except EvaluationConflictError as persistence_error:
            error.add_note(
                "The orchestration failure state could not be persisted: "
                f"{type(persistence_error).__name__}: {persistence_error}"
            )


def _to_outcome(
    result: CropSuitabilityResult,
) -> CropOutcome:
    suitability = result.suitability
    trace = result.trace

    return CropOutcome(
        crop_id=result.crop_id,
        water_regime=result.water_regime,
        status=CropOutcomeStatus(result.status.value),
        suitability=(
            SuitabilitySummary(
                mean=suitability.mean,
                minimum=suitability.minimum,
                maximum=suitability.maximum,
                valid_cells=suitability.valid_cells,
                valid_area_m2=suitability.valid_area_m2,
                coverage_fraction=suitability.coverage_fraction,
                zero_suitability_area_m2=suitability.zero_suitability_area_m2,
            )
            if suitability is not None
            else None
        ),
        failure_message=(
            result.failure.message
            if result.failure is not None
            else None
        ),
        trace=ScientificTrace(
            engine_identifier=trace.engine_identifier,
            execution_reference=trace.execution_reference,
            started_at=trace.started_at,
            finished_at=trace.finished_at,
            elapsed_seconds=trace.elapsed_seconds,
            execution_mode=trace.execution_mode,
            parcel_sha256=trace.parcel_sha256,
            parameter_sha256=trace.parameter_sha256,
            configuration_sha256=trace.configuration_sha256,
            source_files_unchanged=trace.source_files_unchanged,
            source_fingerprints=tuple(
                DomainScientificSourceFingerprint(
                    source_reference=fingerprint.source_reference,
                    sha256=fingerprint.sha256,
                )
                for fingerprint in trace.source_fingerprints
            ),
        ),
        artifacts=tuple(
            ScientificArtifact(
                role=ScientificArtifactRole(
                    artifact.role.value
                ),
                storage_reference=artifact.storage_reference,
                sha256=artifact.sha256,
                media_type=artifact.media_type,
                size_bytes=artifact.size_bytes,
                grid=ScientificArtifactGrid(
                    crs=artifact.grid.crs,
                    width=artifact.grid.width,
                    height=artifact.grid.height,
                    transform=artifact.grid.transform,
                    nodata=artifact.grid.nodata,
                ),
            )
            for artifact in result.artifacts
        ),
        limitation_evidence=CropLimitationEvidence(
            availability=LimitationEvidenceAvailability(
                result.limitation_evidence.availability.value
            ),
            reason=result.limitation_evidence.reason,
            warnings=result.limitation_evidence.warnings,
            factors=tuple(
                LimitingFactorEvidence(
                    factor_code=factor.factor_code,
                    label=factor.label,
                    raw_code=factor.raw_code,
                    affected_cells=factor.affected_cells,
                    affected_area_m2=factor.affected_area_m2,
                    affected_fraction=factor.affected_fraction,
                    dominant=factor.dominant,
                    source_storage_reference=factor.source_storage_reference,
                    source_sha256=factor.source_sha256,
                )
                for factor in result.limitation_evidence.factors
            ),
        ),
    )


def _comparison_request(
    evaluation: Evaluation,
    water_regime: WaterRegime = WaterRegime.RAINFED,
) -> CropComparisonRequest:
    crops: list[CropComparisonInput] = []

    for outcome in evaluation.outcomes:
        if outcome.water_regime is not water_regime:
            continue
        if outcome.status is CropOutcomeStatus.FAILED:
            continue

        artifacts = tuple(
            artifact
            for artifact in outcome.artifacts
            if artifact.role
            is ScientificArtifactRole.CROP_SUITABILITY
        )

        if len(artifacts) != 1:
            raise CropComparisonExecutionError(
                "Every non-failed crop outcome must have exactly one "
                "crop-suitability artifact before comparison."
            )

        artifact = artifacts[0]

        crops.append(
            CropComparisonInput(
                crop_id=outcome.crop_id,
                artifact=ScientificArtifactDescriptor(
                    role=PortScientificArtifactRole(
                        artifact.role.value
                    ),
                    storage_reference=artifact.storage_reference,
                    sha256=artifact.sha256,
                    media_type=artifact.media_type,
                    size_bytes=artifact.size_bytes,
                    grid=PortScientificArtifactGrid(
                        crs=artifact.grid.crs,
                        width=artifact.grid.width,
                        height=artifact.grid.height,
                        transform=artifact.grid.transform,
                        nodata=artifact.grid.nodata,
                    ),
                ),
            )
        )

    return CropComparisonRequest(
        evaluation_id=evaluation.id,
        parcel_snapshot=evaluation.parcel_snapshot,
        crops=tuple(crops),
        water_regime=water_regime,
    )


def _to_common_support(
    result: CommonSupportResult,
) -> CommonSupport:
    return CommonSupport(
        status=DomainCommonSupportStatus(
            result.status.value
        ),
        method=result.method,
        area_crs=result.area_crs,
        parcel_area_m2=result.parcel_area_m2,
        common_valid_area_m2=result.common_valid_area_m2,
        common_coverage_fraction=(
            result.common_coverage_fraction
        ),
        eligible_crops=result.eligible_crops,
        excluded_without_coverage=(
            result.excluded_without_coverage
        ),
    )


def _to_comparable_crop(
    result: ComparableCropResult,
) -> ComparableCrop:
    return ComparableCrop(
        crop_id=result.crop_id,
        mean=result.mean,
        rank=result.rank,
    )
