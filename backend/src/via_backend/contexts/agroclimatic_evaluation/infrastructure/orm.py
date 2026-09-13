"""Database records for Agroclimatic Evaluation; not domain entities."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from geoalchemy2 import Geometry
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Text,
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
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)


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


class CropOutcomeRecord(Base):
    __tablename__ = "crop_outcomes"
    __table_args__ = (
        CheckConstraint(
            "status IN ('succeeded', 'no_coverage', 'failed')",
            name="crop_outcome_status_supported",
        ),
        CheckConstraint(
            "elapsed_seconds >= 0",
            name="crop_outcome_elapsed_nonnegative",
        ),
        CheckConstraint(
            "coverage_fraction IS NULL OR "
            "(coverage_fraction >= 0 AND coverage_fraction <= 1)",
            name="crop_outcome_coverage_fraction_valid",
        ),
        CheckConstraint(
            "(status = 'failed' AND failure_message IS NOT NULL "
            "AND suitability_mean IS NULL AND suitability_minimum IS NULL "
            "AND suitability_maximum IS NULL AND valid_cells IS NULL "
            "AND valid_area_m2 IS NULL AND coverage_fraction IS NULL "
            "AND zero_suitability_area_m2 IS NULL) OR "
            "(status IN ('succeeded', 'no_coverage') AND failure_message IS NULL "
            "AND valid_cells IS NOT NULL AND valid_area_m2 IS NOT NULL "
            "AND coverage_fraction IS NOT NULL "
            "AND zero_suitability_area_m2 IS NOT NULL)",
            name="crop_outcome_payload_matches_status",
        ),
        ForeignKeyConstraint(
            ["evaluation_id", "crop_id"],
            [
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.evaluation_crops.evaluation_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.evaluation_crops.crop_id",
            ],
            name="fk_crop_outcomes_requested_crop",
            ondelete="CASCADE",
        ),
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, nullable=False
    )
    crop_id: Mapped[str] = mapped_column(String(120), primary_key=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    suitability_mean: Mapped[float | None] = mapped_column(Float, nullable=True)
    suitability_minimum: Mapped[float | None] = mapped_column(Float, nullable=True)
    suitability_maximum: Mapped[float | None] = mapped_column(Float, nullable=True)
    valid_cells: Mapped[int | None] = mapped_column(Integer, nullable=True)
    valid_area_m2: Mapped[float | None] = mapped_column(Float, nullable=True)
    coverage_fraction: Mapped[float | None] = mapped_column(Float, nullable=True)
    zero_suitability_area_m2: Mapped[float | None] = mapped_column(Float, nullable=True)
    failure_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    engine_identifier: Mapped[str] = mapped_column(String(120), nullable=False)
    execution_reference: Mapped[str] = mapped_column(Text, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    elapsed_seconds: Mapped[float] = mapped_column(Float, nullable=False)
    execution_mode: Mapped[str] = mapped_column(String(120), nullable=False)
    parcel_sha256: Mapped[str] = mapped_column(String(128), nullable=False)
    parameter_sha256: Mapped[str | None] = mapped_column(String(128), nullable=True)
    configuration_sha256: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_files_unchanged: Mapped[bool] = mapped_column(Boolean, nullable=False)
