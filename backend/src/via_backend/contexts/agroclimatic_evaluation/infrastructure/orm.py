"""Database records for Agroclimatic Evaluation; not domain entities."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from geoalchemy2 import Geometry
from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
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
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
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
        Index("ix_evaluations_owner_user_id", "owner_user_id"),
        Index("ix_evaluations_parcel_id", "parcel_id"),
        Index("ix_evaluations_status_created_at_id", "status", "created_at", "id"),
        Index("ix_evaluations_snapshot_geometry", "snapshot_geometry", postgresql_using="gist"),
    )

    id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True, nullable=False)
    owner_user_id: Mapped[UUID | None] = mapped_column(
        PostgreSQLUUID(as_uuid=True), nullable=True
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
    snapshot_captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)


class EvaluationWaterRegimeRecord(Base):
    __tablename__ = "evaluation_water_regimes"
    __table_args__ = (
        CheckConstraint("position >= 0", name="water_regime_position_nonnegative"),
        CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="water_regime_supported",
        ),
        UniqueConstraint(
            "evaluation_id",
            "water_regime",
            name="uq_evaluation_water_regimes_regime",
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
    water_regime: Mapped[str] = mapped_column(String(16), nullable=False)


class EvaluationEnvironmentalInputRequestRecord(Base):
    __tablename__ = "evaluation_environmental_input_requests"
    __table_args__ = (
        CheckConstraint(
            "position >= 0",
            name="env_input_request_position_nonnegative",
        ),
        CheckConstraint(
            "input_key <> '' AND input_key = btrim(input_key)",
            name="env_input_request_key_nonempty_trimmed",
        ),
        UniqueConstraint(
            "evaluation_id",
            "input_key",
            name="uq_env_input_request_key",
        ),
        UniqueConstraint(
            "evaluation_id",
            "input_key",
            "dataset_id",
            "dataset_version_id",
            name="uq_env_input_request_exact_reference",
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
    input_key: Mapped[str] = mapped_column(String(120), nullable=False)
    dataset_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    dataset_version_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        nullable=False,
    )


class EvaluationEnvironmentalInputManifestRecord(Base):
    __tablename__ = "evaluation_environmental_input_manifests"

    evaluation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(
            f"{AGROCLIMATIC_EVALUATION_SCHEMA}.evaluations.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
        nullable=False,
    )
    resolved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvaluationEnvironmentalInputRecord(Base):
    __tablename__ = "evaluation_environmental_inputs"
    __table_args__ = (
        CheckConstraint("position >= 0", name="env_input_position_nonnegative"),
        CheckConstraint(
            "input_key <> '' AND input_key = btrim(input_key)",
            name="env_input_key_nonempty_trimmed",
        ),
        CheckConstraint(
            "dataset_name <> '' AND dataset_name = btrim(dataset_name)",
            name="env_input_dataset_name_nonempty_trimmed",
        ),
        CheckConstraint(
            "source <> '' AND source = btrim(source)",
            name="env_input_source_nonempty_trimmed",
        ),
        CheckConstraint(
            "variable <> '' AND variable = btrim(variable)",
            name="env_input_variable_nonempty_trimmed",
        ),
        CheckConstraint(
            "unit <> '' AND unit = btrim(unit)",
            name="env_input_unit_nonempty_trimmed",
        ),
        CheckConstraint(
            "version_identifier <> '' AND version_identifier = btrim(version_identifier)",
            name="env_input_version_identifier_nonempty_trimmed",
        ),
        CheckConstraint(
            "checksum <> '' AND checksum = btrim(checksum)",
            name="env_input_checksum_nonempty_trimmed",
        ),
        CheckConstraint(
            "storage_reference <> '' AND storage_reference = btrim(storage_reference)",
            name="env_input_storage_reference_nonempty_trimmed",
        ),
        CheckConstraint(
            "resolution_unit <> '' AND resolution_unit = btrim(resolution_unit)",
            name="env_input_resolution_unit_nonempty_trimmed",
        ),
        CheckConstraint("resolution_x > 0", name="env_input_resolution_x_positive"),
        CheckConstraint("resolution_y > 0", name="env_input_resolution_y_positive"),
        CheckConstraint("extent_west < extent_east", name="env_input_west_before_east"),
        CheckConstraint(
            "extent_south < extent_north",
            name="env_input_south_before_north",
        ),
        CheckConstraint(
            "valid_from IS NULL OR valid_to IS NULL OR valid_from <= valid_to",
            name="env_input_validity_window_ordered",
        ),
        CheckConstraint(
            "scenario IS NULL OR (scenario <> '' AND scenario = btrim(scenario))",
            name="env_input_scenario_nonempty_trimmed",
        ),
        CheckConstraint(
            "crs ~ '^EPSG:[1-9][0-9]*$'",
            name="env_input_crs_epsg_positive",
        ),
        CheckConstraint(
            "crs <> 'EPSG:4326' OR ("
            "extent_west >= -180 AND extent_east <= 180 AND "
            "extent_south >= -90 AND extent_north <= 90)",
            name="env_input_epsg4326_extent_bounds",
        ),
        ForeignKeyConstraint(
            ["evaluation_id"],
            [
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}."
                "evaluation_environmental_input_manifests.evaluation_id"
            ],
            name="fk_env_input_manifest",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["evaluation_id", "input_key", "dataset_id", "dataset_version_id"],
            [
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}."
                "evaluation_environmental_input_requests.evaluation_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}."
                "evaluation_environmental_input_requests.input_key",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}."
                "evaluation_environmental_input_requests.dataset_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}."
                "evaluation_environmental_input_requests.dataset_version_id",
            ],
            name="fk_env_input_exact_requested_reference",
            ondelete="CASCADE",
        ),
        UniqueConstraint(
            "evaluation_id",
            "input_key",
            name="uq_evaluation_environmental_inputs_key",
        ),
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )
    position: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    input_key: Mapped[str] = mapped_column(String(120), nullable=False)
    dataset_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    dataset_name: Mapped[str] = mapped_column(String(120), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    variable: Mapped[str] = mapped_column(String(120), nullable=False)
    unit: Mapped[str] = mapped_column(String(64), nullable=False)
    dataset_version_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        nullable=False,
    )
    version_identifier: Mapped[str] = mapped_column(String(120), nullable=False)
    checksum: Mapped[str] = mapped_column(String(256), nullable=False)
    storage_reference: Mapped[str] = mapped_column(Text, nullable=False)
    crs: Mapped[str] = mapped_column(String(32), nullable=False)
    resolution_x: Mapped[float] = mapped_column(Float, nullable=False)
    resolution_y: Mapped[float] = mapped_column(Float, nullable=False)
    resolution_unit: Mapped[str] = mapped_column(String(32), nullable=False)
    extent_west: Mapped[float] = mapped_column(Float, nullable=False)
    extent_south: Mapped[float] = mapped_column(Float, nullable=False)
    extent_east: Mapped[float] = mapped_column(Float, nullable=False)
    extent_north: Mapped[float] = mapped_column(Float, nullable=False)
    valid_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    valid_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    scenario: Mapped[str | None] = mapped_column(String(120), nullable=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

class EvaluationCommonSupportRecord(Base):
    __tablename__ = "evaluation_common_support"
    __table_args__ = (
        CheckConstraint(
            "status IN ("
            "'comparable', "
            "'no_common_coverage', "
            "'no_successful_crops'"
            ")",
            name="common_support_status_supported",
        ),
        CheckConstraint(
            "parcel_area_m2 > 0",
            name="common_support_parcel_area_positive",
        ),
        CheckConstraint(
            "common_valid_area_m2 >= 0 "
            "AND common_valid_area_m2 <= parcel_area_m2",
            name="common_support_area_valid",
        ),
        CheckConstraint(
            "common_coverage_fraction >= 0 "
            "AND common_coverage_fraction <= 1",
            name="common_support_fraction_valid",
        ),
        CheckConstraint(
            "("
            "status = 'no_successful_crops' "
            "AND method IS NULL "
            "AND area_crs IS NULL "
            "AND common_valid_area_m2 = 0 "
            "AND common_coverage_fraction = 0 "
            "AND cardinality(eligible_crops) = 0 "
            "AND cardinality(excluded_without_coverage) = 0"
            ") OR ("
            "status IN ('comparable', 'no_common_coverage') "
            "AND method = 'area_weighted_mean_on_common_valid_cells' "
            "AND area_crs = 'EPSG:6933'"
            ")",
            name="common_support_payload_matches_status",
        ),
        CheckConstraint(
            "status <> 'comparable' "
            "OR (common_valid_area_m2 > 0 "
            "AND cardinality(eligible_crops) > 0)",
            name="common_support_comparable_has_area",
        ),
        CheckConstraint(
            "status <> 'no_common_coverage' "
            "OR (common_valid_area_m2 = 0 "
            "AND common_coverage_fraction = 0)",
            name="common_support_no_common_has_zero_area",
        ),
        CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="common_support_water_regime_supported",
        ),
        ForeignKeyConstraint(
            ["evaluation_id", "water_regime"],
            [
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.evaluation_water_regimes.evaluation_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.evaluation_water_regimes.water_regime",
            ],
            name="fk_common_support_requested_water_regime",
            ondelete="CASCADE",
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
    water_regime: Mapped[str] = mapped_column(
        String(16),
        primary_key=True,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )
    method: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )
    area_crs: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )
    parcel_area_m2: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    common_valid_area_m2: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    common_coverage_fraction: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    eligible_crops: Mapped[list[str]] = mapped_column(
        ARRAY(String(120)),
        nullable=False,
    )
    excluded_without_coverage: Mapped[list[str]] = mapped_column(
        ARRAY(String(120)),
        nullable=False,
    )

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


class EvaluationComparableCropRecord(Base):
    __tablename__ = "evaluation_comparable_crops"
    __table_args__ = (
        CheckConstraint(
            "position >= 0",
            name="comparable_crop_position_nonnegative",
        ),
        CheckConstraint(
            "crop_id <> '' AND crop_id = btrim(crop_id)",
            name="comparable_crop_id_nonempty_trimmed",
        ),
        CheckConstraint(
            "mean >= 0 AND mean <= 100",
            name="comparable_crop_mean_valid",
        ),
        CheckConstraint(
            "rank >= 1",
            name="comparable_crop_rank_positive",
        ),
        CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="comparable_crop_water_regime_supported",
        ),
        UniqueConstraint(
            "evaluation_id",
            "water_regime",
            "position",
            name="uq_evaluation_comparable_crops_position",
        ),
        ForeignKeyConstraint(
            ["evaluation_id", "crop_id"],
            [
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.evaluation_crops.evaluation_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.evaluation_crops.crop_id",
            ],
            name="fk_evaluation_comparable_crops_requested_crop",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["evaluation_id", "water_regime"],
            [
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.evaluation_water_regimes.evaluation_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.evaluation_water_regimes.water_regime",
            ],
            name="fk_comparable_crops_requested_water_regime",
            ondelete="CASCADE",
        ),
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )
    crop_id: Mapped[str] = mapped_column(
        String(120),
        primary_key=True,
        nullable=False,
    )
    water_regime: Mapped[str] = mapped_column(
        String(16),
        primary_key=True,
        nullable=False,
    )
    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    mean: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    rank: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


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
            "coverage_fraction IS NULL OR (coverage_fraction >= 0 AND coverage_fraction <= 1)",
            name="crop_outcome_coverage_fraction_valid",
        ),
        CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="crop_outcome_water_regime_supported",
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
        ForeignKeyConstraint(
            ["evaluation_id", "water_regime"],
            [
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.evaluation_water_regimes.evaluation_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.evaluation_water_regimes.water_regime",
            ],
            name="fk_crop_outcomes_requested_water_regime",
            ondelete="CASCADE",
        ),
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, nullable=False
    )
    crop_id: Mapped[str] = mapped_column(String(120), primary_key=True, nullable=False)
    water_regime: Mapped[str] = mapped_column(String(16), primary_key=True, nullable=False)
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


class ScientificSourceFingerprintRecord(Base):
    __tablename__ = "scientific_source_fingerprints"
    __table_args__ = (
        CheckConstraint(
            "position >= 0",
            name="scientific_source_fingerprint_position_nonnegative",
        ),
        CheckConstraint(
            "source_reference <> '' AND source_reference = btrim(source_reference)",
            name="scientific_source_fingerprint_reference_nonempty_trimmed",
        ),
        CheckConstraint(
            "sha256 ~ '^[0-9a-f]{64}$'",
            name="scientific_source_fingerprint_sha256_valid",
        ),
        CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="scientific_source_fingerprint_water_regime_supported",
        ),
        ForeignKeyConstraint(
            ["evaluation_id", "crop_id", "water_regime"],
            [
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.crop_outcomes.evaluation_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.crop_outcomes.crop_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.crop_outcomes.water_regime",
            ],
            name="fk_scientific_source_fingerprints_crop_outcome",
            ondelete="CASCADE",
        ),
        UniqueConstraint(
            "evaluation_id",
            "crop_id",
            "water_regime",
            "source_reference",
            name="uq_scientific_source_fingerprint_reference",
        ),
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )
    crop_id: Mapped[str] = mapped_column(
        String(120),
        primary_key=True,
        nullable=False,
    )
    water_regime: Mapped[str] = mapped_column(
        String(16),
        primary_key=True,
        nullable=False,
    )
    position: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    source_reference: Mapped[str] = mapped_column(Text, nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)


class ScientificArtifactRecord(Base):
    __tablename__ = "scientific_artifacts"
    __table_args__ = (
        CheckConstraint(
            "role IN ('crop_suitability', 'crop_limiting_factor')",
            name="scientific_artifact_role_supported",
        ),
        CheckConstraint(
            "storage_reference <> '' "
            "AND storage_reference = btrim(storage_reference)",
            name="scientific_artifact_storage_reference_nonempty_trimmed",
        ),
        CheckConstraint(
            "sha256 ~ '^[0-9a-f]{64}$'",
            name="scientific_artifact_sha256_valid",
        ),
        CheckConstraint(
            "media_type <> '' AND media_type = btrim(media_type)",
            name="scientific_artifact_media_type_nonempty_trimmed",
        ),
        CheckConstraint(
            "size_bytes > 0",
            name="scientific_artifact_size_positive",
        ),
        CheckConstraint(
            "crs <> '' AND crs = btrim(crs)",
            name="scientific_artifact_crs_nonempty_trimmed",
        ),
        CheckConstraint(
            "width > 0",
            name="scientific_artifact_width_positive",
        ),
        CheckConstraint(
            "height > 0",
            name="scientific_artifact_height_positive",
        ),
        CheckConstraint(
            "jsonb_typeof(transform) = 'array' "
            "AND jsonb_array_length(transform) = 6",
            name="scientific_artifact_transform_six_coefficients",
        ),
        CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="scientific_artifact_water_regime_supported",
        ),
        ForeignKeyConstraint(
            ["evaluation_id", "crop_id", "water_regime"],
            [
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.crop_outcomes.evaluation_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.crop_outcomes.crop_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.crop_outcomes.water_regime",
            ],
            name="fk_scientific_artifacts_crop_outcome",
            ondelete="CASCADE",
        ),
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )
    crop_id: Mapped[str] = mapped_column(
        String(120),
        primary_key=True,
        nullable=False,
    )
    water_regime: Mapped[str] = mapped_column(
        String(16),
        primary_key=True,
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        nullable=False,
    )
    storage_reference: Mapped[str] = mapped_column(Text, nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    media_type: Mapped[str] = mapped_column(String(120), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    crs: Mapped[str] = mapped_column(Text, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    transform: Mapped[list[float]] = mapped_column(JSONB, nullable=False)
    nodata: Mapped[float | None] = mapped_column(Float, nullable=True)


class CropLimitationEvidenceRecord(Base):
    __tablename__ = "crop_limitation_evidence"
    __table_args__ = (
        CheckConstraint(
            "availability IN ('available', 'partial', 'unavailable')",
            name="crop_limitation_evidence_availability_supported",
        ),
        CheckConstraint(
            "(availability = 'available' AND reason IS NULL) OR "
            "(availability IN ('partial', 'unavailable') AND reason IS NOT NULL)",
            name="crop_limitation_evidence_reason_matches_availability",
        ),
        CheckConstraint(
            "jsonb_typeof(warnings) = 'array'",
            name="crop_limitation_evidence_warnings_array",
        ),
        CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="crop_limitation_evidence_water_regime_supported",
        ),
        ForeignKeyConstraint(
            ["evaluation_id", "crop_id", "water_regime"],
            [
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.crop_outcomes.evaluation_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.crop_outcomes.crop_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.crop_outcomes.water_regime",
            ],
            name="fk_crop_limitation_evidence_crop_outcome",
            ondelete="CASCADE",
        ),
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, nullable=False
    )
    crop_id: Mapped[str] = mapped_column(String(120), primary_key=True, nullable=False)
    water_regime: Mapped[str] = mapped_column(String(16), primary_key=True, nullable=False)
    availability: Mapped[str] = mapped_column(String(16), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    warnings: Mapped[list[str]] = mapped_column(JSONB, nullable=False)


class CropLimitingFactorRecord(Base):
    __tablename__ = "crop_limiting_factors"
    __table_args__ = (
        CheckConstraint(
            "factor_code <> '' AND factor_code = btrim(factor_code)",
            name="crop_limiting_factor_code_nonempty_trimmed",
        ),
        CheckConstraint(
            "label <> '' AND label = btrim(label)",
            name="crop_limiting_factor_label_nonempty_trimmed",
        ),
        CheckConstraint(
            "affected_cells >= 0",
            name="crop_limiting_factor_cells_nonnegative",
        ),
        CheckConstraint(
            "affected_area_m2 >= 0",
            name="crop_limiting_factor_area_nonnegative",
        ),
        CheckConstraint(
            "affected_fraction >= 0 AND affected_fraction <= 1",
            name="crop_limiting_factor_fraction_valid",
        ),
        CheckConstraint(
            "source_storage_reference IS NULL OR "
            "(source_storage_reference <> '' "
            "AND source_storage_reference = btrim(source_storage_reference))",
            name="crop_limiting_factor_storage_reference_valid",
        ),
        CheckConstraint(
            "source_sha256 ~ '^[0-9a-f]{64}$'",
            name="crop_limiting_factor_sha256_valid",
        ),
        CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="crop_limiting_factor_water_regime_supported",
        ),
        ForeignKeyConstraint(
            ["evaluation_id", "crop_id", "water_regime"],
            [
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.crop_limitation_evidence.evaluation_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.crop_limitation_evidence.crop_id",
                f"{AGROCLIMATIC_EVALUATION_SCHEMA}.crop_limitation_evidence.water_regime",
            ],
            name="fk_crop_limiting_factors_limitation_evidence",
            ondelete="CASCADE",
        ),
        UniqueConstraint(
            "evaluation_id",
            "crop_id",
            "water_regime",
            "factor_code",
            name="uq_crop_limiting_factor_code",
        ),
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, nullable=False
    )
    crop_id: Mapped[str] = mapped_column(String(120), primary_key=True, nullable=False)
    water_regime: Mapped[str] = mapped_column(String(16), primary_key=True, nullable=False)
    raw_code: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    factor_code: Mapped[str] = mapped_column(String(160), nullable=False)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    affected_cells: Mapped[int] = mapped_column(Integer, nullable=False)
    affected_area_m2: Mapped[float] = mapped_column(Float, nullable=False)
    affected_fraction: Mapped[float] = mapped_column(Float, nullable=False)
    dominant: Mapped[bool] = mapped_column(Boolean, nullable=False)
    source_storage_reference: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
