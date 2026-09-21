"""HTTP interface for agronomic knowledge retrieval and recommendations."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, Field

from via_backend.contexts.agroclimatic_evaluation.application.public import WaterRegime

from ..application.knowledge_models import (
    RecommendationContext,
    RecommendationRun,
    RetrievedKnowledge,
)
from ..application.knowledge_services import (
    KnowledgeContextConflictError,
    KnowledgeContextUnavailableError,
    KnowledgeProviderUnavailableError,
    RecommendationApplicationService,
    RecommendationContextBuilder,
)


class RecommendationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    crop_id: str = Field(min_length=1)
    water_regime: WaterRegime
    force_regenerate: bool = False


def create_router(
    context_builder: RecommendationContextBuilder,
    recommendations: RecommendationApplicationService,
) -> APIRouter:
    router = APIRouter(prefix="/decision-support", tags=["decision-support"])

    @router.get(
        "/evaluations/{evaluation_id}/knowledge",
        response_model=RetrievedKnowledge,
        operation_id="get_evaluation_knowledge",
        description=(
            "Retrieve evidence for one successful crop scenario without generating a "
            "recommendation. affected_fraction values in the source context are 0..1."
        ),
    )
    def get_knowledge(
        evaluation_id: UUID,
        crop_id: Annotated[str, Query(min_length=1)],
        water_regime: Annotated[WaterRegime, Query()],
    ) -> RetrievedKnowledge:
        context = _build_context(context_builder, evaluation_id, crop_id, water_regime)
        try:
            return recommendations.retrieve(context)
        except KnowledgeProviderUnavailableError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(exc),
            ) from exc

    @router.post(
        "/evaluations/{evaluation_id}/recommendations",
        response_model=RecommendationRun,
        operation_id="create_evaluation_recommendation",
        description=(
            "Generate or reuse an evidence-grounded recommendation for one finalized "
            "crop and water-regime scenario."
        ),
    )
    def generate_recommendation(
        evaluation_id: UUID,
        request: RecommendationRequest,
    ) -> RecommendationRun:
        context = _build_context(
            context_builder,
            evaluation_id,
            request.crop_id,
            request.water_regime,
        )
        try:
            return recommendations.generate(
                context,
                force_regenerate=request.force_regenerate,
            )
        except KnowledgeProviderUnavailableError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(exc),
            ) from exc

    @router.get(
        "/evaluations/{evaluation_id}/recommendations",
        response_model=list[RecommendationRun],
        operation_id="list_evaluation_recommendations",
        description="List persisted recommendation runs without invoking a provider.",
    )
    def list_recommendations(
        evaluation_id: UUID,
        crop_id: Annotated[str | None, Query(min_length=1)] = None,
        water_regime: Annotated[WaterRegime | None, Query()] = None,
    ) -> tuple[RecommendationRun, ...]:
        runs = recommendations.list_for_evaluation(evaluation_id)
        if crop_id is not None:
            runs = tuple(item for item in runs if item.crop_id == crop_id)
        if water_regime is not None:
            runs = tuple(item for item in runs if item.water_regime == water_regime.value)
        return runs

    return router


def _build_context(
    builder: RecommendationContextBuilder,
    evaluation_id: UUID,
    crop_id: str,
    water_regime: WaterRegime,
) -> RecommendationContext:
    try:
        return builder.build(evaluation_id, crop_id, water_regime)
    except KnowledgeContextConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except KnowledgeContextUnavailableError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
