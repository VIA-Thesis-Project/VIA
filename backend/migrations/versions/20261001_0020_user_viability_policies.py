"""Persist personal viability-policy selections.

Revision ID: 20261001_0020
Revises: 20260927_0019
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261001_0020"
down_revision: str | None = "20260927_0019"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "user_viability_policies",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("policy_identifier", sa.String(120), nullable=False),
        sa.Column("policy_version", sa.String(64), nullable=False),
        sa.Column(
            "selected_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["policy_identifier", "policy_version"],
            [
                "decision_support.viability_policy_versions.identifier",
                "decision_support.viability_policy_versions.version",
            ],
            name="fk_user_viability_policy_version",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("user_id", name="pk_user_viability_policies"),
        schema="decision_support",
    )


def downgrade() -> None:
    op.drop_table("user_viability_policies", schema="decision_support")
