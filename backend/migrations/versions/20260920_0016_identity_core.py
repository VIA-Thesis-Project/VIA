"""Add IA-1 Identity Core and nullable ownership metadata.

Revision ID: 20260920_0016
Revises: 20260918_0015
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260920_0016"
down_revision: str | None = "20260918_0015"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

IDENTITY_SCHEMA = "identity_access"


def upgrade() -> None:
    op.execute(sa.text(f"CREATE SCHEMA IF NOT EXISTS {IDENTITY_SCHEMA}"))

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "email <> '' AND email = btrim(email) AND email = lower(email)",
            name="email_canonical",
        ),
        sa.CheckConstraint("status IN ('active', 'disabled')", name="status_supported"),
        sa.CheckConstraint("role IN ('user', 'admin')", name="role_supported"),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        schema=IDENTITY_SCHEMA,
    )

    op.create_table(
        "auth_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("family_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("access_token_hash", sa.String(length=64), nullable=False),
        sa.Column("access_expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("refresh_token_hash", sa.String(length=64), nullable=False),
        sa.Column("refresh_expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("replaced_by_session_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("revocation_reason", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "access_token_hash ~ '^[0-9a-f]{64}$'",
            name="access_token_hash_sha256",
        ),
        sa.CheckConstraint(
            "refresh_token_hash ~ '^[0-9a-f]{64}$'",
            name="refresh_token_hash_sha256",
        ),
        sa.CheckConstraint(
            "revocation_reason IS NULL OR btrim(revocation_reason) <> ''",
            name="revocation_reason_nonempty",
        ),
        sa.CheckConstraint(
            "revocation_reason IS NULL OR revoked_at IS NOT NULL",
            name="revocation_reason_requires_revocation",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            [f"{IDENTITY_SCHEMA}.users.id"],
            name="fk_auth_sessions_user_id_users",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["replaced_by_session_id"],
            [f"{IDENTITY_SCHEMA}.auth_sessions.id"],
            name="fk_auth_sessions_replaced_by_session_id_auth_sessions",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_auth_sessions"),
        sa.UniqueConstraint(
            "access_token_hash", name="uq_auth_sessions_access_token_hash"
        ),
        sa.UniqueConstraint(
            "refresh_token_hash", name="uq_auth_sessions_refresh_token_hash"
        ),
        schema=IDENTITY_SCHEMA,
    )
    op.create_index(
        "ix_auth_sessions_user_refresh_expires_at",
        "auth_sessions",
        ["user_id", "refresh_expires_at"],
        unique=False,
        schema=IDENTITY_SCHEMA,
    )
    op.create_index(
        "ix_auth_sessions_family_id",
        "auth_sessions",
        ["family_id"],
        unique=False,
        schema=IDENTITY_SCHEMA,
    )

    op.add_column(
        "projects",
        sa.Column("owner_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        schema="farm_management",
    )
    op.create_index(
        "ix_projects_owner_user_id",
        "projects",
        ["owner_user_id"],
        unique=False,
        schema="farm_management",
    )

    op.add_column(
        "evaluations",
        sa.Column("owner_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        schema="agroclimatic_evaluation",
    )
    op.create_index(
        "ix_evaluations_owner_user_id",
        "evaluations",
        ["owner_user_id"],
        unique=False,
        schema="agroclimatic_evaluation",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_evaluations_owner_user_id",
        table_name="evaluations",
        schema="agroclimatic_evaluation",
    )
    op.drop_column("evaluations", "owner_user_id", schema="agroclimatic_evaluation")

    op.drop_index(
        "ix_projects_owner_user_id",
        table_name="projects",
        schema="farm_management",
    )
    op.drop_column("projects", "owner_user_id", schema="farm_management")

    op.drop_index(
        "ix_auth_sessions_family_id",
        table_name="auth_sessions",
        schema=IDENTITY_SCHEMA,
    )
    op.drop_index(
        "ix_auth_sessions_user_refresh_expires_at",
        table_name="auth_sessions",
        schema=IDENTITY_SCHEMA,
    )
    op.drop_table("auth_sessions", schema=IDENTITY_SCHEMA)
    op.drop_table("users", schema=IDENTITY_SCHEMA)
    op.execute(sa.text(f"DROP SCHEMA IF EXISTS {IDENTITY_SCHEMA}"))
