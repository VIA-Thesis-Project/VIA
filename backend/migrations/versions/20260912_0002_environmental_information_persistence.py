"""Create Environmental Information PostgreSQL/PostGIS persistence.

Revision ID: 20260912_0002
Revises: 20260912_0001
"""

from collections.abc import Sequence

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260912_0002"
down_revision: str | None = "20260912_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS environmental_information")

    op.create_table(
        "datasets",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("variable", sa.String(length=120), nullable=False),
        sa.Column("unit", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_datasets"),
        schema="environmental_information",
    )
    op.create_table(
        "dataset_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("version_identifier", sa.String(length=120), nullable=False),
        sa.Column("crs", sa.String(length=32), nullable=False),
        sa.Column("resolution_x", sa.Float(), nullable=False),
        sa.Column("resolution_y", sa.Float(), nullable=False),
        sa.Column("resolution_unit", sa.String(length=32), nullable=False),
        sa.Column(
            "extent",
            geoalchemy2.types.Geometry(
                geometry_type="POLYGON",
                srid=-1,
                dimension=2,
                spatial_index=False,
            ),
            nullable=False,
        ),
        sa.Column("valid_from", sa.Date(), nullable=True),
        sa.Column("valid_to", sa.Date(), nullable=True),
        sa.Column("scenario", sa.String(length=120), nullable=True),
        sa.Column("checksum", sa.String(length=256), nullable=False),
        sa.Column("storage_reference", sa.String(length=1024), nullable=False),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "resolution_x > 0", name="resolution_x_positive"
        ),
        sa.CheckConstraint(
            "resolution_y > 0", name="resolution_y_positive"
        ),
        sa.CheckConstraint(
            "valid_from IS NULL OR valid_to IS NULL OR valid_from <= valid_to",
            name="validity_period_ordered",
        ),
        sa.CheckConstraint(
            "crs = 'EPSG:' || ST_SRID(extent)::text",
            name="crs_matches_extent_srid",
        ),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["environmental_information.datasets.id"],
            name="fk_dataset_versions_dataset_id_datasets",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_dataset_versions"),
        sa.UniqueConstraint(
            "dataset_id",
            "version_identifier",
            name="uq_dataset_versions_dataset_version_identifier",
        ),
        schema="environmental_information",
    )
    op.create_index(
        "ix_dataset_versions_dataset_id",
        "dataset_versions",
        ["dataset_id"],
        unique=False,
        schema="environmental_information",
    )
    op.create_index(
        "ix_dataset_versions_extent",
        "dataset_versions",
        ["extent"],
        unique=False,
        schema="environmental_information",
        postgresql_using="gist",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_dataset_versions_extent",
        table_name="dataset_versions",
        schema="environmental_information",
        postgresql_using="gist",
    )
    op.drop_index(
        "ix_dataset_versions_dataset_id",
        table_name="dataset_versions",
        schema="environmental_information",
    )
    op.drop_table("dataset_versions", schema="environmental_information")
    op.drop_table("datasets", schema="environmental_information")
    op.execute("DROP SCHEMA IF EXISTS environmental_information")
