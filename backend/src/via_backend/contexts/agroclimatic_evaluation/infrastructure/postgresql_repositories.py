"""PostgreSQL/PostGIS repository for Agroclimatic Evaluation."""

from __future__ import annotations

import json
from typing import cast
from uuid import UUID

from geoalchemy2.elements import WKTElement
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from via_backend.infrastructure.database import SessionFactory

from ..domain.errors import EvaluationConflictError
from ..domain.models import Evaluation, EvaluationStatus
from ..domain.snapshot import ParcelSnapshot, SnapshotGeometry
from .orm import EvaluationCropRecord, EvaluationRecord


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
                    snapshot_geometry=WKTElement(
                        _multipolygon_wkt(snapshot.geometry), srid=4326
                    ),
                    snapshot_geometry_kind=snapshot.geometry.type,
                    snapshot_crs=snapshot.crs,
                    snapshot_captured_at=snapshot.captured_at,
                    status=evaluation.status.value,
                    created_at=evaluation.created_at,
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
            record, geometry_json = row
            return _evaluation_from_row(record, geometry_json, crops)

    def list_all(self) -> tuple[Evaluation, ...]:
        with self._sessions() as session:
            rows = session.execute(
                _evaluation_query().order_by(
                    EvaluationRecord.created_at, EvaluationRecord.id
                )
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
                    _evaluation_from_row(record, geometry_json, crops)
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
            positions = ", ".join(
                f"{x:.17g} {y:.17g}"
                for x, y in ring
            )
            ring_texts.append(f"({positions})")

        polygon_texts.append(f"({', '.join(ring_texts)})")

    return f"MULTIPOLYGON ({', '.join(polygon_texts)})"