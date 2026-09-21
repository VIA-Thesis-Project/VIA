"""Focused Application query tests for Agroclimatic Evaluation."""

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest

from via_backend.contexts.agroclimatic_evaluation.application import (
    AgroclimaticEvaluationService,
    EvaluationResultAvailability,
    FinalizedEvaluationResultReader,
    GetEvaluation,
    GetEvaluationEvidence,
    GetEvaluationLimitations,
    GetEvaluationResult,
    GetFinalizedEvaluationResult,
    ResourceConflictError,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    CropOutcome,
    CropOutcomeStatus,
    Evaluation,
    EvaluationStatus,
    ParcelSnapshot,
    ScientificSourceFingerprint,
    ScientificTrace,
    SnapshotGeometry,
    SuitabilitySummary,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    InMemoryEvaluationRepository,
)

NOW = datetime(2026, 9, 12, 15, tzinfo=UTC)
OWNER_ID = uuid4()


class _UnusedSnapshotProvider:
    def resolve(self, **_: object) -> ParcelSnapshot:
        raise AssertionError("query attempted to resolve a parcel snapshot")


class _ReadOnlySpyRepository:
    """Repository double that fails if a query touches a mutation/worker method."""

    def __init__(self, evaluation: Evaluation) -> None:
        self.stored = evaluation
        self.get_calls = 0

    def add(
        self, evaluation: Evaluation, *, max_active: int | None = None,
        daily_limit: int | None = None,
    ) -> None:
        raise AssertionError("read query called add()")

    def save(
        self, evaluation: Evaluation, *, expected_status: EvaluationStatus
    ) -> None:
        raise AssertionError("read query called save()")

    def add_outcome(self, evaluation_id: UUID, outcome: CropOutcome) -> None:
        raise AssertionError("read query called add_outcome()")

    def get(self, evaluation_id: UUID) -> Evaluation | None:
        self.get_calls += 1
        assert evaluation_id == self.stored.id
        return self.stored

    def get_for_owner(
        self, owner_user_id: UUID, evaluation_id: UUID
    ) -> Evaluation | None:
        self.get_calls += 1
        assert owner_user_id == OWNER_ID
        assert evaluation_id == self.stored.id
        return self.stored

    def list_queued_ids(self, *, limit: int) -> tuple[UUID, ...]:
        raise AssertionError("read query called list_queued_ids()")

    def list_active(self, *, limit: int) -> tuple[Evaluation, ...]:
        raise AssertionError("read query called list_active()")

    def list_all(self) -> tuple[Evaluation, ...]:
        raise AssertionError("read query called list_all()")

    def list_for_owner(self, owner_user_id: UUID) -> tuple[Evaluation, ...]:
        raise AssertionError("read query called list_for_owner()")


def _outcome(crop_id: str, status: CropOutcomeStatus) -> CropOutcome:
    summary = None
    failure = None
    if status is CropOutcomeStatus.SUCCEEDED:
        summary = SuitabilitySummary(0.0, 0.0, 0.0, 1, 25.0, 1.0, 25.0)
    elif status is CropOutcomeStatus.NO_COVERAGE:
        summary = SuitabilitySummary(None, None, None, 0, 0.0, 0.0, 0.0)
    else:
        failure = "internal diagnostic"

    return CropOutcome(
        crop_id=crop_id,
        status=status,
        suitability=summary,
        failure_message=failure,
        trace=ScientificTrace(
            engine_identifier="CropSuiteLite",
            execution_reference=f"opaque-{crop_id}",
            started_at=NOW,
            finished_at=NOW + timedelta(seconds=1),
            elapsed_seconds=1.0,
            execution_mode="sequential",
            parcel_sha256="parcel-hash",
            parameter_sha256=f"{crop_id}-hash",
            configuration_sha256="configuration-hash",
            source_files_unchanged=True,
            source_fingerprints=(
                ScientificSourceFingerprint(
                    f"C:\\private\\science\\{crop_id}.tif",
                    "a" * 64,
                ),
                ScientificSourceFingerprint(
                    f"/tmp/engine/{crop_id}.cfg",
                    "b" * 64,
                ),
            ),
        ),
    )


def _evaluation(
    *,
    status: EvaluationStatus,
    outcomes: tuple[CropOutcome, ...] = (),
    failure_reason: str | None = None,
) -> Evaluation:
    return Evaluation(
        id=uuid4(),
        parcel_snapshot=ParcelSnapshot(
            project_id=uuid4(),
            parcel_id=uuid4(),
            parcel_version=7,
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
            captured_at=NOW,
        ),
        requested_crops=("maize", "potato", "rice"),
        status=status,
        created_at=NOW,
        owner_user_id=OWNER_ID,
        outcomes=outcomes,
        failure_reason=failure_reason,
    )


def _service(evaluation: Evaluation) -> AgroclimaticEvaluationService:
    repository = InMemoryEvaluationRepository()
    repository.add(evaluation)
    return AgroclimaticEvaluationService(repository, _UnusedSnapshotProvider())


def test_query_messages_return_read_only_views_without_mutation() -> None:
    evaluation = _evaluation(
        status=EvaluationStatus.RUNNING,
        outcomes=(_outcome("maize", CropOutcomeStatus.SUCCEEDED),),
    )
    repository = _ReadOnlySpyRepository(evaluation)
    service = AgroclimaticEvaluationService(repository, _UnusedSnapshotProvider())

    status_view = service.get_evaluation(GetEvaluation(evaluation.id, OWNER_ID))
    result_view = service.get_evaluation_result(
        GetEvaluationResult(evaluation.id, OWNER_ID)
    )
    evidence_view = service.get_evaluation_evidence(
        GetEvaluationEvidence(evaluation.id, OWNER_ID)
    )
    limitations_view = service.get_evaluation_limitations(
        GetEvaluationLimitations(evaluation.id, OWNER_ID)
    )

    assert repository.get_calls == 4
    assert repository.stored == evaluation
    assert status_view.requested_crops == ("maize", "potato", "rice")
    assert status_view.requested_crop_count == 3
    assert status_view.completed_crop_count == 1
    assert not hasattr(status_view, "progress_percentage")
    assert result_view.availability is EvaluationResultAvailability.PARTIAL
    assert [outcome.crop_id for outcome in result_view.outcomes] == ["maize"]
    assert [item.crop_id for item in evidence_view.evidence] == ["maize"]
    assert evidence_view.evidence[0].trace.source_sha256 == ("a" * 64, "b" * 64)
    assert [item.crop_id for item in limitations_view.limitations] == ["maize"]
    assert limitations_view.limitations[0].limitation_evidence.availability.value == (
        "unavailable"
    )
    assert not hasattr(limitations_view.limitations[0], "execution_reference")


def test_finalized_public_contract_preserves_order_and_outcome_semantics() -> None:
    outcomes = (
        _outcome("maize", CropOutcomeStatus.SUCCEEDED),
        _outcome("potato", CropOutcomeStatus.NO_COVERAGE),
        _outcome("rice", CropOutcomeStatus.FAILED),
    )
    evaluation = _evaluation(
        status=EvaluationStatus.SUCCEEDED,
        outcomes=outcomes,
    )
    service = _service(evaluation)

    assert isinstance(service, FinalizedEvaluationResultReader)
    published = service.get_finalized_evaluation_result(GetFinalizedEvaluationResult(evaluation.id))

    assert published.requested_crops == ("maize", "potato", "rice")
    assert [outcome.crop_id for outcome in published.outcomes] == [
        "maize",
        "potato",
        "rice",
    ]
    assert [outcome.status.value for outcome in published.outcomes] == [
        "succeeded",
        "no_coverage",
        "failed",
    ]
    assert not hasattr(published.outcomes[0].trace, "source_fingerprints")
    assert not hasattr(published.outcomes[0].trace, "source_reference")
    assert published.outcomes[0].suitability is not None
    assert published.outcomes[0].suitability.mean == 0.0
    assert published.outcomes[1].suitability is not None
    assert published.outcomes[1].suitability.mean is None
    assert published.outcomes[2].suitability is None
    assert not hasattr(published, "ranking")
    assert not hasattr(published.outcomes[0].trace, "execution_reference")


@pytest.mark.parametrize(
    "evaluation",
    [
        _evaluation(status=EvaluationStatus.QUEUED),
        _evaluation(
            status=EvaluationStatus.FAILED,
            failure_reason="internal diagnostic",
        ),
    ],
)
def test_public_contract_rejects_non_succeeded_evaluation(
    evaluation: Evaluation,
) -> None:
    with pytest.raises(ResourceConflictError, match="finalized"):
        _service(evaluation).get_finalized_evaluation_result(
            GetFinalizedEvaluationResult(evaluation.id)
        )
