"""HTTP interface for agronomic knowledge retrieval and recommendations."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, Field

from via_backend.contexts.agroclimatic_evaluation.application.public import (
    OwnedEvaluationNotFoundError,
    OwnedEvaluationResolver,
    WaterRegime,
)
from via_backend.contexts.identity_access.application.public import (
    AuthenticatedPrincipal,
    PrincipalResolver,
    UserRole,
)
from via_backend.cost_protection import (
    FixedWindowLimiter,
    QuotaExceededError,
    RateLimitExceededError,
)

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
    owned_evaluations: OwnedEvaluationResolver,
    principal_resolver: PrincipalResolver,
    limiter: FixedWindowLimiter,
    knowledge_limit: int,
    recommendation_limit: int,
) -> APIRouter:
    principal_dependency = Depends(principal_resolver)

    def authorize(owner_user_id: UUID, evaluation_id: UUID) -> None:
        try:
            owned_evaluations.resolve_owned_evaluation(owner_user_id, evaluation_id)
        except OwnedEvaluationNotFoundError as error:
            raise HTTPException(status_code=404, detail="Evaluation was not found.") from error

    def throttle(action: str, user_id: UUID, limit: int) -> None:
        try:
            limiter.check(action, str(user_id), limit)
        except RateLimitExceededError as error:
            raise HTTPException(
                status_code=429,
                detail="Too many requests.",
                headers={"Retry-After": str(error.retry_after)},
            ) from error

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
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> RetrievedKnowledge:
        authorize(principal.user_id, evaluation_id)
        throttle("knowledge", principal.user_id, knowledge_limit)
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
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> RecommendationRun:
        authorize(principal.user_id, evaluation_id)
        if request.force_regenerate and principal.role is not UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Administrator permission required.")
        throttle("recommendations", principal.user_id, recommendation_limit)
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
                owner_user_id=principal.user_id,
            )
        except KnowledgeProviderUnavailableError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(exc),
            ) from exc
        except QuotaExceededError as exc:
            raise HTTPException(
                status_code=429,
                detail="Daily quota exceeded.",
                headers={"Retry-After": str(exc.retry_after)},
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
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> tuple[RecommendationRun, ...]:
        authorize(principal.user_id, evaluation_id)
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
