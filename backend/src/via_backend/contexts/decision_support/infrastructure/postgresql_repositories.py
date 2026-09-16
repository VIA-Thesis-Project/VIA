"""PostgreSQL repositories for Decision Support."""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError

from via_backend.infrastructure.database import SessionFactory

from ..domain.errors import PolicyVersionConflictError
from ..domain.models import (
    PolicyReference,
    ViabilityPolicyConfiguration,
    ViabilityPolicySnapshot,
)
from .orm import ViabilityPolicyVersionRecord


class PostgreSQLViabilityPolicyRepository:
    """Durable adapter for immutable viability-policy versions."""

    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def add(self, policy: ViabilityPolicySnapshot) -> None:
        reference = policy.reference
        identity = (
            reference.identifier,
            reference.version,
        )

        try:
            with self._sessions.begin() as session:
                existing = session.get(
                    ViabilityPolicyVersionRecord,
                    identity,
                )

                if existing is None:
                    session.add(_record_from_snapshot(policy))
                    return

                if _snapshot_from_record(existing) != policy:
                    raise PolicyVersionConflictError(
                        "Policy reference "
                        f"{reference.identifier}:{reference.version} "
                        "already exists with different thresholds."
                    )
        except IntegrityError as error:
            raise PolicyVersionConflictError(
                "Policy reference "
                f"{reference.identifier}:{reference.version} "
                "conflicts with persisted policy data."
            ) from error

    def get(
        self,
        reference: PolicyReference,
    ) -> ViabilityPolicySnapshot | None:
        with self._sessions() as session:
            record = session.get(
                ViabilityPolicyVersionRecord,
                (
                    reference.identifier,
                    reference.version,
                ),
            )

            if record is None:
                return None

            return _snapshot_from_record(record)


def _record_from_snapshot(
    policy: ViabilityPolicySnapshot,
) -> ViabilityPolicyVersionRecord:
    return ViabilityPolicyVersionRecord(
        identifier=policy.reference.identifier,
        version=policy.reference.version,
        conditional_from=policy.configuration.conditional_from,
        viable_from=policy.configuration.viable_from,
    )


def _snapshot_from_record(
    record: ViabilityPolicyVersionRecord,
) -> ViabilityPolicySnapshot:
    return ViabilityPolicySnapshot(
        reference=PolicyReference(
            identifier=record.identifier,
            version=record.version,
        ),
        configuration=ViabilityPolicyConfiguration(
            conditional_from=record.conditional_from,
            viable_from=record.viable_from,
        ),
    )