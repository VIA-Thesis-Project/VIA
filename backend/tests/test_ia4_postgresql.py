"""PostgreSQL evaluation and generation ledger tests."""

from __future__ import annotations

import os
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import func, select

from database_test_support import require_test_database_url
from test_ia4_quota import _evaluation
from via_backend.contexts.agroclimatic_evaluation.infrastructure.postgresql_repositories import (
    PostgreSQLEvaluationRepository,
)
from via_backend.contexts.decision_support.infrastructure.orm import (
    RecommendationGenerationAttemptRecord,
)
from via_backend.contexts.decision_support.infrastructure.postgresql_repositories import (
    PostgreSQLRecommendationRepository,
)
from via_backend.infrastructure import SessionFactory, create_database

pytestmark = pytest.mark.integration
NOW = datetime(2026, 9, 21, 12, tzinfo=UTC)


@pytest.fixture(scope="module")
def sessions() -> Iterator[SessionFactory]:
    url = require_test_database_url()
    previous = os.environ.get("VIA_DATABASE_URL")
    os.environ["VIA_DATABASE_URL"] = url
    try:
        command.upgrade(Config(str(Path(__file__).parents[1] / "alembic.ini")), "head")
    finally:
        if previous is None:
            os.environ.pop("VIA_DATABASE_URL", None)
        else:
            os.environ["VIA_DATABASE_URL"] = previous
    engine, factory = create_database(url)
    yield factory
    engine.dispose()


def test_multiple_active_evaluations_are_owner_scoped(sessions: SessionFactory) -> None:
    owner, other = uuid4(), uuid4()
    repo = PostgreSQLEvaluationRepository(sessions)
    created = [_evaluation(owner, NOW) for _ in range(4)]
    for evaluation in created:
        repo.add(evaluation)
    repo.add(_evaluation(other, NOW))
    repo.add(_evaluation(owner, NOW + timedelta(days=1)))
    assert {item.id for item in repo.list_for_owner(owner)} >= {item.id for item in created}
    assert len(repo.list_for_owner(other)) == 1


def test_simultaneous_evaluation_posts_are_both_admitted(sessions: SessionFactory) -> None:
    owner = uuid4()
    repo = PostgreSQLEvaluationRepository(sessions)
    repo.add(_evaluation(owner, NOW))

    def attempt(_: int) -> bool:
        repo.add(_evaluation(owner, NOW))
        return True

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert list(pool.map(attempt, range(2))) == [True, True]
    assert len(repo.list_for_owner(owner)) == 3


def test_recommendation_ledger_records_multiple_attempts_per_owner(
    sessions: SessionFactory,
) -> None:
    owner, other = uuid4(), uuid4()
    repo = PostgreSQLRecommendationRepository(sessions)
    repo.record_generation_attempt(owner, uuid4(), NOW)
    repo.record_generation_attempt(other, uuid4(), NOW)
    repo.record_generation_attempt(owner, uuid4(), NOW)
    repo.record_generation_attempt(owner, uuid4(), NOW + timedelta(days=1))

    concurrent_owner = uuid4()

    def attempt(_: int) -> bool:
        repo.record_generation_attempt(concurrent_owner, uuid4(), NOW)
        return True

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert list(pool.map(attempt, range(2))) == [True, True]
    with sessions() as session:
        assert session.scalar(
            select(func.count()).select_from(RecommendationGenerationAttemptRecord).where(
                RecommendationGenerationAttemptRecord.owner_user_id == owner,
            )
        ) == 3
        assert session.scalar(
            select(func.count()).select_from(RecommendationGenerationAttemptRecord).where(
                RecommendationGenerationAttemptRecord.owner_user_id == concurrent_owner,
            )
        ) == 2
