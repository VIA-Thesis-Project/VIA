"""Repository contract tests for Agroclimatic Evaluation."""

from datetime import UTC, datetime
from uuid import uuid4

from via_backend.contexts.agroclimatic_evaluation.domain import (
    Evaluation,
    EvaluationStatus,
    ParcelSnapshot,
    SnapshotGeometry,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    InMemoryEvaluationRepository,
)


def test_round_trip_retains_snapshot_after_source_geometry_changes() -> None:
    source_geometry = {
        "type": "Polygon",
        "coordinates": [[[-77.6, -11.1], [-77.5, -11.1], [-77.5, -11.0], [-77.6, -11.1]]],
    }
    now = datetime(2026, 9, 12, tzinfo=UTC)
    evaluation = Evaluation(
        id=uuid4(),
        parcel_snapshot=ParcelSnapshot(
            project_id=uuid4(),
            parcel_id=uuid4(),
            parcel_version=1,
            geometry=SnapshotGeometry.from_geojson(source_geometry),
            crs="EPSG:4326",
            captured_at=now,
        ),
        requested_crops=("maize", "rice"),
        status=EvaluationStatus.QUEUED,
        created_at=now,
    )
    repository = InMemoryEvaluationRepository()
    repository.add(evaluation)

    source_geometry["coordinates"][0][0][0] = 0

    restored = repository.get(evaluation.id)
    assert restored == evaluation
    assert restored is not None
    assert restored.parcel_snapshot.geometry.to_geojson()["coordinates"][0][0][0] == -77.6
    assert repository.list_all() == (evaluation,)
