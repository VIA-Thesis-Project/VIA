"""HTTP contract tests for agronomic knowledge and recommendations."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import cast
from uuid import UUID, uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient

from via_backend.contexts.agroclimatic_evaluation.application.public import WaterRegime
from via_backend.contexts.decision_support.application.knowledge_models import (
    EmbeddingIndex,
    EvidenceItem,
    RecommendationContext,
    RecommendationFactor,
    RecommendationRun,
    RecommendationStatus,
    RetrievalStatus,
    RetrievedKnowledge,
)
from via_backend.contexts.decision_support.application.knowledge_services import (
    RecommendationApplicationService,
    RecommendationContextBuilder,
)
from via_backend.contexts.decision_support.interfaces import create_router


def _context(evaluation_id: UUID, crop_id: str, regime: WaterRegime) -> RecommendationContext:
    return RecommendationContext(
        evaluation_id=evaluation_id,
        crop_id=crop_id,
        water_regime=regime.value,
        suitability_mean=0.0,
        factors=(RecommendationFactor("precipitation", "precipitation", 1.0, True),),
    )


def _knowledge(context: RecommendationContext) -> RetrievedKnowledge:
    return RetrievedKnowledge(
        retrieval_run_id=uuid4(),
        evaluation_id=context.evaluation_id,
        crop_id=context.crop_id,
        water_regime=context.water_regime,
        limiting_factors=("precipitation",),
        retrieval_status=RetrievalStatus.AVAILABLE,
        query="precipitation",
        corpus_version="test",
        retrieval_version="hybrid-rrf-v1",
        embedding_index=EmbeddingIndex(
            uuid4(), "fake", "fake", 3, "test", datetime.now(UTC)
        ),
        evidence=(
            EvidenceItem(
                "SOURCE_1",
                "chunk-1",
                "FAO",
                "Guidance",
                ("methodology",),
                1,
                1,
                None,
                "Evidence",
                "fao/guidance.pdf",
                1,
                1,
                1.0,
            ),
        ),
    )


class _Builder:
    def build(
        self, evaluation_id: UUID, crop_id: str, water_regime: WaterRegime
    ) -> RecommendationContext:
        return _context(evaluation_id, crop_id, water_regime)


class _Service:
    def __init__(self) -> None:
        self.retrieve_calls = 0
        self.generate_calls = 0
        self.list_calls = 0
        self.runs: tuple[RecommendationRun, ...] = ()

    def retrieve(self, context: RecommendationContext) -> RetrievedKnowledge:
        self.retrieve_calls += 1
        return _knowledge(context)

    def generate(
        self, context: RecommendationContext, *, force_regenerate: bool = False
    ) -> RecommendationRun:
        del force_regenerate
        self.generate_calls += 1
        run = RecommendationRun(
            run_id=uuid4(),
            evaluation_id=context.evaluation_id,
            crop_id=context.crop_id,
            water_regime=context.water_regime,
            status=RecommendationStatus.INSUFFICIENT_EVIDENCE,
            prompt_version="test",
            provider="fake",
            model="fake",
            response_id=None,
            corpus_version="test",
            retrieval_version="test",
            embedding_index_id=uuid4(),
            cache_key="cache",
            recommendation=None,
            failure_reason="insufficient_retrieved_evidence",
            input_tokens=None,
            output_tokens=None,
            created_at=datetime.now(UTC),
        )
        self.runs = (run,)
        return run

    def list_for_evaluation(self, evaluation_id: UUID) -> tuple[RecommendationRun, ...]:
        self.list_calls += 1
        return tuple(run for run in self.runs if run.evaluation_id == evaluation_id)


def _client(service: _Service) -> TestClient:
    app = FastAPI()
    app.include_router(
        create_router(
            cast(RecommendationContextBuilder, _Builder()),
            cast(RecommendationApplicationService, service),
        ),
        prefix="/api/v1",
    )
    return TestClient(app)


def test_get_knowledge_retrieves_evidence_without_generation() -> None:
    service = _Service()
    evaluation_id = uuid4()
    response = _client(service).get(
        f"/api/v1/decision-support/evaluations/{evaluation_id}/knowledge",
        params={"crop_id": "maize", "water_regime": "rainfed"},
    )
    assert response.status_code == 200
    assert response.json()["evidence"][0]["evidence_id"] == "SOURCE_1"
    assert response.json()["evidence"][0]["source_reference"] == "fao/guidance.pdf"
    assert service.retrieve_calls == 1
    assert service.generate_calls == 0


def test_post_generates_once_and_get_reads_persisted_only() -> None:
    service = _Service()
    evaluation_id = uuid4()
    client = _client(service)
    posted = client.post(
        f"/api/v1/decision-support/evaluations/{evaluation_id}/recommendations",
        json={"crop_id": "maize", "water_regime": "rainfed"},
    )
    assert posted.status_code == 200
    assert service.generate_calls == 1

    listed = client.get(
        f"/api/v1/decision-support/evaluations/{evaluation_id}/recommendations",
        params={"crop_id": "maize", "water_regime": "rainfed"},
    )
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert service.generate_calls == 1
    assert service.retrieve_calls == 0
    assert service.list_calls == 1
