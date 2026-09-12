"""Create Agroclimatic Evaluation PostgreSQL/PostGIS persistence.

Revision ID: 20260912_0003
Revises: 20260912_0002
"""

from collections.abc import Sequence

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260912_0003"
down_revision: str | None = "20260912_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS agroclimatic_evaluation")

    op.create_table(
        "evaluations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("parcel_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("parcel_version", sa.Integer(), nullable=False),
        sa.Column(
            "snapshot_geometry",
            geoalchemy2.types.Geometry(
                geometry_type="MULTIPOLYGON",
                srid=4326,
                dimension=2,
                spatial_index=False,
            ),
            nullable=False,
        ),
        sa.Column("snapshot_geometry_kind", sa.String(length=16), nullable=False),
        sa.Column("snapshot_crs", sa.String(length=32), nullable=False),
        sa.Column("snapshot_captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "parcel_version > 0", name="parcel_version_positive"
        ),
        sa.CheckConstraint(
            "snapshot_geometry_kind IN ('Polygon', 'MultiPolygon')",
            name="snapshot_geometry_kind_supported",
        ),
        sa.CheckConstraint(
            "snapshot_crs = 'EPSG:4326'", name="snapshot_crs_supported"
        ),
        sa.CheckConstraint(
            "status IN ('queued', 'preparing', 'running', 'summarizing', "
            "'succeeded', 'failed', 'cancelled')",
            name="evaluation_status_supported",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_evaluations"),
        schema="agroclimatic_evaluation",
    )
    op.create_index(
        "ix_evaluations_parcel_id",
        "evaluations",
        ["parcel_id"],
        unique=False,
        schema="agroclimatic_evaluation",
    )
    op.create_index(
        "ix_evaluations_snapshot_geometry",
        "evaluations",
        ["snapshot_geometry"],
        unique=False,
        schema="agroclimatic_evaluation",
        postgresql_using="gist",
    )
    op.create_table(
        "evaluation_crops",
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("crop_id", sa.String(length=120), nullable=False),
        sa.CheckConstraint("position >= 0", name="crop_position_nonnegative"),
        sa.CheckConstraint(
            "crop_id <> '' AND crop_id = btrim(crop_id)",
            name="crop_id_nonempty_trimmed",
        ),
        sa.ForeignKeyConstraint(
            ["evaluation_id"],
            ["agroclimatic_evaluation.evaluations.id"],
            name="fk_evaluation_crops_evaluation_id_evaluations",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "evaluation_id", "position", name="pk_evaluation_crops"
        ),
        sa.UniqueConstraint(
            "evaluation_id",
            "crop_id",
            name="uq_evaluation_crops_evaluation_crop",
        ),
        schema="agroclimatic_evaluation",
    )


def downgrade() -> None:
    op.drop_table("evaluation_crops", schema="agroclimatic_evaluation")
    op.drop_index(
        "ix_evaluations_snapshot_geometry",
        table_name="evaluations",
        schema="agroclimatic_evaluation",
        postgresql_using="gist",
    )
    op.drop_index(
        "ix_evaluations_parcel_id",
        table_name="evaluations",
        schema="agroclimatic_evaluation",
    )
    op.drop_table("evaluations", schema="agroclimatic_evaluation")
    op.execute("DROP SCHEMA IF EXISTS agroclimatic_evaluation")
