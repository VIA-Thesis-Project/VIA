"""PostgreSQL repositories for Decision Support."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert as postgresql_insert

from via_backend.infrastructure.database import SessionFactory

from ..application.errors import (
    DefaultViabilityPolicyConflictError,
    DefaultViabilityPolicyNotConfiguredError,
    ViabilityPolicyVersionNotFoundError,
)
from ..domain.errors import PolicyVersionConflictError
from ..domain.models import (
    PolicyReference,
    ViabilityPolicyConfiguration,
    ViabilityPolicySnapshot,
)
from .orm import (
    DefaultViabilityPolicyRecord,
    ViabilityPolicyVersionRecord,
)


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

        with self._sessions.begin() as session:
            statement = (
                postgresql_insert(ViabilityPolicyVersionRecord)
                .values(
                    identifier=reference.identifier,
                    version=reference.version,
                    conditional_from=policy.configuration.conditional_from,
                    viable_from=policy.configuration.viable_from,
                )
                .on_conflict_do_nothing(
                    index_elements=[
                        ViabilityPolicyVersionRecord.identifier,
                        ViabilityPolicyVersionRecord.version,
                    ]
                )
                .returning(ViabilityPolicyVersionRecord.identifier)
            )
            inserted_identifier = session.execute(statement).scalar_one_or_none()

            if inserted_identifier is not None:
                return

            existing = session.get(
                ViabilityPolicyVersionRecord,
                identity,
            )
            if existing is None:
                raise RuntimeError(
                    "Policy registration conflicted, but the persisted policy "
                    f"{reference.identifier}:{reference.version} could not be restored."
                )

            if _snapshot_from_record(existing) != policy:
                raise PolicyVersionConflictError(
                    "Policy reference "
                    f"{reference.identifier}:{reference.version} "
                    "already exists with different thresholds."
                )

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


_DEFAULT_POLICY_SLOT = "default"


class PostgreSQLDefaultViabilityPolicyStore:
    """Persist and resolve the singleton VIA default-policy pointer."""

    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def get_default_viability_policy(
        self,
    ) -> ViabilityPolicySnapshot:
        with self._sessions() as session:
            pointer = session.get(
                DefaultViabilityPolicyRecord,
                _DEFAULT_POLICY_SLOT,
            )

            if pointer is None:
                raise DefaultViabilityPolicyNotConfiguredError(
                    "No default viability policy is configured."
                )

            policy_record = session.get(
                ViabilityPolicyVersionRecord,
                (
                    pointer.policy_identifier,
                    pointer.policy_version,
                ),
            )

            if policy_record is None:
                raise RuntimeError(
                    "Default viability-policy pointer references "
                    "missing persisted policy data."
                )

            return _snapshot_from_record(policy_record)

    def set_default_viability_policy(
        self,
        reference: PolicyReference,
        *,
        expected_current: PolicyReference | None,
    ) -> None:
        identity = (
            reference.identifier,
            reference.version,
        )

        with self._sessions.begin() as session:
            policy_record = session.get(
                ViabilityPolicyVersionRecord,
                identity,
            )

            if policy_record is None:
                raise ViabilityPolicyVersionNotFoundError(
                    "Cannot select missing viability policy "
                    f"{reference.identifier}:{reference.version}."
                )

            if expected_current is None:
                statement = (
                    postgresql_insert(DefaultViabilityPolicyRecord)
                    .values(
                        slot=_DEFAULT_POLICY_SLOT,
                        policy_identifier=reference.identifier,
                        policy_version=reference.version,
                    )
                    .on_conflict_do_nothing(
                        index_elements=[DefaultViabilityPolicyRecord.slot]
                    )
                    .returning(DefaultViabilityPolicyRecord.slot)
                )
            else:
                statement = (
                    update(DefaultViabilityPolicyRecord)
                    .where(
                        DefaultViabilityPolicyRecord.slot == _DEFAULT_POLICY_SLOT,
                        DefaultViabilityPolicyRecord.policy_identifier
                        == expected_current.identifier,
                        DefaultViabilityPolicyRecord.policy_version
                        == expected_current.version,
                    )
                    .values(
                        policy_identifier=reference.identifier,
                        policy_version=reference.version,
                        selected_at=datetime.now(UTC),
                    )
                    .returning(DefaultViabilityPolicyRecord.slot)
                )

            changed_slot = session.execute(statement).scalar_one_or_none()
            if changed_slot is not None:
                return

            pointer = session.get(
                DefaultViabilityPolicyRecord,
                _DEFAULT_POLICY_SLOT,
            )
            if pointer is not None and (
                pointer.policy_identifier == reference.identifier
                and pointer.policy_version == reference.version
            ):
                return

            raise DefaultViabilityPolicyConflictError(
                "Default viability-policy pointer changed before the expected update."
            )
