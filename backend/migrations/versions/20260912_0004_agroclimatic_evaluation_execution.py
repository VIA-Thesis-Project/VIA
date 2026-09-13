"""Add Evaluation lifecycle failure and per-crop outcomes.

Revision ID: 20260912_0004
Revises: 20260912_0003
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260912_0004"
down_revision: str | None = "20260912_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "evaluations",
        sa.Column("failure_reason", sa.Text(), nullable=True),
        schema="agroclimatic_evaluation",
    )
    op.create_table(
        "crop_outcomes",
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("crop_id", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("suitability_mean", sa.Float(), nullable=True),
        sa.Column("suitability_minimum", sa.Float(), nullable=True),
        sa.Column("suitability_maximum", sa.Float(), nullable=True),
        sa.Column("valid_cells", sa.Integer(), nullable=True),
        sa.Column("valid_area_m2", sa.Float(), nullable=True),
        sa.Column("coverage_fraction", sa.Float(), nullable=True),
        sa.Column("zero_suitability_area_m2", sa.Float(), nullable=True),
        sa.Column("failure_message", sa.Text(), nullable=True),
        sa.Column("engine_identifier", sa.String(length=120), nullable=False),
        sa.Column("execution_reference", sa.Text(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("elapsed_seconds", sa.Float(), nullable=False),
        sa.Column("execution_mode", sa.String(length=120), nullable=False),
        sa.Column("parcel_sha256", sa.String(length=128), nullable=False),
        sa.Column("parameter_sha256", sa.String(length=128), nullable=True),
        sa.Column("configuration_sha256", sa.String(length=128), nullable=True),
        sa.Column("source_files_unchanged", sa.Boolean(), nullable=False),
        sa.CheckConstraint(
            "status IN ('succeeded', 'no_coverage', 'failed')",
            name="crop_outcome_status_supported",
        ),
        sa.CheckConstraint(
            "elapsed_seconds >= 0",
            name="crop_outcome_elapsed_nonnegative",
        ),
        sa.CheckConstraint(
            "coverage_fraction IS NULL OR "
            "(coverage_fraction >= 0 AND coverage_fraction <= 1)",
            name="crop_outcome_coverage_fraction_valid",
        ),
        sa.CheckConstraint(
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
        sa.ForeignKeyConstraint(
            ["evaluation_id", "crop_id"],
            [
                "agroclimatic_evaluation.evaluation_crops.evaluation_id",
                "agroclimatic_evaluation.evaluation_crops.crop_id",
            ],
            name="fk_crop_outcomes_requested_crop",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "evaluation_id",
            "crop_id",
            name="pk_crop_outcomes",
        ),
        schema="agroclimatic_evaluation",
    )


def downgrade() -> None:
    op.drop_table("crop_outcomes", schema="agroclimatic_evaluation")
    op.drop_column(
        "evaluations",
        "failure_reason",
        schema="agroclimatic_evaluation",
    )
