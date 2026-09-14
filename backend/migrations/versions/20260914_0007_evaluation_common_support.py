"""Persist evaluation common spatial support.

Revision ID: 20260914_0007
Revises: 20260914_0006
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260914_0007"
down_revision: str | None = "20260914_0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "evaluation_common_support",
        sa.Column(
            "evaluation_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=32),
            nullable=False,
        ),
        sa.Column(
            "method",
            sa.String(length=120),
            nullable=True,
        ),
        sa.Column(
            "area_crs",
            sa.String(length=32),
            nullable=True,
        ),
        sa.Column(
            "parcel_area_m2",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "common_valid_area_m2",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "common_coverage_fraction",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "eligible_crops",
            postgresql.ARRAY(sa.String(length=120)),
            nullable=False,
        ),
        sa.Column(
            "excluded_without_coverage",
            postgresql.ARRAY(sa.String(length=120)),
            nullable=False,
        ),
        sa.CheckConstraint(
            "status IN ("
            "'comparable', "
            "'no_common_coverage', "
            "'no_successful_crops'"
            ")",
            name="common_support_status_supported",
        ),
        sa.CheckConstraint(
            "parcel_area_m2 > 0",
            name="common_support_parcel_area_positive",
        ),
        sa.CheckConstraint(
            "common_valid_area_m2 >= 0 "
            "AND common_valid_area_m2 <= parcel_area_m2",
            name="common_support_area_valid",
        ),
        sa.CheckConstraint(
            "common_coverage_fraction >= 0 "
            "AND common_coverage_fraction <= 1",
            name="common_support_fraction_valid",
        ),
        sa.CheckConstraint(
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
        sa.CheckConstraint(
            "status <> 'comparable' "
            "OR (common_valid_area_m2 > 0 "
            "AND cardinality(eligible_crops) > 0)",
            name="common_support_comparable_has_area",
        ),
        sa.CheckConstraint(
            "status <> 'no_common_coverage' "
            "OR (common_valid_area_m2 = 0 "
            "AND common_coverage_fraction = 0)",
            name="common_support_no_common_has_zero_area",
        ),
        sa.ForeignKeyConstraint(
            ["evaluation_id"],
            ["agroclimatic_evaluation.evaluations.id"],
            name="fk_evaluation_common_support_evaluation",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "evaluation_id",
            name="pk_evaluation_common_support",
        ),
        schema="agroclimatic_evaluation",
    )


def downgrade() -> None:
    op.drop_table(
        "evaluation_common_support",
        schema="agroclimatic_evaluation",
    )