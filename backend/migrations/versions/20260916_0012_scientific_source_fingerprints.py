"""Persist ordered per-crop scientific source fingerprints.

Revision ID: 20260916_0012
Revises: 20260916_0011
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260916_0012"
down_revision: str | None = "20260916_0011"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "agroclimatic_evaluation"


def upgrade() -> None:
    op.create_table(
        "scientific_source_fingerprints",
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("crop_id", sa.String(length=120), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("source_reference", sa.Text(), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.CheckConstraint(
            "position >= 0",
            name="scientific_source_fingerprint_position_nonnegative",
        ),
        sa.CheckConstraint(
            "source_reference <> '' AND source_reference = btrim(source_reference)",
            name="scientific_source_fingerprint_reference_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "sha256 ~ '^[0-9a-f]{64}$'",
            name="scientific_source_fingerprint_sha256_valid",
        ),
        sa.ForeignKeyConstraint(
            ["evaluation_id", "crop_id"],
            [
                f"{SCHEMA}.crop_outcomes.evaluation_id",
                f"{SCHEMA}.crop_outcomes.crop_id",
            ],
            name="fk_scientific_source_fingerprints_crop_outcome",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "evaluation_id",
            "crop_id",
            "position",
            name="pk_scientific_source_fingerprints",
        ),
        sa.UniqueConstraint(
            "evaluation_id",
            "crop_id",
            "source_reference",
            name="uq_scientific_source_fingerprint_reference",
        ),
        schema=SCHEMA,
    )


def downgrade() -> None:
    op.drop_table("scientific_source_fingerprints", schema=SCHEMA)
