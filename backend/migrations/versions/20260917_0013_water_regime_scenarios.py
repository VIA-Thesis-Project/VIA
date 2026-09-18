"""Persist explicit rainfed and irrigated evaluation scenarios.

Revision ID: 20260917_0013
Revises: 20260916_0012
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260917_0013"
down_revision: str | None = "20260916_0012"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "agroclimatic_evaluation"
WATER_REGIME_TABLE = "evaluation_water_regimes"
SCENARIO_TABLES = (
    "evaluation_common_support",
    "evaluation_comparable_crops",
    "crop_outcomes",
    "scientific_source_fingerprints",
    "scientific_artifacts",
)


def upgrade() -> None:
    op.create_table(
        WATER_REGIME_TABLE,
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("water_regime", sa.String(length=16), nullable=False),
        sa.CheckConstraint(
            "position >= 0",
            name="water_regime_position_nonnegative",
        ),
        sa.CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="water_regime_supported",
        ),
        sa.ForeignKeyConstraint(
            ["evaluation_id"],
            [f"{SCHEMA}.evaluations.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "evaluation_id",
            "position",
            name="pk_evaluation_water_regimes",
        ),
        sa.UniqueConstraint(
            "evaluation_id",
            "water_regime",
            name="uq_evaluation_water_regimes_regime",
        ),
        schema=SCHEMA,
    )
    op.execute(
        sa.text(
            f"INSERT INTO {SCHEMA}.{WATER_REGIME_TABLE} "
            "(evaluation_id, position, water_regime) "
            f"SELECT id, 0, 'rainfed' FROM {SCHEMA}.evaluations"
        )
    )

    for table in SCENARIO_TABLES:
        op.add_column(
            table,
            sa.Column("water_regime", sa.String(length=16), nullable=True),
            schema=SCHEMA,
        )
        op.execute(
            sa.text(
                f"UPDATE {SCHEMA}.{table} "
                "SET water_regime = 'rainfed' WHERE water_regime IS NULL"
            )
        )
        op.alter_column(
            table,
            "water_regime",
            existing_type=sa.String(length=16),
            nullable=False,
            schema=SCHEMA,
        )

    # Drop foreign keys that depend on crop_outcomes' old two-column key.
    op.drop_constraint(
        "fk_scientific_artifacts_crop_outcome",
        "scientific_artifacts",
        schema=SCHEMA,
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_scientific_source_fingerprints_crop_outcome",
        "scientific_source_fingerprints",
        schema=SCHEMA,
        type_="foreignkey",
    )

    op.drop_constraint(
        "pk_crop_outcomes",
        "crop_outcomes",
        schema=SCHEMA,
        type_="primary",
    )
    op.create_primary_key(
        "pk_crop_outcomes",
        "crop_outcomes",
        ["evaluation_id", "crop_id", "water_regime"],
        schema=SCHEMA,
    )
    op.create_check_constraint(
        "crop_outcome_water_regime_supported",
        "crop_outcomes",
        "water_regime IN ('rainfed', 'irrigated')",
        schema=SCHEMA,
    )
    op.create_foreign_key(
        "fk_crop_outcomes_requested_water_regime",
        "crop_outcomes",
        WATER_REGIME_TABLE,
        ["evaluation_id", "water_regime"],
        ["evaluation_id", "water_regime"],
        source_schema=SCHEMA,
        referent_schema=SCHEMA,
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "pk_scientific_artifacts",
        "scientific_artifacts",
        schema=SCHEMA,
        type_="primary",
    )
    op.create_primary_key(
        "pk_scientific_artifacts",
        "scientific_artifacts",
        ["evaluation_id", "crop_id", "water_regime", "role"],
        schema=SCHEMA,
    )
    op.create_check_constraint(
        "scientific_artifact_water_regime_supported",
        "scientific_artifacts",
        "water_regime IN ('rainfed', 'irrigated')",
        schema=SCHEMA,
    )
    op.create_foreign_key(
        "fk_scientific_artifacts_crop_outcome",
        "scientific_artifacts",
        "crop_outcomes",
        ["evaluation_id", "crop_id", "water_regime"],
        ["evaluation_id", "crop_id", "water_regime"],
        source_schema=SCHEMA,
        referent_schema=SCHEMA,
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "uq_scientific_source_fingerprint_reference",
        "scientific_source_fingerprints",
        schema=SCHEMA,
        type_="unique",
    )
    op.drop_constraint(
        "pk_scientific_source_fingerprints",
        "scientific_source_fingerprints",
        schema=SCHEMA,
        type_="primary",
    )
    op.create_primary_key(
        "pk_scientific_source_fingerprints",
        "scientific_source_fingerprints",
        ["evaluation_id", "crop_id", "water_regime", "position"],
        schema=SCHEMA,
    )
    op.create_unique_constraint(
        "uq_scientific_source_fingerprint_reference",
        "scientific_source_fingerprints",
        ["evaluation_id", "crop_id", "water_regime", "source_reference"],
        schema=SCHEMA,
    )
    op.create_check_constraint(
        "scientific_source_fingerprint_water_regime_supported",
        "scientific_source_fingerprints",
        "water_regime IN ('rainfed', 'irrigated')",
        schema=SCHEMA,
    )
    op.create_foreign_key(
        "fk_scientific_source_fingerprints_crop_outcome",
        "scientific_source_fingerprints",
        "crop_outcomes",
        ["evaluation_id", "crop_id", "water_regime"],
        ["evaluation_id", "crop_id", "water_regime"],
        source_schema=SCHEMA,
        referent_schema=SCHEMA,
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "pk_evaluation_common_support",
        "evaluation_common_support",
        schema=SCHEMA,
        type_="primary",
    )
    op.create_primary_key(
        "pk_evaluation_common_support",
        "evaluation_common_support",
        ["evaluation_id", "water_regime"],
        schema=SCHEMA,
    )
    op.create_check_constraint(
        "common_support_water_regime_supported",
        "evaluation_common_support",
        "water_regime IN ('rainfed', 'irrigated')",
        schema=SCHEMA,
    )
    op.create_foreign_key(
        "fk_common_support_requested_water_regime",
        "evaluation_common_support",
        WATER_REGIME_TABLE,
        ["evaluation_id", "water_regime"],
        ["evaluation_id", "water_regime"],
        source_schema=SCHEMA,
        referent_schema=SCHEMA,
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "uq_evaluation_comparable_crops_position",
        "evaluation_comparable_crops",
        schema=SCHEMA,
        type_="unique",
    )
    op.drop_constraint(
        "pk_evaluation_comparable_crops",
        "evaluation_comparable_crops",
        schema=SCHEMA,
        type_="primary",
    )
    op.create_primary_key(
        "pk_evaluation_comparable_crops",
        "evaluation_comparable_crops",
        ["evaluation_id", "crop_id", "water_regime"],
        schema=SCHEMA,
    )
    op.create_unique_constraint(
        "uq_evaluation_comparable_crops_position",
        "evaluation_comparable_crops",
        ["evaluation_id", "water_regime", "position"],
        schema=SCHEMA,
    )
    op.create_check_constraint(
        "comparable_crop_water_regime_supported",
        "evaluation_comparable_crops",
        "water_regime IN ('rainfed', 'irrigated')",
        schema=SCHEMA,
    )
    op.create_foreign_key(
        "fk_comparable_crops_requested_water_regime",
        "evaluation_comparable_crops",
        WATER_REGIME_TABLE,
        ["evaluation_id", "water_regime"],
        ["evaluation_id", "water_regime"],
        source_schema=SCHEMA,
        referent_schema=SCHEMA,
        ondelete="CASCADE",
    )


def downgrade() -> None:
    # The legacy schema cannot represent multiple regimes. Keep only rainfed data.
    for table in (
        "scientific_artifacts",
        "scientific_source_fingerprints",
        "evaluation_comparable_crops",
        "evaluation_common_support",
        "crop_outcomes",
    ):
        op.execute(
            sa.text(
                f"DELETE FROM {SCHEMA}.{table} WHERE water_regime <> 'rainfed'"
            )
        )

    op.drop_constraint(
        "fk_scientific_artifacts_crop_outcome",
        "scientific_artifacts",
        schema=SCHEMA,
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_scientific_source_fingerprints_crop_outcome",
        "scientific_source_fingerprints",
        schema=SCHEMA,
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_comparable_crops_requested_water_regime",
        "evaluation_comparable_crops",
        schema=SCHEMA,
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_common_support_requested_water_regime",
        "evaluation_common_support",
        schema=SCHEMA,
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_crop_outcomes_requested_water_regime",
        "crop_outcomes",
        schema=SCHEMA,
        type_="foreignkey",
    )

    op.drop_constraint(
        "pk_scientific_artifacts",
        "scientific_artifacts",
        schema=SCHEMA,
        type_="primary",
    )
    op.drop_constraint(
        "scientific_artifact_water_regime_supported",
        "scientific_artifacts",
        schema=SCHEMA,
        type_="check",
    )

    op.drop_constraint(
        "uq_scientific_source_fingerprint_reference",
        "scientific_source_fingerprints",
        schema=SCHEMA,
        type_="unique",
    )
    op.drop_constraint(
        "pk_scientific_source_fingerprints",
        "scientific_source_fingerprints",
        schema=SCHEMA,
        type_="primary",
    )
    op.drop_constraint(
        "scientific_source_fingerprint_water_regime_supported",
        "scientific_source_fingerprints",
        schema=SCHEMA,
        type_="check",
    )

    op.drop_constraint(
        "uq_evaluation_comparable_crops_position",
        "evaluation_comparable_crops",
        schema=SCHEMA,
        type_="unique",
    )
    op.drop_constraint(
        "pk_evaluation_comparable_crops",
        "evaluation_comparable_crops",
        schema=SCHEMA,
        type_="primary",
    )
    op.drop_constraint(
        "comparable_crop_water_regime_supported",
        "evaluation_comparable_crops",
        schema=SCHEMA,
        type_="check",
    )

    op.drop_constraint(
        "pk_evaluation_common_support",
        "evaluation_common_support",
        schema=SCHEMA,
        type_="primary",
    )
    op.drop_constraint(
        "common_support_water_regime_supported",
        "evaluation_common_support",
        schema=SCHEMA,
        type_="check",
    )

    op.drop_constraint(
        "pk_crop_outcomes",
        "crop_outcomes",
        schema=SCHEMA,
        type_="primary",
    )
    op.drop_constraint(
        "crop_outcome_water_regime_supported",
        "crop_outcomes",
        schema=SCHEMA,
        type_="check",
    )
    op.create_primary_key(
        "pk_crop_outcomes",
        "crop_outcomes",
        ["evaluation_id", "crop_id"],
        schema=SCHEMA,
    )

    op.create_primary_key(
        "pk_scientific_artifacts",
        "scientific_artifacts",
        ["evaluation_id", "crop_id", "role"],
        schema=SCHEMA,
    )
    op.create_foreign_key(
        "fk_scientific_artifacts_crop_outcome",
        "scientific_artifacts",
        "crop_outcomes",
        ["evaluation_id", "crop_id"],
        ["evaluation_id", "crop_id"],
        source_schema=SCHEMA,
        referent_schema=SCHEMA,
        ondelete="CASCADE",
    )

    op.create_primary_key(
        "pk_scientific_source_fingerprints",
        "scientific_source_fingerprints",
        ["evaluation_id", "crop_id", "position"],
        schema=SCHEMA,
    )
    op.create_unique_constraint(
        "uq_scientific_source_fingerprint_reference",
        "scientific_source_fingerprints",
        ["evaluation_id", "crop_id", "source_reference"],
        schema=SCHEMA,
    )
    op.create_foreign_key(
        "fk_scientific_source_fingerprints_crop_outcome",
        "scientific_source_fingerprints",
        "crop_outcomes",
        ["evaluation_id", "crop_id"],
        ["evaluation_id", "crop_id"],
        source_schema=SCHEMA,
        referent_schema=SCHEMA,
        ondelete="CASCADE",
    )

    op.create_primary_key(
        "pk_evaluation_common_support",
        "evaluation_common_support",
        ["evaluation_id"],
        schema=SCHEMA,
    )

    op.create_primary_key(
        "pk_evaluation_comparable_crops",
        "evaluation_comparable_crops",
        ["evaluation_id", "crop_id"],
        schema=SCHEMA,
    )
    op.create_unique_constraint(
        "uq_evaluation_comparable_crops_position",
        "evaluation_comparable_crops",
        ["evaluation_id", "position"],
        schema=SCHEMA,
    )

    for table in SCENARIO_TABLES:
        op.drop_column(table, "water_regime", schema=SCHEMA)

    op.drop_table(WATER_REGIME_TABLE, schema=SCHEMA)
