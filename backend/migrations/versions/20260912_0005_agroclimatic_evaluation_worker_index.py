"""Index queued evaluation discovery for the PostgreSQL polling worker.

Revision ID: 20260912_0005
Revises: 20260912_0004
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260912_0005"
down_revision: str | None = "20260912_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index(
        "ix_evaluations_status_created_at_id",
        "evaluations",
        ["status", "created_at", "id"],
        unique=False,
        schema="agroclimatic_evaluation",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_evaluations_status_created_at_id",
        table_name="evaluations",
        schema="agroclimatic_evaluation",
    )
