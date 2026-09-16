"""PostgreSQL integration tests for Decision Support policy persistence."""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, text

from database_test_support import require_test_database_url
from via_backend.contexts.decision_support.application.errors import (
    DefaultViabilityPolicyNotConfiguredError,
    ViabilityPolicyVersionNotFoundError,
)
from via_backend.contexts.decision_support.application.policy_lifecycle import (
    RegisterViabilityPolicyVersion,
    ReviseViabilityPolicyVersion,
    ViabilityPolicyLifecycleService,
)
from via_backend.contexts.decision_support.domain import (
    PolicyReference,
    PolicyVersionConflictError,
    ViabilityPolicyConfiguration,
    ViabilityPolicySnapshot,
)
from via_backend.contexts.decision_support.infrastructure import (
    PostgreSQLDefaultViabilityPolicyStore,
    PostgreSQLViabilityPolicyRepository,
)
from via_backend.infrastructure import SessionFactory, create_database

pytestmark = pytest.mark.integration
BACKEND_ROOT = Path(__file__).parents[1]


def _database_url() -> str:
    return require_test_database_url()


@pytest.fixture(scope="session")
def database() -> Iterator[tuple[Engine, SessionFactory]]:
    database_url = _database_url()

    previous = os.environ.get("VIA_DATABASE_URL")
    os.environ["VIA_DATABASE_URL"] = database_url

    try:
        command.upgrade(
            Config(str(BACKEND_ROOT / "alembic.ini")),
            "head",
        )
    finally:
        if previous is None:
            os.environ.pop("VIA_DATABASE_URL", None)
        else:
            os.environ["VIA_DATABASE_URL"] = previous

    engine, sessions = create_database(database_url)

    yield engine, sessions

    engine.dispose()


@pytest.fixture(autouse=True)
def clean_policy_versions(
    database: tuple[Engine, SessionFactory],
) -> None:
    engine, _ = database

    with engine.begin() as connection:
        connection.execute(
            text(
                "TRUNCATE TABLE "
                "decision_support.default_viability_policy, "
                "decision_support.viability_policy_versions"
            )
        )


def _snapshot(
    *,
    identifier: str = "via-policy",
    version: str = "1",
    conditional_from: float = 40.0,
    viable_from: float = 70.0,
) -> ViabilityPolicySnapshot:
    return ViabilityPolicySnapshot(
        reference=PolicyReference(
            identifier=identifier,
            version=version,
        ),
        configuration=ViabilityPolicyConfiguration(
            conditional_from=conditional_from,
            viable_from=viable_from,
        ),
    )


def test_policy_version_round_trips(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database

    repository = PostgreSQLViabilityPolicyRepository(sessions)
    policy = _snapshot()

    repository.add(policy)

    restored = repository.get(policy.reference)

    assert restored == policy


def test_same_immutable_policy_can_be_added_idempotently(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database

    repository = PostgreSQLViabilityPolicyRepository(sessions)
    policy = _snapshot()

    repository.add(policy)
    repository.add(policy)

    assert repository.get(policy.reference) == policy


def test_same_reference_cannot_change_thresholds(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database

    repository = PostgreSQLViabilityPolicyRepository(sessions)

    original = _snapshot(
        conditional_from=40.0,
        viable_from=70.0,
    )
    conflicting = _snapshot(
        conditional_from=45.0,
        viable_from=75.0,
    )

    repository.add(original)

    with pytest.raises(
        PolicyVersionConflictError,
        match="different thresholds",
    ):
        repository.add(conflicting)

    assert repository.get(original.reference) == original


def test_multiple_versions_of_same_policy_are_preserved(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database

    repository = PostgreSQLViabilityPolicyRepository(sessions)

    first = _snapshot(
        version="1",
        conditional_from=40.0,
        viable_from=70.0,
    )
    second = _snapshot(
        version="2",
        conditional_from=45.0,
        viable_from=75.0,
    )

    repository.add(first)
    repository.add(second)

    assert repository.get(first.reference) == first
    assert repository.get(second.reference) == second


def test_policy_revision_preserves_source_and_revised_versions(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database

    repository = PostgreSQLViabilityPolicyRepository(sessions)
    lifecycle = ViabilityPolicyLifecycleService(repository)
    source = lifecycle.register(
        RegisterViabilityPolicyVersion(
            reference=PolicyReference(identifier="via-policy", version="1"),
            configuration=ViabilityPolicyConfiguration(
                conditional_from=32.0,
                viable_from=62.0,
            ),
        )
    )

    revised = lifecycle.revise(
        ReviseViabilityPolicyVersion(
            source=source.reference,
            new_version="2",
            configuration=ViabilityPolicyConfiguration(
                conditional_from=47.0,
                viable_from=77.0,
            ),
        )
    )

    assert repository.get(source.reference) == source
    assert repository.get(revised.reference) == revised
    assert source.reference.version == "1"
    assert revised.reference.version == "2"


def test_missing_policy_version_returns_none(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database

    repository = PostgreSQLViabilityPolicyRepository(sessions)

    assert (
        repository.get(
            PolicyReference(
                identifier="missing-policy",
                version="1",
            )
        )
        is None
    )

def test_default_provider_requires_configured_policy(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database

    store = PostgreSQLDefaultViabilityPolicyStore(sessions)

    with pytest.raises(
        DefaultViabilityPolicyNotConfiguredError,
        match="No default viability policy",
    ):
        store.get_default_viability_policy()


def test_default_policy_round_trips_exact_snapshot(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database

    repository = PostgreSQLViabilityPolicyRepository(sessions)
    store = PostgreSQLDefaultViabilityPolicyStore(sessions)
    policy = _snapshot()

    repository.add(policy)
    store.set_default_viability_policy(policy.reference)

    assert store.get_default_viability_policy() == policy


def test_default_pointer_rejects_missing_policy_version(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database

    store = PostgreSQLDefaultViabilityPolicyStore(sessions)

    with pytest.raises(
        ViabilityPolicyVersionNotFoundError,
        match="Cannot select missing viability policy",
    ):
        store.set_default_viability_policy(
            PolicyReference(
                identifier="missing-policy",
                version="1",
            )
        )


def test_setting_same_default_is_idempotent(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database

    repository = PostgreSQLViabilityPolicyRepository(sessions)
    store = PostgreSQLDefaultViabilityPolicyStore(sessions)
    policy = _snapshot()

    repository.add(policy)

    store.set_default_viability_policy(policy.reference)
    store.set_default_viability_policy(policy.reference)

    assert store.get_default_viability_policy() == policy


def test_switching_default_preserves_historical_policy_versions(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database

    repository = PostgreSQLViabilityPolicyRepository(sessions)
    store = PostgreSQLDefaultViabilityPolicyStore(sessions)

    first = _snapshot(
        version="1",
        conditional_from=40.0,
        viable_from=70.0,
    )
    second = _snapshot(
        version="2",
        conditional_from=45.0,
        viable_from=75.0,
    )

    repository.add(first)
    repository.add(second)

    store.set_default_viability_policy(first.reference)
    assert store.get_default_viability_policy() == first

    store.set_default_viability_policy(second.reference)

    assert store.get_default_viability_policy() == second
    assert repository.get(first.reference) == first
    assert repository.get(second.reference) == second