"""Bind new evaluations to immutable viability policy versions.

Revision ID: 20260927_0018
Revises: 20260921_0017
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260927_0018"
down_revision: str | None = "20260921_0017"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "evaluation_viability_policy_bindings",
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), primary_key=True),
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
            name="fk_evaluation_viability_policy_binding_version",
            ondelete="RESTRICT",
        ),
        schema="decision_support",
    )
    op.create_index(
        "ix_evaluation_viability_policy_bindings_policy",
        "evaluation_viability_policy_bindings",
        ["policy_identifier", "policy_version"],
        schema="decision_support",
    )
    op.execute(
        """INSERT INTO decision_support.viability_policy_versions
        (identifier, version, conditional_from, viable_from)
        VALUES ('via-policy', '1', 40.0, 70.0)
        ON CONFLICT (identifier, version) DO NOTHING"""
    )
    op.execute(
        """DO $$ BEGIN
        IF EXISTS (
            SELECT 1 FROM decision_support.viability_policy_versions
            WHERE identifier = 'via-policy' AND version = '1'
              AND (conditional_from <> 40.0 OR viable_from <> 70.0)
        ) THEN
            RAISE EXCEPTION 'via-policy:1 conflicts with the required initial baseline';
        END IF;
        END $$"""
    )
    op.execute(
        """INSERT INTO decision_support.default_viability_policy
        (slot, policy_identifier, policy_version)
        VALUES ('default', 'via-policy', '1')
        ON CONFLICT (slot) DO NOTHING"""
    )


def downgrade() -> None:
    op.drop_index(
        "ix_evaluation_viability_policy_bindings_policy",
        table_name="evaluation_viability_policy_bindings",
        schema="decision_support",
    )
    op.drop_table("evaluation_viability_policy_bindings", schema="decision_support")
