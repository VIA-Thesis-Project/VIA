"""Persist the current default Decision Support viability-policy pointer.

Revision ID: 20260916_0010
Revises: 20260915_0009
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260916_0010"
down_revision: str | None = "20260915_0009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "default_viability_policy",
        sa.Column(
            "slot",
            sa.String(length=32),
            nullable=False,
        ),
        sa.Column(
            "policy_identifier",
            sa.String(length=120),
            nullable=False,
        ),
        sa.Column(
            "policy_version",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "selected_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "slot = 'default'",
            name="default_policy_singleton_slot",
        ),
        sa.ForeignKeyConstraint(
            ["policy_identifier", "policy_version"],
            [
                "decision_support.viability_policy_versions.identifier",
                "decision_support.viability_policy_versions.version",
            ],
            name="fk_default_policy_version",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "slot",
            name="pk_default_viability_policy",
        ),
        schema="decision_support",
    )


def downgrade() -> None:
    op.drop_table(
        "default_viability_policy",
        schema="decision_support",
    )