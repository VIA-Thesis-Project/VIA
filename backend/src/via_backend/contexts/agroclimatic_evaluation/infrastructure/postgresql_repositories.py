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

from ..domain.errors import EvaluationConflictError
from ..domain.models import Evaluation, EvaluationStatus
from ..domain.outcomes import (
    CropOutcome,
    CropOutcomeStatus,
    ScientificArtifact,
    ScientificArtifactGrid,
    ScientificArtifactRole,
    ScientificTrace,
    SuitabilitySummary,
)
from ..domain.snapshot import ParcelSnapshot, SnapshotGeometry
from .orm import (
    CropOutcomeRecord,
    EvaluationCropRecord,
    EvaluationRecord,
    ScientificArtifactRecord,
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
        except IntegrityError as error:
            raise EvaluationConflictError(
                f"Evaluation {evaluation.id} conflicts with persisted evaluation data."
            ) from error

    def save(self, evaluation: Evaluation, *, expected_status: EvaluationStatus) -> None:
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
                    _artifact_record(
                        evaluation_id,
                        outcome.crop_id,
                        artifact,
                    )
                    for artifact in outcome.artifacts
                )
        except IntegrityError as error:
            raise EvaluationConflictError(
                f"Evaluation {evaluation_id} already has an outcome for {outcome.crop_id}."
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
            outcomes = _load_outcomes(session, evaluation_id)
            record, geometry_json = row
            return _evaluation_from_row(record, geometry_json, crops, outcomes)

    def list_queued_ids(self, *, limit: int) -> tuple[UUID, ...]:
        if isinstance(limit, bool) or limit < 1:
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
                evaluations.append(
                    _evaluation_from_row(
                        record,
                        geometry_json,
                        crops,
                        _load_outcomes(session, record.id),
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
    outcomes: tuple[CropOutcome, ...],
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
        outcomes=outcomes,
        failure_reason=record.failure_reason,
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
            .where(CropOutcomeRecord.evaluation_id == evaluation_id)
            .order_by(EvaluationCropRecord.position)
        )
    )

    artifact_records = session.scalars(
        select(ScientificArtifactRecord)
        .where(ScientificArtifactRecord.evaluation_id == evaluation_id)
        .order_by(
            ScientificArtifactRecord.crop_id,
            ScientificArtifactRecord.role,
        )
    )

    artifacts_by_crop: dict[str, list[ScientificArtifact]] = {}

    for record in artifact_records:
        artifacts_by_crop.setdefault(record.crop_id, []).append(
            _artifact_from_record(record)
        )

    return tuple(
        _outcome_from_record(
            record,
            tuple(artifacts_by_crop.get(record.crop_id, ())),
        )
        for record in outcome_records
    )


def _outcome_record(evaluation_id: UUID, outcome: CropOutcome) -> CropOutcomeRecord:
    summary = outcome.suitability
    trace = outcome.trace
    return CropOutcomeRecord(
        evaluation_id=evaluation_id,
        crop_id=outcome.crop_id,
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
    artifact: ScientificArtifact,
) -> ScientificArtifactRecord:
    return ScientificArtifactRecord(
        evaluation_id=evaluation_id,
        crop_id=crop_id,
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
