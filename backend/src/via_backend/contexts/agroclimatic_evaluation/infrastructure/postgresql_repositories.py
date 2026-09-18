"""PostgreSQL/PostGIS repository for Agroclimatic Evaluation."""

from __future__ import annotations

import json
from typing import cast
from uuid import UUID

from geoalchemy2.elements import WKTElement
from sqlalchemy import func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from via_backend.infrastructure.database import SessionFactory

from ..domain.comparison import (
    CommonSupport,
    CommonSupportStatus,
    ComparableCrop,
)
from ..domain.environmental_inputs import (
    EnvironmentalInputManifest,
    EnvironmentalInputReference,
    EnvironmentalInputSnapshot,
)
from ..domain.errors import EvaluationConflictError
from ..domain.models import Evaluation, EvaluationScenarioResult, EvaluationStatus
from ..domain.outcomes import (
    CropOutcome,
    CropOutcomeStatus,
    ScientificArtifact,
    ScientificArtifactGrid,
    ScientificArtifactRole,
    ScientificSourceFingerprint,
    ScientificTrace,
    SuitabilitySummary,
)
from ..domain.snapshot import ParcelSnapshot, SnapshotGeometry
from ..domain.water_regime import WaterRegime
from .orm import (
    CropOutcomeRecord,
    EvaluationCommonSupportRecord,
    EvaluationComparableCropRecord,
    EvaluationCropRecord,
    EvaluationEnvironmentalInputManifestRecord,
    EvaluationEnvironmentalInputRecord,
    EvaluationEnvironmentalInputRequestRecord,
    EvaluationRecord,
    EvaluationWaterRegimeRecord,
    ScientificArtifactRecord,
    ScientificSourceFingerprintRecord,
)


class PostgreSQLEvaluationRepository:
    """Durable adapter for immutable Evaluation aggregates."""

    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def add(self, evaluation: Evaluation) -> None:
        snapshot = evaluation.parcel_snapshot
        try:
            with self._sessions.begin() as session:
                record = EvaluationRecord(
                    id=evaluation.id,
                    project_id=snapshot.project_id,
                    parcel_id=snapshot.parcel_id,
                    parcel_version=snapshot.parcel_version,
                    snapshot_geometry=WKTElement(_multipolygon_wkt(snapshot.geometry), srid=4326),
                    snapshot_geometry_kind=snapshot.geometry.type,
                    snapshot_crs=snapshot.crs,
                    snapshot_captured_at=snapshot.captured_at,
                    status=evaluation.status.value,
                    created_at=evaluation.created_at,
                    failure_reason=evaluation.failure_reason,
                )

                session.add(record)

                # The evaluation row must exist before evaluation_crops because
                # evaluation_crops.evaluation_id references evaluations.id.
                session.flush()

                session.add_all(
                    EvaluationCropRecord(
                        evaluation_id=evaluation.id,
                        position=position,
                        crop_id=crop_id,
                    )
                    for position, crop_id in enumerate(evaluation.requested_crops)
                )
                session.add_all(
                    EvaluationWaterRegimeRecord(
                        evaluation_id=evaluation.id,
                        position=position,
                        water_regime=water_regime.value,
                    )
                    for position, water_regime in enumerate(
                        evaluation.requested_water_regimes
                    )
                )
                session.add_all(
                    EvaluationEnvironmentalInputRequestRecord(
                        evaluation_id=evaluation.id,
                        position=position,
                        input_key=reference.input_key,
                        dataset_id=reference.dataset_id,
                        dataset_version_id=reference.dataset_version_id,
                    )
                    for position, reference in enumerate(
                        evaluation.environmental_input_references
                    )
                )
                _persist_environmental_input_manifest(session, evaluation)
        except IntegrityError as error:
            raise EvaluationConflictError(
                f"Evaluation {evaluation.id} conflicts with persisted evaluation data."
            ) from error

    def save(
        self,
        evaluation: Evaluation,
        *,
        expected_status: EvaluationStatus,
    ) -> None:
        try:
            with self._sessions.begin() as session:
                updated_id = session.scalar(
                    update(EvaluationRecord)
                    .where(
                        EvaluationRecord.id == evaluation.id,
                        EvaluationRecord.status == expected_status.value,
                    )
                    .values(
                        status=evaluation.status.value,
                        failure_reason=evaluation.failure_reason,
                    )
                    .returning(EvaluationRecord.id)
                )

                if updated_id is None:
                    raise EvaluationConflictError(
                        f"Evaluation {evaluation.id} changed before it could be saved."
                    )

                _persist_environmental_input_manifest(session, evaluation)
                _persist_scenarios(session, evaluation)
        except IntegrityError as error:
            raise EvaluationConflictError(
                f"Evaluation {evaluation.id} conflicts with persisted evaluation data."
            ) from error

    def add_outcome(self, evaluation_id: UUID, outcome: CropOutcome) -> None:
        try:
            with self._sessions.begin() as session:
                status = session.scalar(
                    select(EvaluationRecord.status)
                    .where(EvaluationRecord.id == evaluation_id)
                    .with_for_update()
                )
                if status != EvaluationStatus.RUNNING.value:
                    raise EvaluationConflictError(f"Evaluation {evaluation_id} is not running.")
                session.add(_outcome_record(evaluation_id, outcome))

                # Materialize the crop outcome before inserting artifact rows whose
                # composite foreign key references it. Both operations remain inside
                # the same database transaction.
                session.flush()

                session.add_all(
                    _source_fingerprint_record(
                        evaluation_id,
                        outcome.crop_id,
                        outcome.water_regime,
                        position,
                        fingerprint,
                    )
                    for position, fingerprint in enumerate(
                        outcome.trace.source_fingerprints
                    )
                )
                session.add_all(
                    _artifact_record(
                        evaluation_id,
                        outcome.crop_id,
                        outcome.water_regime,
                        artifact,
                    )
                    for artifact in outcome.artifacts
                )
        except IntegrityError as error:
            raise EvaluationConflictError(
                f"Evaluation {evaluation_id} already has an outcome for "
                f"{outcome.crop_id} under {outcome.water_regime.value}."
            ) from error

    def get(self, evaluation_id: UUID) -> Evaluation | None:
        with self._sessions() as session:
            row = session.execute(
                _evaluation_query().where(EvaluationRecord.id == evaluation_id)
            ).one_or_none()
            if row is None:
                return None
            crops = tuple(
                session.scalars(
                    select(EvaluationCropRecord.crop_id)
                    .where(EvaluationCropRecord.evaluation_id == evaluation_id)
                    .order_by(EvaluationCropRecord.position)
                )
            )
            water_regimes = _load_requested_water_regimes(session, evaluation_id)
            outcomes = _load_outcomes(session, evaluation_id)
            environmental_input_references = _load_environmental_input_references(
                session,
                evaluation_id,
            )
            environmental_input_manifest = _load_environmental_input_manifest(
                session,
                evaluation_id,
            )
            record, geometry_json = row
            return _evaluation_from_row(
                record,
                geometry_json,
                crops,
                environmental_input_references,
                environmental_input_manifest,
                water_regimes,
                outcomes,
                _load_scenarios(session, evaluation_id, water_regimes),
            )

    def list_queued_ids(self, *, limit: int) -> tuple[UUID, ...]:
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError("limit must be a positive integer.")
        with self._sessions() as session:
            return tuple(
                session.scalars(
                    select(EvaluationRecord.id)
                    .where(EvaluationRecord.status == EvaluationStatus.QUEUED.value)
                    .order_by(EvaluationRecord.created_at, EvaluationRecord.id)
                    .limit(limit)
                )
            )

    def list_active(self, *, limit: int) -> tuple[Evaluation, ...]:
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError("limit must be a positive integer.")
        active_statuses = (
            EvaluationStatus.PREPARING.value,
            EvaluationStatus.RUNNING.value,
            EvaluationStatus.SUMMARIZING.value,
        )
        with self._sessions() as session:
            rows = session.execute(
                _evaluation_query()
                .where(EvaluationRecord.status.in_(active_statuses))
                .order_by(EvaluationRecord.created_at, EvaluationRecord.id)
                .limit(limit)
            )
            evaluations = []
            for record, geometry_json in rows:
                crops = tuple(
                    session.scalars(
                        select(EvaluationCropRecord.crop_id)
                        .where(EvaluationCropRecord.evaluation_id == record.id)
                        .order_by(EvaluationCropRecord.position)
                    )
                )
                water_regimes = _load_requested_water_regimes(session, record.id)
                evaluations.append(
                    _evaluation_from_row(
                        record,
                        geometry_json,
                        crops,
                        _load_environmental_input_references(session, record.id),
                        _load_environmental_input_manifest(session, record.id),
                        water_regimes,
                        _load_outcomes(session, record.id),
                        _load_scenarios(session, record.id, water_regimes),
                    )
                )
            return tuple(evaluations)

    def list_all(self) -> tuple[Evaluation, ...]:
        with self._sessions() as session:
            rows = session.execute(
                _evaluation_query().order_by(EvaluationRecord.created_at, EvaluationRecord.id)
            )
            evaluations = []
            for record, geometry_json in rows:
                crops = tuple(
                    session.scalars(
                        select(EvaluationCropRecord.crop_id)
                        .where(EvaluationCropRecord.evaluation_id == record.id)
                        .order_by(EvaluationCropRecord.position)
                    )
                )
                water_regimes = _load_requested_water_regimes(session, record.id)
                evaluations.append(
                    _evaluation_from_row(
                        record,
                        geometry_json,
                        crops,
                        _load_environmental_input_references(session, record.id),
                        _load_environmental_input_manifest(session, record.id),
                        water_regimes,
                        _load_outcomes(session, record.id),
                        _load_scenarios(session, record.id, water_regimes),
                    )
                )
            return tuple(evaluations)


def _evaluation_query():
    return select(
        EvaluationRecord,
        func.ST_AsGeoJSON(EvaluationRecord.snapshot_geometry, 17, 0),
    )


def _evaluation_from_row(
    record: EvaluationRecord,
    geometry_json: str,
    crops: tuple[str, ...],
    environmental_input_references: tuple[EnvironmentalInputReference, ...],
    environmental_input_manifest: EnvironmentalInputManifest | None,
    water_regimes: tuple[WaterRegime, ...],
    outcomes: tuple[CropOutcome, ...],
    scenarios: tuple[EvaluationScenarioResult, ...],
) -> Evaluation:
    stored_geometry = json.loads(geometry_json)
    if record.snapshot_geometry_kind == "Polygon":
        geometry = {
            "type": "Polygon",
            "coordinates": stored_geometry["coordinates"][0],
        }
    else:
        geometry = stored_geometry
    return Evaluation(
        id=record.id,
        parcel_snapshot=ParcelSnapshot(
            project_id=record.project_id,
            parcel_id=record.parcel_id,
            parcel_version=record.parcel_version,
            geometry=SnapshotGeometry.from_geojson(geometry),
            crs=record.snapshot_crs,
            captured_at=record.snapshot_captured_at,
        ),
        requested_crops=crops,
        status=EvaluationStatus(record.status),
        created_at=record.created_at,
        environmental_input_references=environmental_input_references,
        environmental_input_manifest=environmental_input_manifest,
        requested_water_regimes=water_regimes,
        outcomes=outcomes,
        scenarios=scenarios,
        failure_reason=record.failure_reason,
    )


def _load_requested_water_regimes(
    session: Session,
    evaluation_id: UUID,
) -> tuple[WaterRegime, ...]:
    records = session.scalars(
        select(EvaluationWaterRegimeRecord)
        .where(EvaluationWaterRegimeRecord.evaluation_id == evaluation_id)
        .order_by(EvaluationWaterRegimeRecord.position)
    )
    return tuple(WaterRegime(record.water_regime) for record in records)


def _load_environmental_input_references(
    session: Session,
    evaluation_id: UUID,
) -> tuple[EnvironmentalInputReference, ...]:
    records = session.scalars(
        select(EvaluationEnvironmentalInputRequestRecord)
        .where(EvaluationEnvironmentalInputRequestRecord.evaluation_id == evaluation_id)
        .order_by(EvaluationEnvironmentalInputRequestRecord.position)
    )
    return tuple(
        EnvironmentalInputReference(
            input_key=record.input_key,
            dataset_id=record.dataset_id,
            dataset_version_id=record.dataset_version_id,
        )
        for record in records
    )


def _load_environmental_input_manifest(
    session: Session,
    evaluation_id: UUID,
) -> EnvironmentalInputManifest | None:
    manifest_record = session.get(
        EvaluationEnvironmentalInputManifestRecord,
        evaluation_id,
    )
    if manifest_record is None:
        return None

    input_records = session.scalars(
        select(EvaluationEnvironmentalInputRecord)
        .where(EvaluationEnvironmentalInputRecord.evaluation_id == evaluation_id)
        .order_by(EvaluationEnvironmentalInputRecord.position)
    )
    return EnvironmentalInputManifest(
        resolved_at=manifest_record.resolved_at,
        inputs=tuple(
            EnvironmentalInputSnapshot(
                input_key=record.input_key,
                dataset_id=record.dataset_id,
                dataset_name=record.dataset_name,
                source=record.source,
                variable=record.variable,
                unit=record.unit,
                dataset_version_id=record.dataset_version_id,
                version_identifier=record.version_identifier,
                checksum=record.checksum,
                storage_reference=record.storage_reference,
                crs=record.crs,
                resolution_x=record.resolution_x,
                resolution_y=record.resolution_y,
                resolution_unit=record.resolution_unit,
                extent_west=record.extent_west,
                extent_south=record.extent_south,
                extent_east=record.extent_east,
                extent_north=record.extent_north,
                valid_from=record.valid_from,
                valid_to=record.valid_to,
                scenario=record.scenario,
                registered_at=record.registered_at,
            )
            for record in input_records
        ),
    )


def _persist_environmental_input_manifest(
    session: Session,
    evaluation: Evaluation,
) -> None:
    manifest = evaluation.environmental_input_manifest
    if manifest is None:
        return

    persisted = _load_environmental_input_manifest(session, evaluation.id)
    if persisted is not None:
        if persisted != manifest:
            raise EvaluationConflictError(
                f"Evaluation {evaluation.id} already has a different environmental input manifest."
            )
        return

    session.add(
        EvaluationEnvironmentalInputManifestRecord(
            evaluation_id=evaluation.id,
            resolved_at=manifest.resolved_at,
        )
    )
    session.flush()
    session.add_all(
        EvaluationEnvironmentalInputRecord(
            evaluation_id=evaluation.id,
            position=position,
            input_key=item.input_key,
            dataset_id=item.dataset_id,
            dataset_name=item.dataset_name,
            source=item.source,
            variable=item.variable,
            unit=item.unit,
            dataset_version_id=item.dataset_version_id,
            version_identifier=item.version_identifier,
            checksum=item.checksum,
            storage_reference=item.storage_reference,
            crs=item.crs,
            resolution_x=item.resolution_x,
            resolution_y=item.resolution_y,
            resolution_unit=item.resolution_unit,
            extent_west=item.extent_west,
            extent_south=item.extent_south,
            extent_east=item.extent_east,
            extent_north=item.extent_north,
            valid_from=item.valid_from,
            valid_to=item.valid_to,
            scenario=item.scenario,
            registered_at=item.registered_at,
        )
        for position, item in enumerate(manifest.inputs)
    )

def _persist_scenarios(session: Session, evaluation: Evaluation) -> None:
    for scenario in evaluation.scenarios:
        existing_common_support = session.get(
            EvaluationCommonSupportRecord,
            (evaluation.id, scenario.water_regime.value),
        )
        if existing_common_support is None:
            session.add(
                _common_support_record(
                    evaluation.id,
                    scenario.water_regime,
                    scenario.common_support,
                )
            )
        elif _common_support_from_record(existing_common_support) != scenario.common_support:
            raise EvaluationConflictError(
                f"Evaluation {evaluation.id} already has different common-support "
                f"data for {scenario.water_regime.value}."
            )

        existing_comparable_crops = tuple(
            session.scalars(
                select(EvaluationComparableCropRecord)
                .where(
                    EvaluationComparableCropRecord.evaluation_id == evaluation.id,
                    EvaluationComparableCropRecord.water_regime
                    == scenario.water_regime.value,
                )
                .order_by(EvaluationComparableCropRecord.position)
            )
        )
        restored = tuple(
            _comparable_crop_from_record(record)
            for record in existing_comparable_crops
        )
        if existing_comparable_crops:
            if restored != scenario.comparable_crops:
                raise EvaluationConflictError(
                    f"Evaluation {evaluation.id} already has different comparable-crop "
                    f"data for {scenario.water_regime.value}."
                )
        elif scenario.comparable_crops:
            session.add_all(
                _comparable_crop_record(
                    evaluation.id,
                    scenario.water_regime,
                    position,
                    crop,
                )
                for position, crop in enumerate(scenario.comparable_crops)
            )


def _load_scenarios(
    session: Session,
    evaluation_id: UUID,
    requested_water_regimes: tuple[WaterRegime, ...],
) -> tuple[EvaluationScenarioResult, ...]:
    scenarios: list[EvaluationScenarioResult] = []
    for water_regime in requested_water_regimes:
        common_support_record = session.get(
            EvaluationCommonSupportRecord,
            (evaluation_id, water_regime.value),
        )
        if common_support_record is None:
            continue
        comparable_records = session.scalars(
            select(EvaluationComparableCropRecord)
            .where(
                EvaluationComparableCropRecord.evaluation_id == evaluation_id,
                EvaluationComparableCropRecord.water_regime == water_regime.value,
            )
            .order_by(EvaluationComparableCropRecord.position)
        )
        scenarios.append(
            EvaluationScenarioResult(
                water_regime=water_regime,
                common_support=_common_support_from_record(common_support_record),
                comparable_crops=tuple(
                    _comparable_crop_from_record(record)
                    for record in comparable_records
                ),
            )
        )
    return tuple(scenarios)


def _common_support_record(
    evaluation_id: UUID,
    water_regime: WaterRegime,
    common_support: CommonSupport,
) -> EvaluationCommonSupportRecord:
    return EvaluationCommonSupportRecord(
        evaluation_id=evaluation_id,
        water_regime=water_regime.value,
        status=common_support.status.value,
        method=common_support.method,
        area_crs=common_support.area_crs,
        parcel_area_m2=common_support.parcel_area_m2,
        common_valid_area_m2=common_support.common_valid_area_m2,
        common_coverage_fraction=common_support.common_coverage_fraction,
        eligible_crops=list(common_support.eligible_crops),
        excluded_without_coverage=list(
            common_support.excluded_without_coverage
        ),
    )


def _common_support_from_record(
    record: EvaluationCommonSupportRecord,
) -> CommonSupport:
    return CommonSupport(
        status=CommonSupportStatus(record.status),
        method=record.method,
        area_crs=record.area_crs,
        parcel_area_m2=record.parcel_area_m2,
        common_valid_area_m2=record.common_valid_area_m2,
        common_coverage_fraction=record.common_coverage_fraction,
        eligible_crops=tuple(record.eligible_crops),
        excluded_without_coverage=tuple(
            record.excluded_without_coverage
        ),
    )


def _comparable_crop_record(
    evaluation_id: UUID,
    water_regime: WaterRegime,
    position: int,
    crop: ComparableCrop,
) -> EvaluationComparableCropRecord:
    return EvaluationComparableCropRecord(
        evaluation_id=evaluation_id,
        crop_id=crop.crop_id,
        water_regime=water_regime.value,
        position=position,
        mean=crop.mean,
        rank=crop.rank,
    )


def _comparable_crop_from_record(
    record: EvaluationComparableCropRecord,
) -> ComparableCrop:
    return ComparableCrop(
        crop_id=record.crop_id,
        mean=record.mean,
        rank=record.rank,
    )


def _load_outcomes(
    session: Session,
    evaluation_id: UUID,
) -> tuple[CropOutcome, ...]:
    outcome_records = tuple(
        session.scalars(
            select(CropOutcomeRecord)
            .join(
                EvaluationCropRecord,
                (
                    EvaluationCropRecord.evaluation_id
                    == CropOutcomeRecord.evaluation_id
                )
                & (
                    EvaluationCropRecord.crop_id
                    == CropOutcomeRecord.crop_id
                ),
            )
            .join(
                EvaluationWaterRegimeRecord,
                (
                    EvaluationWaterRegimeRecord.evaluation_id
                    == CropOutcomeRecord.evaluation_id
                )
                & (
                    EvaluationWaterRegimeRecord.water_regime
                    == CropOutcomeRecord.water_regime
                ),
            )
            .where(CropOutcomeRecord.evaluation_id == evaluation_id)
            .order_by(
                EvaluationCropRecord.position,
                EvaluationWaterRegimeRecord.position,
            )
        )
    )

    artifact_records = session.scalars(
        select(ScientificArtifactRecord)
        .where(ScientificArtifactRecord.evaluation_id == evaluation_id)
        .order_by(
            ScientificArtifactRecord.crop_id,
            ScientificArtifactRecord.water_regime,
            ScientificArtifactRecord.role,
        )
    )

    source_fingerprint_records = session.scalars(
        select(ScientificSourceFingerprintRecord)
        .where(ScientificSourceFingerprintRecord.evaluation_id == evaluation_id)
        .order_by(
            ScientificSourceFingerprintRecord.crop_id,
            ScientificSourceFingerprintRecord.water_regime,
            ScientificSourceFingerprintRecord.position,
        )
    )

    artifacts_by_execution: dict[
        tuple[str, WaterRegime], list[ScientificArtifact]
    ] = {}
    source_fingerprints_by_execution: dict[
        tuple[str, WaterRegime], list[ScientificSourceFingerprint]
    ] = {}

    for record in artifact_records:
        key = (record.crop_id, WaterRegime(record.water_regime))
        artifacts_by_execution.setdefault(key, []).append(
            _artifact_from_record(record)
        )

    for record in source_fingerprint_records:
        key = (record.crop_id, WaterRegime(record.water_regime))
        source_fingerprints_by_execution.setdefault(key, []).append(
            ScientificSourceFingerprint(
                source_reference=record.source_reference,
                sha256=record.sha256,
            )
        )

    return tuple(
        _outcome_from_record(
            record,
            tuple(
                artifacts_by_execution.get(
                    (record.crop_id, WaterRegime(record.water_regime)),
                    (),
                )
            ),
            tuple(
                source_fingerprints_by_execution.get(
                    (record.crop_id, WaterRegime(record.water_regime)),
                    (),
                )
            ),
        )
        for record in outcome_records
    )


def _outcome_record(evaluation_id: UUID, outcome: CropOutcome) -> CropOutcomeRecord:
    summary = outcome.suitability
    trace = outcome.trace
    return CropOutcomeRecord(
        evaluation_id=evaluation_id,
        crop_id=outcome.crop_id,
        water_regime=outcome.water_regime.value,
        status=outcome.status.value,
        suitability_mean=summary.mean if summary is not None else None,
        suitability_minimum=summary.minimum if summary is not None else None,
        suitability_maximum=summary.maximum if summary is not None else None,
        valid_cells=summary.valid_cells if summary is not None else None,
        valid_area_m2=summary.valid_area_m2 if summary is not None else None,
        coverage_fraction=summary.coverage_fraction if summary is not None else None,
        zero_suitability_area_m2=(
            summary.zero_suitability_area_m2 if summary is not None else None
        ),
        failure_message=outcome.failure_message,
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
    )

def _artifact_record(
    evaluation_id: UUID,
    crop_id: str,
    water_regime: WaterRegime,
    artifact: ScientificArtifact,
) -> ScientificArtifactRecord:
    return ScientificArtifactRecord(
        evaluation_id=evaluation_id,
        crop_id=crop_id,
        water_regime=water_regime.value,
        role=artifact.role.value,
        storage_reference=artifact.storage_reference,
        sha256=artifact.sha256,
        media_type=artifact.media_type,
        size_bytes=artifact.size_bytes,
        crs=artifact.grid.crs,
        width=artifact.grid.width,
        height=artifact.grid.height,
        transform=list(artifact.grid.transform),
        nodata=artifact.grid.nodata,
    )


def _source_fingerprint_record(
    evaluation_id: UUID,
    crop_id: str,
    water_regime: WaterRegime,
    position: int,
    fingerprint: ScientificSourceFingerprint,
) -> ScientificSourceFingerprintRecord:
    return ScientificSourceFingerprintRecord(
        evaluation_id=evaluation_id,
        crop_id=crop_id,
        water_regime=water_regime.value,
        position=position,
        source_reference=fingerprint.source_reference,
        sha256=fingerprint.sha256,
    )


def _artifact_from_record(
    record: ScientificArtifactRecord,
) -> ScientificArtifact:
    transform = tuple(float(value) for value in record.transform)

    if len(transform) != 6:
        raise ValueError(
            "Persisted scientific artifact transform must contain six coefficients."
        )

    return ScientificArtifact(
        role=ScientificArtifactRole(record.role),
        storage_reference=record.storage_reference,
        sha256=record.sha256,
        media_type=record.media_type,
        size_bytes=record.size_bytes,
        grid=ScientificArtifactGrid(
            crs=record.crs,
            width=record.width,
            height=record.height,
            transform=cast(
                tuple[float, float, float, float, float, float],
                transform,
            ),
            nodata=record.nodata,
        ),
    )

def _outcome_from_record(
    record: CropOutcomeRecord,
    artifacts: tuple[ScientificArtifact, ...],
    source_fingerprints: tuple[ScientificSourceFingerprint, ...],
) -> CropOutcome:
    status = CropOutcomeStatus(record.status)
    summary = (
        None
        if status is CropOutcomeStatus.FAILED
        else SuitabilitySummary(
            mean=record.suitability_mean,
            minimum=record.suitability_minimum,
            maximum=record.suitability_maximum,
            valid_cells=cast(int, record.valid_cells),
            valid_area_m2=cast(float, record.valid_area_m2),
            coverage_fraction=cast(float, record.coverage_fraction),
            zero_suitability_area_m2=cast(float, record.zero_suitability_area_m2),
        )
    )
    return CropOutcome(
        crop_id=record.crop_id,
        water_regime=WaterRegime(record.water_regime),
        status=status,
        suitability=summary,
        failure_message=record.failure_message,
        trace=ScientificTrace(
            engine_identifier=record.engine_identifier,
            execution_reference=record.execution_reference,
            started_at=record.started_at,
            finished_at=record.finished_at,
            elapsed_seconds=record.elapsed_seconds,
            execution_mode=record.execution_mode,
            parcel_sha256=record.parcel_sha256,
            parameter_sha256=record.parameter_sha256,
            configuration_sha256=record.configuration_sha256,
            source_files_unchanged=record.source_files_unchanged,
            source_fingerprints=source_fingerprints,
        ),
        artifacts=artifacts,
    )


def _multipolygon_wkt(geometry: SnapshotGeometry) -> str:
    if geometry.type == "Polygon":
        polygon = cast(
            tuple[
                tuple[
                    tuple[float, float],
                    ...,
                ],
                ...,
            ],
            geometry.coordinates,
        )
        polygons = (polygon,)
    else:
        polygons = cast(
            tuple[
                tuple[
                    tuple[
                        tuple[float, float],
                        ...,
                    ],
                    ...,
                ],
                ...,
            ],
            geometry.coordinates,
        )

    polygon_texts = []

    for polygon in polygons:
        ring_texts = []

        for ring in polygon:
            positions = ", ".join(f"{x:.17g} {y:.17g}" for x, y in ring)
            ring_texts.append(f"({positions})")

        polygon_texts.append(f"({', '.join(ring_texts)})")

    return f"MULTIPOLYGON ({', '.join(polygon_texts)})"
