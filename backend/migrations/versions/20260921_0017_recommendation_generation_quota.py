"""Add durable, owner-scoped recommendation generation attempts.

Revision ID: 20260921_0017
Revises: 20260920_0016
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260921_0017"
down_revision: str | None = "20260920_0016"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "decision_support"


def upgrade() -> None:
    op.create_table(
        "recommendation_generation_attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("owner_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        schema=SCHEMA,
    )
    op.create_index(
        "ix_recommendation_attempts_owner_created",
        "recommendation_generation_attempts",
        ["owner_user_id", "created_at"],
        schema=SCHEMA,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_recommendation_attempts_owner_created",
        table_name="recommendation_generation_attempts",
        schema=SCHEMA,
    )
    op.drop_table("recommendation_generation_attempts", schema=SCHEMA)
