"""Create Farm Management PostgreSQL/PostGIS persistence.

Revision ID: 20260912_0001
Revises: None
"""

from collections.abc import Sequence

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260912_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.execute("CREATE SCHEMA IF NOT EXISTS farm_management")

    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_projects"),
        schema="farm_management",
    )
    op.create_table(
        "parcels",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("current_version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "current_version >= 1", name="current_version_positive"
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["farm_management.projects.id"],
            name="fk_parcels_project_id_projects",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_parcels"),
        schema="farm_management",
    )
    op.create_index(
        "ix_parcels_project_id",
        "parcels",
        ["project_id"],
        unique=False,
        schema="farm_management",
    )
    op.create_table(
        "parcel_versions",
        sa.Column("parcel_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("geometry_type", sa.String(length=12), nullable=False),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(
                geometry_type="MULTIPOLYGON",
                srid=4326,
                dimension=2,
                spatial_index=False,
            ),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "number >= 1", name="number_positive"
        ),
        sa.CheckConstraint(
            "geometry_type IN ('Polygon', 'MultiPolygon')",
            name="geometry_type_supported",
        ),
        sa.ForeignKeyConstraint(
            ["parcel_id"],
            ["farm_management.parcels.id"],
            name="fk_parcel_versions_parcel_id_parcels",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "parcel_id", "number", name="pk_parcel_versions"
        ),
        schema="farm_management",
    )
    op.create_index(
        "ix_parcel_versions_geometry",
        "parcel_versions",
        ["geometry"],
        unique=False,
        schema="farm_management",
        postgresql_using="gist",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_parcel_versions_geometry",
        table_name="parcel_versions",
        schema="farm_management",
        postgresql_using="gist",
    )
    op.drop_table("parcel_versions", schema="farm_management")
    op.drop_index(
        "ix_parcels_project_id",
        table_name="parcels",
        schema="farm_management",
    )
    op.drop_table("parcels", schema="farm_management")
    op.drop_table("projects", schema="farm_management")
    op.execute("DROP SCHEMA IF EXISTS farm_management")
