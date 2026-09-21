"""PostgreSQL/PostGIS repository adapters for Farm Management."""

from __future__ import annotations

import json
from typing import Any, cast
from uuid import UUID

from geoalchemy2.elements import WKTElement
from sqlalchemy import func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..domain.errors import ParcelVersionConflictError
from ..domain.geometry import ParcelGeometry
from ..domain.models import Parcel, ParcelVersion, Project
from .database import SessionFactory
from .orm import ParcelRecord, ParcelVersionRecord, ProjectRecord


class PostgreSQLProjectRepository:
    """Durable adapter for the Project aggregate."""

    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def add(self, project: Project) -> None:
        try:
            with self._sessions.begin() as session:
                session.add(
                    ProjectRecord(
                        id=project.id,
                        owner_user_id=project.owner_user_id,
                        name=project.name,
                        created_at=project.created_at,
                    )
                )
        except IntegrityError as error:
            raise ValueError(f"Project {project.id} already exists.") from error

    def get(self, project_id: UUID) -> Project | None:
        with self._sessions() as session:
            record = session.get(ProjectRecord, project_id)
            return _project_from_record(record) if record is not None else None

    def list_all(self) -> tuple[Project, ...]:
        with self._sessions() as session:
            records = session.scalars(
                select(ProjectRecord).order_by(ProjectRecord.created_at, ProjectRecord.id)
            )
            return tuple(_project_from_record(record) for record in records)


class PostgreSQLParcelRepository:
    """Durable adapter that appends immutable PostGIS geometry versions."""

    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def add(self, parcel: Parcel) -> None:
        try:
            with self._sessions.begin() as session:
                session.add(
                    ParcelRecord(
                        id=parcel.id,
                        project_id=parcel.project_id,
                        name=parcel.name,
                        current_version=parcel.current_version.number,
                        created_at=parcel.created_at,
                    )
                )
                for version in parcel.versions:
                    session.add(_version_record(parcel.id, version))
        except IntegrityError as error:
            raise ValueError(f"Parcel {parcel.id} already exists or is invalid.") from error

    def save(self, parcel: Parcel, *, expected_version: int) -> None:
        if not _is_single_append(parcel, expected_version):
            raise _conflict(parcel.id)

        try:
            with self._sessions.begin() as session:
                updated_id = session.execute(
                    update(ParcelRecord)
                    .where(
                        ParcelRecord.id == parcel.id,
                        ParcelRecord.project_id == parcel.project_id,
                        ParcelRecord.name == parcel.name,
                        ParcelRecord.created_at == parcel.created_at,
                        ParcelRecord.current_version == expected_version,
                    )
                    .values(current_version=expected_version + 1)
                    .returning(ParcelRecord.id)
                ).scalar_one_or_none()

                if updated_id is None:
                    if session.get(ParcelRecord, parcel.id) is None:
                        raise ValueError(f"Parcel {parcel.id} does not exist.")
                    raise _conflict(parcel.id)

                persisted = _load_versions(session, parcel.id)
                if persisted != parcel.versions[:-1]:
                    raise _conflict(parcel.id)

                session.add(_version_record(parcel.id, parcel.current_version))
        except IntegrityError as error:
            raise _conflict(parcel.id) from error

    def get(self, parcel_id: UUID) -> Parcel | None:
        with self._sessions() as session:
            record = session.get(ParcelRecord, parcel_id)
            return _parcel_from_record(session, record) if record is not None else None

    def list_for_project(self, project_id: UUID) -> tuple[Parcel, ...]:
        with self._sessions() as session:
            records = session.scalars(
                select(ParcelRecord)
                .where(ParcelRecord.project_id == project_id)
                .order_by(ParcelRecord.created_at, ParcelRecord.id)
            )
            return tuple(_parcel_from_record(session, record) for record in records)


def _project_from_record(record: ProjectRecord) -> Project:
    return Project(
        id=record.id,
        name=record.name,
        created_at=record.created_at,
        owner_user_id=record.owner_user_id,
    )


def _parcel_from_record(session: Session, record: ParcelRecord) -> Parcel:
    versions = _load_versions(session, record.id)
    if len(versions) != record.current_version:
        raise RuntimeError(
            f"Parcel {record.id} persistence history does not match current_version."
        )
    return Parcel(
        id=record.id,
        project_id=record.project_id,
        name=record.name,
        versions=versions,
        created_at=record.created_at,
    )


def _load_versions(session: Session, parcel_id: UUID) -> tuple[ParcelVersion, ...]:
    rows = session.execute(
        select(
            ParcelVersionRecord.number,
            ParcelVersionRecord.geometry_type,
            func.ST_AsGeoJSON(ParcelVersionRecord.geometry, 17, 0),
            ParcelVersionRecord.created_at,
        )
        .where(ParcelVersionRecord.parcel_id == parcel_id)
        .order_by(ParcelVersionRecord.number)
    )
    versions: list[ParcelVersion] = []
    for number, geometry_type, geometry_json, created_at in rows:
        stored = json.loads(geometry_json)
        if geometry_type == "Polygon":
            geometry: dict[str, Any] = {
                "type": "Polygon",
                "coordinates": stored["coordinates"][0],
            }
        else:
            geometry = stored
        versions.append(
            ParcelVersion(
                number=number,
                geometry=ParcelGeometry.from_geojson(geometry),
                created_at=created_at,
            )
        )
    return tuple(versions)


def _version_record(parcel_id: UUID, version: ParcelVersion) -> ParcelVersionRecord:
    return ParcelVersionRecord(
        parcel_id=parcel_id,
        number=version.number,
        geometry_type=version.geometry.type,
        geometry=WKTElement(_as_multi_polygon_wkt(version.geometry), srid=4326),
        created_at=version.created_at,
    )


def _as_multi_polygon_wkt(geometry: ParcelGeometry) -> str:
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

    polygon_text = []
    for polygon in polygons:
        rings = []
        for ring in polygon:
            positions = ", ".join(
                f"{longitude:.17g} {latitude:.17g}"
                for longitude, latitude in ring
            )
            rings.append(f"({positions})")
        polygon_text.append(f"({', '.join(rings)})")

    return f"MULTIPOLYGON ({', '.join(polygon_text)})"


def _is_single_append(parcel: Parcel, expected_version: int) -> bool:
    return (
        len(parcel.versions) == expected_version + 1
        and parcel.current_version.number == expected_version + 1
    )


def _conflict(parcel_id: UUID) -> ParcelVersionConflictError:
    return ParcelVersionConflictError(
        f"Parcel {parcel_id} changed before its revision could be saved."
    )
