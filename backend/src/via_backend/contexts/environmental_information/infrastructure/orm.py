"""Database records for Environmental Information; not domain entities."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from geoalchemy2 import Geometry
from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from .database import ENVIRONMENTAL_INFORMATION_SCHEMA, Base


class DatasetRecord(Base):
    __tablename__ = "datasets"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    variable: Mapped[str] = mapped_column(String(120), nullable=False)
    unit: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class DatasetVersionRecord(Base):
    __tablename__ = "dataset_versions"
    __table_args__ = (
        UniqueConstraint(
            "dataset_id",
            "version_identifier",
            name="uq_dataset_versions_dataset_version_identifier",
        ),
        CheckConstraint("resolution_x > 0", name="resolution_x_positive"),
        CheckConstraint("resolution_y > 0", name="resolution_y_positive"),
        CheckConstraint(
            "valid_from IS NULL OR valid_to IS NULL OR valid_from <= valid_to",
            name="validity_period_ordered",
        ),
        CheckConstraint(
            "crs = 'EPSG:' || ST_SRID(extent)::text",
            name="crs_matches_extent_srid",
        ),
        Index(
            "ix_dataset_versions_dataset_id",
            "dataset_id",
        ),
        Index(
            "ix_dataset_versions_extent",
            "extent",
            postgresql_using="gist",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, nullable=False
    )
    dataset_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(
            f"{ENVIRONMENTAL_INFORMATION_SCHEMA}.datasets.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    version_identifier: Mapped[str] = mapped_column(String(120), nullable=False)
    crs: Mapped[str] = mapped_column(String(32), nullable=False)
    resolution_x: Mapped[float] = mapped_column(Float, nullable=False)
    resolution_y: Mapped[float] = mapped_column(Float, nullable=False)
    resolution_unit: Mapped[str] = mapped_column(String(32), nullable=False)
    extent: Mapped[object] = mapped_column(
        Geometry(
            geometry_type="POLYGON",
            srid=-1,
            dimension=2,
            spatial_index=False,
        ),
        nullable=False,
    )
    valid_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    valid_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    scenario: Mapped[str | None] = mapped_column(String(120), nullable=True)
    checksum: Mapped[str] = mapped_column(String(256), nullable=False)
    storage_reference: Mapped[str] = mapped_column(String(1024), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
