"""Add parcel description and soft deletion.

Revision ID: 20260927_0019
Revises: 20260927_0018
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260927_0019"
down_revision: str | None = "20260927_0018"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "parcels", sa.Column("description", sa.Text(), nullable=True), schema="farm_management"
    )
    op.add_column(
        "parcels",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        schema="farm_management",
    )


def downgrade() -> None:
    op.drop_column("parcels", "deleted_at", schema="farm_management")
    op.drop_column("parcels", "description", schema="farm_management")
