"""Persist immutable Decision Support viability-policy versions.

Revision ID: 20260915_0009
Revises: 20260914_0008
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260915_0009"
down_revision: str | None = "20260914_0008"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        sa.text(
            "CREATE SCHEMA IF NOT EXISTS decision_support"
        )
    )

    op.create_table(
        "viability_policy_versions",
        sa.Column(
            "identifier",
            sa.String(length=120),
            nullable=False,
        ),
        sa.Column(
            "version",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "conditional_from",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "viable_from",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "identifier <> '' AND identifier = btrim(identifier)",
            name="policy_identifier_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "version <> '' AND version = btrim(version)",
            name="policy_version_nonempty_trimmed",
        ),
        sa.CheckConstraint(
            "conditional_from >= 0 AND conditional_from <= 100",
            name="policy_conditional_threshold_valid",
        ),
        sa.CheckConstraint(
            "viable_from >= 0 AND viable_from <= 100",
            name="policy_viable_threshold_valid",
        ),
        sa.CheckConstraint(
            "conditional_from < viable_from",
            name="policy_threshold_order_valid",
        ),
        sa.PrimaryKeyConstraint(
            "identifier",
            "version",
            name="pk_viability_policy_versions",
        ),
        schema="decision_support",
    )


def downgrade() -> None:
    op.drop_table(
        "viability_policy_versions",
        schema="decision_support",
    )

    op.execute(
        sa.text(
            "DROP SCHEMA IF EXISTS decision_support"
        )
    )