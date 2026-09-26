"""Unrestricted evaluation creation and recommendation attempt accounting."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

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


def test_multiple_active_evaluations_for_same_owner_are_admitted() -> None:
    owner, other = uuid4(), uuid4()
    repo = InMemoryEvaluationRepository()
    created = [_evaluation(owner, NOW) for _ in range(4)]
    for evaluation in created:
        repo.add(evaluation)
    repo.add(_evaluation(other, NOW))
    repo.add(_evaluation(owner, NOW + timedelta(days=1)))
    assert {item.id for item in repo.list_for_owner(owner)} >= {item.id for item in created}
    assert all(item.status is EvaluationStatus.QUEUED for item in created)
    assert len(repo.list_for_owner(other)) == 1


class _AttemptRepository(_RecommendationRepository):
    def __init__(self) -> None:
        super().__init__()
        self.attempts: list[tuple[UUID, datetime]] = []

    def record_generation_attempt(
        self,
        owner_user_id: UUID,
        evaluation_id: UUID,
        created_at: datetime,
    ) -> None:
        del evaluation_id
        self.attempts.append((owner_user_id, created_at))


def test_multiple_generations_for_same_owner_are_recorded_and_cache_is_reused() -> None:
    context = _context()
    repo = _AttemptRepository()
    generator = _Generator(_recommendation())
    owner = uuid4()
    service = RecommendationApplicationService(
        retriever=_Retriever(_retrieved(context)),
        generator=generator,
        repository=repo,
    )
    first = service.generate(context, owner_user_id=owner)
    second = service.generate(context, owner_user_id=owner)
    assert second.run_id == first.run_id
    assert len(repo.attempts) == 1 and generator.calls == 1
    for _ in range(3):
        service.generate(context, force_regenerate=True, owner_user_id=owner)
    assert len(repo.attempts) == 4
    assert all(user == owner for user, _ in repo.attempts)
    assert generator.calls == 4
