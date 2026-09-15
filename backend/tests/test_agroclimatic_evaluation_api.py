"""API tests for Agroclimatic Evaluation request and read resources."""

import asyncio
import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, Response

from via_backend.config import Settings
from via_backend.contexts.agroclimatic_evaluation.application import (
    AgroclimaticEvaluationService,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    CommonSupport,
    CommonSupportStatus,
    ComparableCrop,
    CropOutcome,
    CropOutcomeStatus,
    Evaluation,
    EvaluationStatus,
    ParcelSnapshot,
    ScientificTrace,
    SnapshotGeometry,
    SuitabilitySummary,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    InMemoryEvaluationRepository,
)
from via_backend.contexts.agroclimatic_evaluation.interfaces import create_router
from via_backend.main import create_app

NOW = datetime(2026, 9, 12, 15, tzinfo=UTC)


def _test_app() -> FastAPI:
    return create_app(
        Settings(
            farm_management_repository="memory",
            environmental_information_repository="memory",
            agroclimatic_evaluation_repository="memory",
        )
    )


def _app_with(evaluation: Evaluation) -> FastAPI:
    repository = InMemoryEvaluationRepository()
    repository.add(evaluation)
    app = FastAPI()
    app.include_router(
        create_router(AgroclimaticEvaluationService(repository)),
        prefix="/api/v1",
    )
    return app


def _body() -> dict[str, Any]:
    return {
        "parcel_snapshot": {
            "project_id": str(uuid4()),
            "parcel_id": str(uuid4()),
            "parcel_version": 2,
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-77.6, -11.1],
                    [-77.5, -11.1],
                    [-77.5, -11.0],
                    [-77.6, -11.1],
                ]],
            },
            "crs": "EPSG:4326",
            "captured_at": "2026-09-12T15:00:00Z",
        },
        "requested_crops": ["maize", "potato", "rice"],
    }


def _evaluation(
    *,
    status: EvaluationStatus = EvaluationStatus.QUEUED,
    outcomes: tuple[CropOutcome, ...] = (),
    failure_reason: str | None = None,
) -> Evaluation:
    return Evaluation(
        id=uuid4(),
        parcel_snapshot=ParcelSnapshot(
            project_id=uuid4(),
            parcel_id=uuid4(),
            parcel_version=2,
            geometry=SnapshotGeometry.from_geojson(_body()["parcel_snapshot"]["geometry"]),
            crs="EPSG:4326",
            captured_at=NOW,
        ),
        requested_crops=("maize", "potato", "rice"),
        status=status,
        created_at=NOW,
        outcomes=outcomes,
        failure_reason=failure_reason,
    )


def _outcome(crop_id: str, status: CropOutcomeStatus) -> CropOutcome:
    if status is CropOutcomeStatus.SUCCEEDED:
        suitability = SuitabilitySummary(
            mean=0.0,
            minimum=0.0,
            maximum=0.0,
            valid_cells=1,
            valid_area_m2=25.0,
            coverage_fraction=1.0,
            zero_suitability_area_m2=25.0,
        )
        failure_message = None
    elif status is CropOutcomeStatus.NO_COVERAGE:
        suitability = SuitabilitySummary(
            mean=None,
            minimum=None,
            maximum=None,
            valid_cells=0,
            valid_area_m2=0.0,
            coverage_fraction=0.0,
            zero_suitability_area_m2=0.0,
        )
        failure_message = None
    else:
        suitability = None
        failure_message = "internal failure at C:\\private\\workspace\\engine.py"

    return CropOutcome(
        crop_id=crop_id,
        status=status,
        suitability=suitability,
        failure_message=failure_message,
        trace=ScientificTrace(
            engine_identifier="CropSuiteLite",
            execution_reference="C:\\private\\workspace\\run-123",
            started_at=NOW,
            finished_at=NOW + timedelta(seconds=2),
            elapsed_seconds=2.0,
            execution_mode="sequential",
            parcel_sha256="parcel-hash",
            parameter_sha256=f"{crop_id}-parameter-hash",
            configuration_sha256="configuration-hash",
            source_files_unchanged=True,
        ),
    )


def _completed_outcomes() -> tuple[CropOutcome, ...]:
    return (
        _outcome("maize", CropOutcomeStatus.SUCCEEDED),
        _outcome("potato", CropOutcomeStatus.NO_COVERAGE),
        _outcome("rice", CropOutcomeStatus.FAILED),
    )

def _evaluation_with_comparison() -> Evaluation:
    evaluation = _evaluation(
        status=EvaluationStatus.SUCCEEDED,
        outcomes=_completed_outcomes(),
    )

    return replace(
        evaluation,
        common_support=CommonSupport(
            status=CommonSupportStatus.COMPARABLE,
            method="area_weighted_mean_on_common_valid_cells",
            area_crs="EPSG:6933",
            parcel_area_m2=100.0,
            common_valid_area_m2=80.0,
            common_coverage_fraction=0.8,
            eligible_crops=("maize",),
            excluded_without_coverage=("potato",),
        ),
        comparable_crops=(
            ComparableCrop(
                crop_id="maize",
                mean=0.0,
                rank=1,
            ),
        ),
    )

def test_final_result_exposes_common_support_and_comparable_crops() -> None:
    evaluation = _evaluation_with_comparison()

    response = asyncio.run(
        _request(
            _app_with(evaluation),
            "GET",
            f"/api/v1/evaluations/{evaluation.id}/result",
        )
    )

    assert response.status_code == 200

    body = response.json()

    assert body["common_support"] == {
        "status": "comparable",
        "method": "area_weighted_mean_on_common_valid_cells",
        "area_crs": "EPSG:6933",
        "parcel_area_m2": 100.0,
        "common_valid_area_m2": 80.0,
        "common_coverage_fraction": 0.8,
        "eligible_crops": ["maize"],
        "excluded_without_coverage": ["potato"],
    }

    assert body["comparable_crops"] == [
        {
            "crop_id": "maize",
            "mean": 0.0,
            "rank": 1,
        }
    ]

    assert "ranking" not in body

async def _request(app: FastAPI, method: str, path: str, **kwargs: Any) -> Response:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.request(method, path, **kwargs)


def test_create_get_and_list_evaluation() -> None:
    async def scenario() -> None:
        transport = ASGITransport(app=_test_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            body = _body()
            created_response = await client.post("/api/v1/evaluations", json=body)
            assert created_response.status_code == 201
            created = created_response.json()
            assert created["status"] == "queued"
            assert created["requested_crops"] == ["maize", "potato", "rice"]
            assert created["parcel_snapshot"] == body["parcel_snapshot"]

            status_response = await client.get(f"/api/v1/evaluations/{created['id']}")
            assert status_response.status_code == 200
            status_view = status_response.json()
            assert status_view["evaluation_id"] == created["id"]
            assert status_view["status"] == "queued"
            assert status_view["requested_crop_count"] == 3
            assert status_view["completed_crop_count"] == 0
            assert "progress_percentage" not in status_view

            listed = await client.get("/api/v1/evaluations")
            assert listed.json() == [created]

    asyncio.run(scenario())


def test_duplicate_crops_return_validation_error() -> None:
    body = _body()
    body["requested_crops"] = ["maize", "maize"]

    response = asyncio.run(_request(_test_app(), "POST", "/api/v1/evaluations", json=body))

    assert response.status_code == 422
    assert "unique" in response.json()["detail"]


@pytest.mark.parametrize("suffix", ["", "/result", "/evidence"])
def test_missing_evaluation_returns_not_found(suffix: str) -> None:
    response = asyncio.run(
        _request(
            _test_app(),
            "GET",
            f"/api/v1/evaluations/{uuid4()}{suffix}",
        )
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    ("evaluation", "completed_count"),
    [
        (_evaluation(status=EvaluationStatus.PREPARING), 0),
        (_evaluation(status=EvaluationStatus.RUNNING), 0),
        (
            _evaluation(
                status=EvaluationStatus.SUMMARIZING,
                outcomes=_completed_outcomes(),
            ),
            3,
        ),
    ],
)
def test_active_status_has_counts_without_fake_percentage(
    evaluation: Evaluation, completed_count: int
) -> None:
    response = asyncio.run(
        _request(
            _app_with(evaluation),
            "GET",
            f"/api/v1/evaluations/{evaluation.id}",
        )
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == evaluation.status.value
    assert body["requested_crop_count"] == 3
    assert body["completed_crop_count"] == completed_count
    assert "progress_percentage" not in body


def test_final_result_preserves_order_and_scientific_outcome_distinctions() -> None:
    evaluation = _evaluation(
        status=EvaluationStatus.SUCCEEDED,
        outcomes=_completed_outcomes(),
    )

    response = asyncio.run(
        _request(
            _app_with(evaluation),
            "GET",
            f"/api/v1/evaluations/{evaluation.id}/result",
        )
    )

    assert response.status_code == 200
    body = response.json()
    assert body["availability"] == "final"
    assert body["requested_crops"] == ["maize", "potato", "rice"]
    assert [item["crop_id"] for item in body["outcomes"]] == [
        "maize",
        "potato",
        "rice",
    ]
    assert [item["status"] for item in body["outcomes"]] == [
        "succeeded",
        "no_coverage",
        "failed",
    ]
    assert body["outcomes"][0]["suitability"]["mean"] == 0.0
    assert body["outcomes"][0]["suitability"]["valid_cells"] == 1
    assert body["outcomes"][1]["suitability"]["mean"] is None
    assert body["outcomes"][1]["suitability"]["valid_cells"] == 0
    assert body["outcomes"][2]["suitability"] is None
    assert body["common_support"] is None
    assert body["comparable_crops"] == []


def test_active_result_is_explicitly_partial() -> None:
    evaluation = _evaluation(
        status=EvaluationStatus.RUNNING,
        outcomes=(_outcome("maize", CropOutcomeStatus.SUCCEEDED),),
    )

    response = asyncio.run(
        _request(
            _app_with(evaluation),
            "GET",
            f"/api/v1/evaluations/{evaluation.id}/result",
        )
    )

    assert response.status_code == 200
    body = response.json()
    assert body["availability"] == "partial"
    assert body["evaluation_status"] == "running"
    assert body["completed_crop_count"] == 1
    assert [item["crop_id"] for item in body["outcomes"]] == ["maize"]
    assert body["common_support"] is None
    assert body["comparable_crops"] == []


def test_queued_result_is_explicitly_pending() -> None:
    evaluation = _evaluation()

    response = asyncio.run(
        _request(
            _app_with(evaluation),
            "GET",
            f"/api/v1/evaluations/{evaluation.id}/result",
        )
    )

    assert response.status_code == 200

    body = response.json()

    assert body["availability"] == "pending"
    assert body["outcomes"] == []
    assert body["common_support"] is None
    assert body["comparable_crops"] == []


def test_failed_evaluation_has_sanitized_public_semantics() -> None:
    evaluation = _evaluation(
        status=EvaluationStatus.FAILED,
        outcomes=(_outcome("maize", CropOutcomeStatus.SUCCEEDED),),
        failure_reason="RuntimeError: database_url=postgresql://secret C:\\work\\run.py",
    )

    status_response = asyncio.run(
        _request(
            _app_with(evaluation),
            "GET",
            f"/api/v1/evaluations/{evaluation.id}",
        )
    )
    result_response = asyncio.run(
        _request(
            _app_with(evaluation),
            "GET",
            f"/api/v1/evaluations/{evaluation.id}/result",
        )
    )
    evidence_response = asyncio.run(
        _request(
            _app_with(evaluation),
            "GET",
            f"/api/v1/evaluations/{evaluation.id}/evidence",
        )
    )

    assert status_response.status_code == 200
    assert status_response.json()["failed"] is True
    assert "failure_reason" not in status_response.json()
    assert result_response.json()["availability"] == "failed"
    assert evidence_response.json()["availability"] == "failed"
    serialized = json.dumps(
        [status_response.json(), result_response.json(), evidence_response.json()]
    ).casefold()
    assert "secret" not in serialized
    assert "database_url" not in serialized
    assert "run.py" not in serialized


def test_evidence_exposes_only_current_safe_trace_subset() -> None:
    evaluation = _evaluation(
        status=EvaluationStatus.SUCCEEDED,
        outcomes=_completed_outcomes(),
    )

    response = asyncio.run(
        _request(
            _app_with(evaluation),
            "GET",
            f"/api/v1/evaluations/{evaluation.id}/evidence",
        )
    )

    assert response.status_code == 200
    body = response.json()
    assert body["availability"] == "final"
    assert [item["crop_id"] for item in body["evidence"]] == [
        "maize",
        "potato",
        "rice",
    ]
    assert set(body["evidence"][0]["trace"]) == {
        "engine_identifier",
        "started_at",
        "finished_at",
        "elapsed_seconds",
        "execution_mode",
        "parcel_sha256",
        "parameter_sha256",
        "configuration_sha256",
        "source_files_unchanged",
    }
    serialized = json.dumps(body).casefold()
    assert "execution_reference" not in serialized
    assert "failure_message" not in serialized
    assert "private" not in serialized
    assert "workspace" not in serialized
    assert "python" not in serialized
    assert "postgresql" not in serialized