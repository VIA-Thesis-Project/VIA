"""PostgreSQL/PostGIS repositories for Environmental Information."""

from __future__ import annotations

import json
from uuid import UUID

from geoalchemy2.elements import WKTElement
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from via_backend.infrastructure.database import SessionFactory

from ..domain.errors import DatasetVersionConflictError
from ..domain.models import Dataset, DatasetVersion
from ..domain.spatial import SpatialExtent, SpatialResolution, validate_crs
from .orm import DatasetRecord, DatasetVersionRecord


class PostgreSQLDatasetRepository:
    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def add(self, dataset: Dataset) -> None:
        try:
            with self._sessions.begin() as session:
                session.add(
                    DatasetRecord(
                        id=dataset.id,
                        name=dataset.name,
                        source=dataset.source,
                        variable=dataset.variable,
                        unit=dataset.unit,
                        created_at=dataset.created_at,
                    )
                )
        except IntegrityError as error:
            raise ValueError(f"Dataset {dataset.id} already exists.") from error

    def get(self, dataset_id: UUID) -> Dataset | None:
        with self._sessions() as session:
            record = session.get(DatasetRecord, dataset_id)
            return _dataset_from_record(record) if record is not None else None

    def list_all(self) -> tuple[Dataset, ...]:
        with self._sessions() as session:
            records = session.scalars(
                select(DatasetRecord).order_by(DatasetRecord.created_at, DatasetRecord.id)
            )
            return tuple(_dataset_from_record(record) for record in records)


class PostgreSQLDatasetVersionRepository:
    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def add(self, version: DatasetVersion) -> None:
        try:
            with self._sessions.begin() as session:
                session.add(_version_record(version))
        except IntegrityError as error:
            raise DatasetVersionConflictError(
                f"Version {version.version_identifier!r} already exists for "
                f"dataset {version.dataset_id}."
            ) from error

    def get(self, version_id: UUID) -> DatasetVersion | None:
        with self._sessions() as session:
            row = session.execute(
                _version_query().where(DatasetVersionRecord.id == version_id)
            ).one_or_none()
            return _version_from_row(*row) if row is not None else None

    def list_for_dataset(self, dataset_id: UUID) -> tuple[DatasetVersion, ...]:
        with self._sessions() as session:
            rows = session.execute(
                _version_query()
                .where(DatasetVersionRecord.dataset_id == dataset_id)
                .order_by(
                    DatasetVersionRecord.registered_at,
                    DatasetVersionRecord.id,
                )
            )
            return tuple(_version_from_row(*row) for row in rows)


def _dataset_from_record(record: DatasetRecord) -> Dataset:
    return Dataset(
        id=record.id,
        name=record.name,
        source=record.source,
        variable=record.variable,
        unit=record.unit,
        created_at=record.created_at,
    )


def _version_query():
    return select(
        DatasetVersionRecord,
        func.ST_AsGeoJSON(DatasetVersionRecord.extent, 17, 0),
    )


def _version_from_row(
    record: DatasetVersionRecord, extent_json: str
) -> DatasetVersion:
    geometry = json.loads(extent_json)
    positions = geometry["coordinates"][0]
    longitudes = [float(position[0]) for position in positions]
    latitudes = [float(position[1]) for position in positions]
    return DatasetVersion(
        id=record.id,
        dataset_id=record.dataset_id,
        version_identifier=record.version_identifier,
        crs=record.crs,
        resolution=SpatialResolution(
            x=record.resolution_x,
            y=record.resolution_y,
            unit=record.resolution_unit,
        ),
        extent=SpatialExtent(
            west=min(longitudes),
            south=min(latitudes),
            east=max(longitudes),
            north=max(latitudes),
        ),
        valid_from=record.valid_from,
        valid_to=record.valid_to,
        scenario=record.scenario,
        checksum=record.checksum,
        storage_reference=record.storage_reference,
        registered_at=record.registered_at,
    )


def _version_record(version: DatasetVersion) -> DatasetVersionRecord:
    extent = version.extent
    positions = (
        (extent.west, extent.south),
        (extent.east, extent.south),
        (extent.east, extent.north),
        (extent.west, extent.north),
        (extent.west, extent.south),
    )
    wkt_positions = ", ".join(
        f"{x:.17g} {y:.17g}" for x, y in positions
    )
    return DatasetVersionRecord(
        id=version.id,
        dataset_id=version.dataset_id,
        version_identifier=version.version_identifier,
        crs=version.crs,
        resolution_x=version.resolution.x,
        resolution_y=version.resolution.y,
        resolution_unit=version.resolution.unit,
        extent=WKTElement(
            f"POLYGON (({wkt_positions}))",
            srid=validate_crs(version.crs),
        ),
        valid_from=version.valid_from,
        valid_to=version.valid_to,
        scenario=version.scenario,
        checksum=version.checksum,
        storage_reference=version.storage_reference,
        registered_at=version.registered_at,
    )
