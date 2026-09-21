"""Focused IA-3 ownership and authoritative parcel-snapshot tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

import pytest

from via_backend.contexts.agroclimatic_evaluation.application import (
    AgroclimaticEvaluationService,
    AuthorizedParcelSnapshotNotFoundError,
    EnvironmentalInputReferenceInput,
    GetEvaluation,
    ListEvaluations,
    ParcelReferenceInput,
    RequestEvaluation,
)
from via_backend.contexts.agroclimatic_evaluation.application import (
    ResourceNotFoundError as EvaluationNotFoundError,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    Evaluation,
    EvaluationStatus,
    ParcelSnapshot,
    SnapshotGeometry,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    InMemoryEvaluationRepository,
)
from via_backend.contexts.farm_management.application import (
    AuthorizedParcelSnapshotNotFoundError as FarmSnapshotNotFoundError,
)
from via_backend.contexts.farm_management.application import (
    CreateParcel,
    CreateProject,
    FarmManagementService,
    ListProjects,
    ReviseParcelGeometry,
)
from via_backend.contexts.farm_management.domain import Project
from via_backend.contexts.farm_management.infrastructure import (
    InMemoryParcelRepository,
    InMemoryProjectRepository,
)

NOW = datetime(2026, 9, 21, 10, tzinfo=UTC)
USER_A = UUID("11111111-1111-4111-8111-111111111111")
USER_B = UUID("22222222-2222-4222-8222-222222222222")
PROJECT_A = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
PARCEL_A = UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")
EVALUATION_ID = UUID("cccccccc-cccc-4ccc-8ccc-cccccccccccc")
DATASET_ID = UUID("dddddddd-dddd-4ddd-8ddd-dddddddddddd")
DATASET_VERSION_ID = UUID("eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee")


def _polygon(offset: float = 0.0) -> dict[str, Any]:
    return {
        "type": "Polygon",
        "coordinates": [[
            [-77.6 + offset, -11.1],
            [-77.5 + offset, -11.1],
            [-77.5 + offset, -11.0],
            [-77.6 + offset, -11.1],
        ]],
    }


def test_farm_ownership_and_authoritative_exact_version_resolution() -> None:
    projects = InMemoryProjectRepository()
    parcels = InMemoryParcelRepository()
    identifiers = iter((PROJECT_A, PARCEL_A))
    instants = iter((NOW, NOW, NOW + timedelta(hours=1)))
    service = FarmManagementService(
        projects,
        parcels,
        new_id=lambda: next(identifiers),
        clock=lambda: next(instants),
    )

    service.create_project(CreateProject("A project", USER_A))
    projects.add(Project(UUID(int=90), "Legacy", NOW, owner_user_id=None))
    projects.add(Project(UUID(int=91), "B project", NOW, owner_user_id=USER_B))
    created = service.create_parcel(
        CreateParcel(PROJECT_A, USER_A, "A parcel", _polygon())
    )
    service.revise_parcel_geometry(
        ReviseParcelGeometry(PROJECT_A, USER_A, PARCEL_A, _polygon(0.01))
    )

    stored_project = projects.get(PROJECT_A)
    assert stored_project is not None
    assert stored_project.owner_user_id == USER_A
    assert [project.id for project in service.list_projects(ListProjects(USER_A))] == [
        PROJECT_A
    ]
    assert created.id == PARCEL_A

    first = service.resolve_authorized_parcel_snapshot(
        owner_user_id=USER_A,
        project_id=PROJECT_A,
        parcel_id=PARCEL_A,
        parcel_version=1,
    )
    second = service.resolve_authorized_parcel_snapshot(
        owner_user_id=USER_A,
        project_id=PROJECT_A,
        parcel_id=PARCEL_A,
        parcel_version=2,
    )

    assert first.geometry.type == "Polygon"
    assert first.geometry.coordinates == (
        ((-77.6, -11.1), (-77.5, -11.1), (-77.5, -11.0), (-77.6, -11.1)),
    )
    assert first.crs == second.crs == "EPSG:4326"
    assert first.captured_at == NOW
    assert second.captured_at == NOW + timedelta(hours=1)

    for owner, project, parcel, version in (
        (USER_B, PROJECT_A, PARCEL_A, 1),
        (USER_A, UUID(int=91), PARCEL_A, 1),
        (USER_A, PROJECT_A, UUID(int=999), 1),
        (USER_A, PROJECT_A, PARCEL_A, 3),
    ):
        with pytest.raises(FarmSnapshotNotFoundError):
            service.resolve_authorized_parcel_snapshot(
                owner_user_id=owner,
                project_id=project,
                parcel_id=parcel,
                parcel_version=version,
            )


class _AuthoritativeProvider:
    def __init__(self, snapshot: ParcelSnapshot) -> None:
        self.snapshot = snapshot
        self.calls: list[tuple[UUID, UUID, UUID, int]] = []

    def resolve(
        self,
        *,
        owner_user_id: UUID,
        project_id: UUID,
        parcel_id: UUID,
        parcel_version: int,
    ) -> ParcelSnapshot:
        self.calls.append((owner_user_id, project_id, parcel_id, parcel_version))
        return self.snapshot


def test_evaluation_persists_authenticated_owner_and_authoritative_snapshot() -> None:
    snapshot = ParcelSnapshot(
        PROJECT_A,
        PARCEL_A,
        2,
        SnapshotGeometry.from_geojson(_polygon(0.01)),
        "EPSG:4326",
        NOW + timedelta(hours=1),
    )
    provider = _AuthoritativeProvider(snapshot)
    repository = InMemoryEvaluationRepository()
    service = AgroclimaticEvaluationService(
        repository,
        provider,
        new_id=lambda: EVALUATION_ID,
        clock=lambda: NOW + timedelta(hours=2),
    )

    result = service.request_evaluation(
        RequestEvaluation(
            owner_user_id=USER_A,
            parcel_reference=ParcelReferenceInput(PROJECT_A, PARCEL_A, 2),
            requested_crops=("maize",),
            environmental_inputs=(
                EnvironmentalInputReferenceInput(
                    "soil.ph", DATASET_ID, DATASET_VERSION_ID
                ),
            ),
        )
    )

    stored = repository.get(EVALUATION_ID)
    assert stored is not None
    assert stored.owner_user_id == USER_A
    assert stored.parcel_snapshot == snapshot
    assert result.parcel_snapshot.geometry == _polygon(0.01)
    assert provider.calls == [(USER_A, PROJECT_A, PARCEL_A, 2)]
    assert service.get_evaluation(GetEvaluation(EVALUATION_ID, USER_A)).evaluation_id == (
        EVALUATION_ID
    )
    assert [item.id for item in service.list_evaluations(ListEvaluations(USER_A))] == [
        EVALUATION_ID
    ]
    with pytest.raises(EvaluationNotFoundError):
        service.get_evaluation(GetEvaluation(EVALUATION_ID, USER_B))

    legacy = Evaluation(
        id=UUID(int=88),
        parcel_snapshot=snapshot,
        requested_crops=("maize",),
        status=EvaluationStatus.QUEUED,
        created_at=NOW,
        owner_user_id=None,
    )
    repository.add(legacy)
    assert repository.get(legacy.id) == legacy
    assert repository.get_for_owner(USER_A, legacy.id) is None
    assert legacy not in repository.list_for_owner(USER_A)


class _MissingProvider:
    def resolve(self, **_: object) -> ParcelSnapshot:
        raise AuthorizedParcelSnapshotNotFoundError


def test_evaluation_translates_foreign_or_missing_parcel_to_not_found() -> None:
    service = AgroclimaticEvaluationService(
        InMemoryEvaluationRepository(), _MissingProvider()
    )

    with pytest.raises(EvaluationNotFoundError, match="parcel version"):
        service.request_evaluation(
            RequestEvaluation(
                owner_user_id=USER_B,
                parcel_reference=ParcelReferenceInput(PROJECT_A, PARCEL_A, 1),
                requested_crops=("maize",),
                environmental_inputs=(
                    EnvironmentalInputReferenceInput(
                        "soil.ph", DATASET_ID, DATASET_VERSION_ID
                    ),
                ),
            )
        )
