"""Database records for Decision Support; these are not domain entities."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    ForeignKeyConstraint,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class ViabilityPolicyVersionRecord(Base):
    """One immutable persisted viability-policy configuration."""

    __tablename__ = "viability_policy_versions"
    __table_args__ = (
        CheckConstraint(
            "identifier <> '' AND identifier = btrim(identifier)",
            name="policy_identifier_nonempty_trimmed",
        ),
        CheckConstraint(
            "version <> '' AND version = btrim(version)",
            name="policy_version_nonempty_trimmed",
        ),
        CheckConstraint(
            "conditional_from >= 0 AND conditional_from <= 100",
            name="policy_conditional_threshold_valid",
        ),
        CheckConstraint(
            "viable_from >= 0 AND viable_from <= 100",
            name="policy_viable_threshold_valid",
        ),
        CheckConstraint(
            "conditional_from < viable_from",
            name="policy_threshold_order_valid",
        ),
    )

    identifier: Mapped[str] = mapped_column(
        String(120),
        primary_key=True,
        nullable=False,
    )
    version: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        nullable=False,
    )
    conditional_from: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    viable_from: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

class DefaultViabilityPolicyRecord(Base):
    """Singleton pointer to the currently selected VIA default policy version."""

    __tablename__ = "default_viability_policy"
    __table_args__ = (
        CheckConstraint(
            "slot = 'default'",
            name="default_policy_singleton_slot",
        ),
        ForeignKeyConstraint(
            ["policy_identifier", "policy_version"],
            [
                "decision_support.viability_policy_versions.identifier",
                "decision_support.viability_policy_versions.version",
            ],
            name="fk_default_policy_version",
            ondelete="RESTRICT",
        ),
    )

    slot: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
        nullable=False,
    )
    policy_identifier: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )
    policy_version: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    selected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )