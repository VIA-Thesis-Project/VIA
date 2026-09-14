"""Persist durable scientific artifact metadata.

Revision ID: 20260914_0006
Revises: 20260912_0005
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260914_0006"
down_revision: str | None = "20260912_0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "scientific_artifacts",
        sa.Column(
            "evaluation_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("crop_id", sa.String(length=120), nullable=False),
        sa.Column("role", sa.String(length=64), nullable=False),
        sa.Column("storage_reference", sa.Text(), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("media_type", sa.String(length=120), nullable=False),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("crs", sa.Text(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column(
            "transform",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("nodata", sa.Float(), nullable=True),
        sa.CheckConstraint(
            "role IN ('crop_suitability')",
            name="scientific_artifact_role_supported",
        ),
        sa.CheckConstraint(
            "storage_reference <> '' "
            "AND storage_reference = btrim(storage_reference)",
            name="scientific_artifact_storage_reference_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "sha256 ~ '^[0-9a-f]{64}$'",
            name="scientific_artifact_sha256_valid",
        ),
        sa.CheckConstraint(
            "media_type <> '' AND media_type = btrim(media_type)",
            name="scientific_artifact_media_type_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "size_bytes > 0",
            name="scientific_artifact_size_positive",
        ),
        sa.CheckConstraint(
            "crs <> '' AND crs = btrim(crs)",
            name="scientific_artifact_crs_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "width > 0",
            name="scientific_artifact_width_positive",
        ),
        sa.CheckConstraint(
            "height > 0",
            name="scientific_artifact_height_positive",
        ),
        sa.CheckConstraint(
            "jsonb_typeof(transform) = 'array' "
            "AND jsonb_array_length(transform) = 6",
            name="scientific_artifact_transform_six_coefficients",
        ),
        sa.ForeignKeyConstraint(
            ["evaluation_id", "crop_id"],
            [
                "agroclimatic_evaluation.crop_outcomes.evaluation_id",
                "agroclimatic_evaluation.crop_outcomes.crop_id",
            ],
            name="fk_scientific_artifacts_crop_outcome",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "evaluation_id",
            "crop_id",
            "role",
            name="pk_scientific_artifacts",
        ),
        schema="agroclimatic_evaluation",
    )


def downgrade() -> None:
    op.drop_table(
        "scientific_artifacts",
        schema="agroclimatic_evaluation",
    )