"""IA-4 quota boundaries and recommendation cache accounting."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest

from test_agronomic_knowledge import (
    _context,
    _Generator,
    _recommendation,
    _RecommendationRepository,
    _retrieved,
    _Retriever,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    Evaluation,
    EvaluationStatus,
    ParcelSnapshot,
    SnapshotGeometry,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import InMemoryEvaluationRepository
from via_backend.contexts.decision_support.application.knowledge_services import (
    RecommendationApplicationService,
)
from via_backend.cost_protection import QuotaExceededError

NOW = datetime(2026, 9, 21, 12, tzinfo=UTC)


def _evaluation(
    owner: UUID, when: datetime, status: EvaluationStatus = EvaluationStatus.QUEUED
) -> Evaluation:
    return Evaluation(
        id=uuid4(),
        owner_user_id=owner,
        parcel_snapshot=ParcelSnapshot(
            project_id=uuid4(),
            parcel_id=uuid4(),
            parcel_version=1,
            geometry=SnapshotGeometry.from_geojson(
                {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-77.6, -11.1],
                            [-77.5, -11.1],
                            [-77.5, -11.0],
                            [-77.6, -11.1],
                        ]
                    ],
                }
            ),
            crs="EPSG:4326",
            captured_at=when,
        ),
        requested_crops=("maize",),
        status=status,
        created_at=when,
    )


def test_evaluation_active_and_utc_daily_quota() -> None:
    owner, other = uuid4(), uuid4()
    repo = InMemoryEvaluationRepository()
    repo.add(_evaluation(owner, NOW), max_active=2, daily_limit=2)
    repo.add(_evaluation(other, NOW), max_active=2, daily_limit=2)
    repo.add(_evaluation(owner, NOW), max_active=2, daily_limit=2)
    with pytest.raises(QuotaExceededError):
        repo.add(_evaluation(owner, NOW), max_active=2, daily_limit=2)
    for item in repo.list_for_owner(owner):
        repo.save(replace(item, status=EvaluationStatus.CANCELLED), expected_status=item.status)
    with pytest.raises(QuotaExceededError):
        repo.add(_evaluation(owner, NOW), max_active=2, daily_limit=2)
    repo.add(_evaluation(owner, NOW + timedelta(days=1)), max_active=2, daily_limit=2)


class _QuotaRepository(_RecommendationRepository):
    def __init__(self) -> None:
        super().__init__()
        self.attempts: list[tuple[UUID, datetime]] = []

    def reserve_generation(
        self,
        owner_user_id: UUID,
        evaluation_id: UUID,
        created_at: datetime,
        daily_limit: int,
    ) -> None:
        del evaluation_id
        start = created_at.astimezone(UTC).date()
        if (
            sum(
                user == owner_user_id and when.astimezone(UTC).date() == start
                for user, when in self.attempts
            )
            >= daily_limit
        ):
            raise QuotaExceededError(60)
        self.attempts.append((owner_user_id, created_at))


def test_recommendation_cache_does_not_consume_generation_quota() -> None:
    context = _context()
    repo = _QuotaRepository()
    generator = _Generator(_recommendation())
    owner = uuid4()
    service = RecommendationApplicationService(
        retriever=_Retriever(_retrieved(context)),
        generator=generator,
        repository=repo,
        daily_quota=1,
    )
    first = service.generate(context, owner_user_id=owner)
    second = service.generate(context, owner_user_id=owner)
    assert second.run_id == first.run_id
    assert len(repo.attempts) == 1 and generator.calls == 1
    with pytest.raises(QuotaExceededError):
        service.generate(context, force_regenerate=True, owner_user_id=owner)
    assert generator.calls == 1
