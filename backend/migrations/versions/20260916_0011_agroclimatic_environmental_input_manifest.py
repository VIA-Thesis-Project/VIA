"""Persist exact environmental input requests and immutable manifests.

Revision ID: 20260916_0011
Revises: 20260916_0010
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260916_0011"
down_revision: str | None = "20260916_0010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "agroclimatic_evaluation"


def upgrade() -> None:
    op.create_table(
        "evaluation_environmental_input_requests",
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("input_key", sa.String(length=120), nullable=False),
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dataset_version_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.CheckConstraint(
            "position >= 0",
            name="env_input_request_position_nonnegative",
        ),
        sa.CheckConstraint(
            "input_key <> '' AND input_key = btrim(input_key)",
            name="env_input_request_key_nonempty_trimmed",
        ),
        sa.ForeignKeyConstraint(
            ["evaluation_id"],
            [f"{SCHEMA}.evaluations.id"],
            name="fk_env_input_request_evaluation",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "evaluation_id",
            "position",
            name="pk_evaluation_environmental_input_requests",
        ),
        sa.UniqueConstraint(
            "evaluation_id",
            "input_key",
            name="uq_env_input_request_key",
        ),
        sa.UniqueConstraint(
            "evaluation_id",
            "input_key",
            "dataset_id",
            "dataset_version_id",
            name="uq_env_input_request_exact_reference",
        ),
        schema=SCHEMA,
    )

    op.create_table(
        "evaluation_environmental_input_manifests",
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["evaluation_id"],
            [f"{SCHEMA}.evaluations.id"],
            name="fk_env_input_manifest_evaluation",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "evaluation_id",
            name="pk_evaluation_environmental_input_manifests",
        ),
        schema=SCHEMA,
    )

    op.create_table(
        "evaluation_environmental_inputs",
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("input_key", sa.String(length=120), nullable=False),
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dataset_name", sa.String(length=120), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("variable", sa.String(length=120), nullable=False),
        sa.Column("unit", sa.String(length=64), nullable=False),
        sa.Column("dataset_version_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("version_identifier", sa.String(length=120), nullable=False),
        sa.Column("checksum", sa.String(length=256), nullable=False),
        sa.Column("storage_reference", sa.Text(), nullable=False),
        sa.Column("crs", sa.String(length=32), nullable=False),
        sa.Column("resolution_x", sa.Float(), nullable=False),
        sa.Column("resolution_y", sa.Float(), nullable=False),
        sa.Column("resolution_unit", sa.String(length=32), nullable=False),
        sa.Column("extent_west", sa.Float(), nullable=False),
        sa.Column("extent_south", sa.Float(), nullable=False),
        sa.Column("extent_east", sa.Float(), nullable=False),
        sa.Column("extent_north", sa.Float(), nullable=False),
        sa.Column("valid_from", sa.Date(), nullable=True),
        sa.Column("valid_to", sa.Date(), nullable=True),
        sa.Column("scenario", sa.String(length=120), nullable=True),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "position >= 0",
            name="env_input_position_nonnegative",
        ),
        sa.CheckConstraint(
            "input_key <> '' AND input_key = btrim(input_key)",
            name="env_input_key_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "dataset_name <> '' AND dataset_name = btrim(dataset_name)",
            name="env_input_dataset_name_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "source <> '' AND source = btrim(source)",
            name="env_input_source_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "variable <> '' AND variable = btrim(variable)",
            name="env_input_variable_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "unit <> '' AND unit = btrim(unit)",
            name="env_input_unit_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "version_identifier <> '' AND version_identifier = btrim(version_identifier)",
            name="env_input_version_identifier_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "checksum <> '' AND checksum = btrim(checksum)",
            name="env_input_checksum_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "storage_reference <> '' AND storage_reference = btrim(storage_reference)",
            name="env_input_storage_reference_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "resolution_unit <> '' AND resolution_unit = btrim(resolution_unit)",
            name="env_input_resolution_unit_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "resolution_x > 0",
            name="env_input_resolution_x_positive",
        ),
        sa.CheckConstraint(
            "resolution_y > 0",
            name="env_input_resolution_y_positive",
        ),
        sa.CheckConstraint(
            "extent_west < extent_east",
            name="env_input_west_before_east",
        ),
        sa.CheckConstraint(
            "extent_south < extent_north",
            name="env_input_south_before_north",
        ),
        sa.CheckConstraint(
            "valid_from IS NULL OR valid_to IS NULL OR valid_from <= valid_to",
            name="env_input_validity_window_ordered",
        ),
        sa.CheckConstraint(
            "scenario IS NULL OR (scenario <> '' AND scenario = btrim(scenario))",
            name="env_input_scenario_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "crs ~ '^EPSG:[1-9][0-9]*$'",
            name="env_input_crs_epsg_positive",
        ),
        sa.CheckConstraint(
            "crs <> 'EPSG:4326' OR ("
            "extent_west >= -180 AND extent_east <= 180 AND "
            "extent_south >= -90 AND extent_north <= 90)",
            name="env_input_epsg4326_extent_bounds",
        ),
        sa.ForeignKeyConstraint(
            ["evaluation_id"],
            [f"{SCHEMA}.evaluation_environmental_input_manifests.evaluation_id"],
            name="fk_env_input_manifest",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["evaluation_id", "input_key", "dataset_id", "dataset_version_id"],
            [
                f"{SCHEMA}.evaluation_environmental_input_requests.evaluation_id",
                f"{SCHEMA}.evaluation_environmental_input_requests.input_key",
                f"{SCHEMA}.evaluation_environmental_input_requests.dataset_id",
                f"{SCHEMA}.evaluation_environmental_input_requests.dataset_version_id",
            ],
            name="fk_env_input_exact_requested_reference",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "evaluation_id",
            "position",
            name="pk_evaluation_environmental_inputs",
        ),
        sa.UniqueConstraint(
            "evaluation_id",
            "input_key",
            name="uq_evaluation_environmental_inputs_key",
        ),
        schema=SCHEMA,
    )


def downgrade() -> None:
    op.drop_table("evaluation_environmental_inputs", schema=SCHEMA)
    op.drop_table("evaluation_environmental_input_manifests", schema=SCHEMA)
    op.drop_table("evaluation_environmental_input_requests", schema=SCHEMA)
