"""Persist deterministic SAME-RUN limiting-factor evidence.

Revision ID: 20260918_0014
Revises: 20260917_0013
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260918_0014"
down_revision: str | None = "20260917_0013"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "agroclimatic_evaluation"


def upgrade() -> None:
    op.drop_constraint(
        "scientific_artifact_role_supported",
        "scientific_artifacts",
        schema=SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        "scientific_artifact_role_supported",
        "scientific_artifacts",
        "role IN ('crop_suitability', 'crop_limiting_factor')",
        schema=SCHEMA,
    )

    op.create_table(
        "crop_limitation_evidence",
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("crop_id", sa.String(length=120), nullable=False),
        sa.Column("water_regime", sa.String(length=16), nullable=False),
        sa.Column("availability", sa.String(length=16), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("warnings", postgresql.JSONB(), nullable=False),
        sa.CheckConstraint(
            "availability IN ('available', 'partial', 'unavailable')",
            name="crop_limitation_evidence_availability_supported",
        ),
        sa.CheckConstraint(
            "(availability = 'available' AND reason IS NULL) OR "
            "(availability IN ('partial', 'unavailable') AND reason IS NOT NULL)",
            name="crop_limitation_evidence_reason_matches_availability",
        ),
        sa.CheckConstraint(
            "jsonb_typeof(warnings) = 'array'",
            name="crop_limitation_evidence_warnings_array",
        ),
        sa.CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="crop_limitation_evidence_water_regime_supported",
        ),
        sa.ForeignKeyConstraint(
            ["evaluation_id", "crop_id", "water_regime"],
            [
                f"{SCHEMA}.crop_outcomes.evaluation_id",
                f"{SCHEMA}.crop_outcomes.crop_id",
                f"{SCHEMA}.crop_outcomes.water_regime",
            ],
            name="fk_crop_limitation_evidence_crop_outcome",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "evaluation_id",
            "crop_id",
            "water_regime",
            name="pk_crop_limitation_evidence",
        ),
        schema=SCHEMA,
    )

    op.create_table(
        "crop_limiting_factors",
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("crop_id", sa.String(length=120), nullable=False),
        sa.Column("water_regime", sa.String(length=16), nullable=False),
        sa.Column("raw_code", sa.Integer(), nullable=False),
        sa.Column("factor_code", sa.String(length=160), nullable=False),
        sa.Column("label", sa.Text(), nullable=False),
        sa.Column("affected_cells", sa.Integer(), nullable=False),
        sa.Column("affected_area_m2", sa.Float(), nullable=False),
        sa.Column("affected_fraction", sa.Float(), nullable=False),
        sa.Column("dominant", sa.Boolean(), nullable=False),
        sa.Column("source_storage_reference", sa.Text(), nullable=True),
        sa.Column("source_sha256", sa.String(length=64), nullable=False),
        sa.CheckConstraint(
            "factor_code <> '' AND factor_code = btrim(factor_code)",
            name="crop_limiting_factor_code_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "label <> '' AND label = btrim(label)",
            name="crop_limiting_factor_label_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "affected_cells >= 0",
            name="crop_limiting_factor_cells_nonnegative",
        ),
        sa.CheckConstraint(
            "affected_area_m2 >= 0",
            name="crop_limiting_factor_area_nonnegative",
        ),
        sa.CheckConstraint(
            "affected_fraction >= 0 AND affected_fraction <= 1",
            name="crop_limiting_factor_fraction_valid",
        ),
        sa.CheckConstraint(
            "source_storage_reference IS NULL OR "
            "(source_storage_reference <> '' "
            "AND source_storage_reference = btrim(source_storage_reference))",
            name="crop_limiting_factor_storage_reference_valid",
        ),
        sa.CheckConstraint(
            "source_sha256 ~ '^[0-9a-f]{64}$'",
            name="crop_limiting_factor_sha256_valid",
        ),
        sa.CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="crop_limiting_factor_water_regime_supported",
        ),
        sa.ForeignKeyConstraint(
            ["evaluation_id", "crop_id", "water_regime"],
            [
                f"{SCHEMA}.crop_limitation_evidence.evaluation_id",
                f"{SCHEMA}.crop_limitation_evidence.crop_id",
                f"{SCHEMA}.crop_limitation_evidence.water_regime",
            ],
            name="fk_crop_limiting_factors_limitation_evidence",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "evaluation_id",
            "crop_id",
            "water_regime",
            "raw_code",
            name="pk_crop_limiting_factors",
        ),
        sa.UniqueConstraint(
            "evaluation_id",
            "crop_id",
            "water_regime",
            "factor_code",
            name="uq_crop_limiting_factor_code",
        ),
        schema=SCHEMA,
    )


def downgrade() -> None:
    op.drop_table("crop_limiting_factors", schema=SCHEMA)
    op.drop_table("crop_limitation_evidence", schema=SCHEMA)
    op.drop_constraint(
        "scientific_artifact_role_supported",
        "scientific_artifacts",
        schema=SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        "scientific_artifact_role_supported",
        "scientific_artifacts",
        "role IN ('crop_suitability')",
        schema=SCHEMA,
    )
