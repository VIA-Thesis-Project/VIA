"""PostgreSQL quota transactions; skipped when VIA_TEST_DATABASE_URL is absent."""

from __future__ import annotations

import os
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config

from database_test_support import require_test_database_url
from test_ia4_quota import _evaluation
from via_backend.contexts.agroclimatic_evaluation.domain import EvaluationStatus
from via_backend.contexts.agroclimatic_evaluation.infrastructure.postgresql_repositories import (
    PostgreSQLEvaluationRepository,
)
from via_backend.contexts.decision_support.infrastructure.postgresql_repositories import (
    PostgreSQLRecommendationRepository,
)
from via_backend.cost_protection import QuotaExceededError
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


def test_evaluation_quota_is_owner_scoped_and_atomic(sessions: SessionFactory) -> None:
    owner, other = uuid4(), uuid4()
    repo = PostgreSQLEvaluationRepository(sessions)
    first = _evaluation(owner, NOW)
    repo.add(first, max_active=2, daily_limit=2)
    repo.add(_evaluation(other, NOW), max_active=2, daily_limit=2)
    repo.add(_evaluation(owner, NOW), max_active=2, daily_limit=2)
    with pytest.raises(QuotaExceededError):
        repo.add(_evaluation(owner, NOW), max_active=2, daily_limit=2)
    for item in repo.list_for_owner(owner):
        repo.save(replace(item, status=EvaluationStatus.CANCELLED), expected_status=item.status)
    with pytest.raises(QuotaExceededError):
        repo.add(_evaluation(owner, NOW), max_active=2, daily_limit=2)
    repo.add(_evaluation(owner, NOW + timedelta(days=1)), max_active=2, daily_limit=2)


def test_simultaneous_evaluation_posts_admit_only_one(sessions: SessionFactory) -> None:
    owner = uuid4()
    repo = PostgreSQLEvaluationRepository(sessions)
    repo.add(_evaluation(owner, NOW), max_active=2, daily_limit=20)

    def attempt(_: int) -> bool:
        try:
            repo.add(_evaluation(owner, NOW), max_active=2, daily_limit=20)
        except QuotaExceededError:
            return False
        return True

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(attempt, range(2))) == [False, True]


def test_recommendation_ledger_is_owner_scoped_durable_and_atomic(
    sessions: SessionFactory,
) -> None:
    owner, other = uuid4(), uuid4()
    repo = PostgreSQLRecommendationRepository(sessions)
    repo.reserve_generation(owner, uuid4(), NOW, 1)
    repo.reserve_generation(other, uuid4(), NOW, 1)
    with pytest.raises(QuotaExceededError):
        repo.reserve_generation(owner, uuid4(), NOW, 1)
    repo.reserve_generation(owner, uuid4(), NOW + timedelta(days=1), 1)

    concurrent_owner = uuid4()

    def attempt(_: int) -> bool:
        try:
            repo.reserve_generation(concurrent_owner, uuid4(), NOW, 1)
        except QuotaExceededError:
            return False
        return True

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(attempt, range(2))) == [False, True]
