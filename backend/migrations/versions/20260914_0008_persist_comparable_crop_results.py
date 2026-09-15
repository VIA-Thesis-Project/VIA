"""Persist comparable crop results and scientific ranking.

Revision ID: 20260914_0008

Revises: 20260914_0007

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260914_0008"

down_revision: str | None = "20260914_0007"

branch_labels: str | Sequence[str] | None = None

depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "evaluation_comparable_crops",
        sa.Column(
            "evaluation_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "crop_id",
            sa.String(length=120),
            nullable=False,
        ),
        sa.Column(
            "position",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "mean",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "rank",
            sa.Integer(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "position >= 0",
            name="comparable_crop_position_nonnegative",
        ),
        sa.CheckConstraint(
            "crop_id <> '' AND crop_id = btrim(crop_id)",
            name="comparable_crop_id_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "mean >= 0 AND mean <= 100",
            name="comparable_crop_mean_valid",
        ),
        sa.CheckConstraint(
            "rank >= 1",
            name="comparable_crop_rank_positive",
        ),
        sa.ForeignKeyConstraint(
            ["evaluation_id", "crop_id"],
            [
                "agroclimatic_evaluation.evaluation_crops.evaluation_id",
                "agroclimatic_evaluation.evaluation_crops.crop_id",
            ],
            name="fk_evaluation_comparable_crops_requested_crop",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "evaluation_id",
            "crop_id",
            name="pk_evaluation_comparable_crops",
        ),
        sa.UniqueConstraint(
            "evaluation_id",
            "position",
            name="uq_evaluation_comparable_crops_position",
        ),
        schema="agroclimatic_evaluation",
    )


def downgrade() -> None:
    op.drop_table(
        "evaluation_comparable_crops",
        schema="agroclimatic_evaluation",
    )
