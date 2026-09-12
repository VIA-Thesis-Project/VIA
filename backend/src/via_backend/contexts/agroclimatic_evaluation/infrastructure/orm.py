"""Database records for Agroclimatic Evaluation; not domain entities."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from geoalchemy2 import Geometry
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from .database import AGROCLIMATIC_EVALUATION_SCHEMA, Base


class EvaluationRecord(Base):
    __tablename__ = "evaluations"
    __table_args__ = (
        CheckConstraint("parcel_version > 0", name="parcel_version_positive"),
        CheckConstraint(
            "snapshot_geometry_kind IN ('Polygon', 'MultiPolygon')",
            name="snapshot_geometry_kind_supported",
        ),
        CheckConstraint(
            "snapshot_crs = 'EPSG:4326'",
            name="snapshot_crs_supported",
        ),
        CheckConstraint(
            "status IN ('queued', 'preparing', 'running', 'summarizing', "
            "'succeeded', 'failed', 'cancelled')",
            name="evaluation_status_supported",
        ),
        Index("ix_evaluations_parcel_id", "parcel_id"),
        Index("ix_evaluations_snapshot_geometry", "snapshot_geometry", postgresql_using="gist"),
    )

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, nullable=False
    )
    project_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    parcel_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    parcel_version: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_geometry: Mapped[object] = mapped_column(
        Geometry(
            geometry_type="MULTIPOLYGON",
            srid=4326,
            dimension=2,
            spatial_index=False,
        ),
        nullable=False,
    )
    snapshot_geometry_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    snapshot_crs: Mapped[str] = mapped_column(String(32), nullable=False)
    snapshot_captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvaluationCropRecord(Base):
    __tablename__ = "evaluation_crops"
    __table_args__ = (
        CheckConstraint("position >= 0", name="crop_position_nonnegative"),
        CheckConstraint(
            "crop_id <> '' AND crop_id = btrim(crop_id)",
            name="crop_id_nonempty_trimmed",
        ),
        UniqueConstraint(
            "evaluation_id",
            "crop_id",
            name="uq_evaluation_crops_evaluation_crop",
        ),
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(
            f"{AGROCLIMATIC_EVALUATION_SCHEMA}.evaluations.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
        nullable=False,
    )
    position: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    crop_id: Mapped[str] = mapped_column(String(120), nullable=False, unique=False)
