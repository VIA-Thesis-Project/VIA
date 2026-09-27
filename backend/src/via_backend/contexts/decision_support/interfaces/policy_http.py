"""Authenticated management of VIA's global viability policy."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from via_backend.contexts.agroclimatic_evaluation.application.public import (
    FinalizedEvaluationNotReadyError,
    OwnedEvaluationNotFoundError,
    OwnedEvaluationResolver,
    WaterRegime,
)
from via_backend.contexts.identity_access.application.public import (
    AuthenticatedPrincipal,
    PrincipalResolver,
    UserRole,
)

from ..application.default_policy import BASELINE_CONFIGURATION, DefaultViabilityPolicyService
from ..application.errors import DefaultViabilityPolicyConflictError
from ..application.queries import EvaluateDecisionSupport
from ..application.service import DecisionSupportService
from ..domain.errors import DomainValidationError
from ..domain.models import PolicyReference, ViabilityPolicyConfiguration, ViabilityPolicySnapshot
from ..domain.policy import DeterministicViabilityPolicy


class PolicyConfigurationResponse(BaseModel):
    conditional_from: float
    viable_from: float


class ViabilityPolicyResponse(BaseModel):
    identifier: str
    version: str
    conditional_from: float
    viable_from: float
    default_configuration: PolicyConfigurationResponse


class UpdateViabilityPolicyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    conditional_from: float
    viable_from: float
    expected_identifier: str
    expected_version: str


class EvaluationPolicyResponse(BaseModel):
    status: str
    policy: ViabilityPolicyResponse | None


class CropViabilityResponse(BaseModel):
    crop_id: str
    comparable_mean: float
    scientific_rank: int
    viability: str


class EvaluationViabilityResponse(BaseModel):
    status: str
    policy: ViabilityPolicyResponse | None
    assessments: list[CropViabilityResponse]


def _response(snapshot: ViabilityPolicySnapshot) -> ViabilityPolicyResponse:
    return ViabilityPolicyResponse(
        identifier=snapshot.reference.identifier,
        version=snapshot.reference.version,
        conditional_from=snapshot.configuration.conditional_from,
        viable_from=snapshot.configuration.viable_from,
        default_configuration=PolicyConfigurationResponse(
            conditional_from=BASELINE_CONFIGURATION.conditional_from,
            viable_from=BASELINE_CONFIGURATION.viable_from,
        ),
    )


def create_policy_router(
    service: DefaultViabilityPolicyService,
    principal_resolver: PrincipalResolver,
    owned_evaluations: OwnedEvaluationResolver,
    decision_support: DecisionSupportService,
) -> APIRouter:
    router = APIRouter(prefix="/decision-support", tags=["decision-support"])
    principal_dependency = Depends(principal_resolver)

    @router.get(
        "/viability-policy",
        response_model=ViabilityPolicyResponse,
        operation_id="get_default_viability_policy",
    )
    def get_policy(
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> ViabilityPolicyResponse:
        return _response(service.current())

    @router.put(
        "/viability-policy",
        response_model=ViabilityPolicyResponse,
        operation_id="update_default_viability_policy",
        responses={
            403: {"description": "Administrator permission required."},
            409: {"description": "Default policy changed since it was read."},
        },
    )
    def update_policy(
        body: UpdateViabilityPolicyRequest,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> ViabilityPolicyResponse:
        if principal.role is not UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Administrator permission required.")
        try:
            configuration = ViabilityPolicyConfiguration(
                conditional_from=body.conditional_from,
                viable_from=body.viable_from,
            )
            reference = PolicyReference(
                identifier=body.expected_identifier, version=body.expected_version
            )
            return _response(service.revise(reference, configuration))
        except DomainValidationError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        except DefaultViabilityPolicyConflictError as error:
            raise HTTPException(
                status_code=409, detail="Default viability policy changed."
            ) from error

    def authorize(owner_user_id: UUID, evaluation_id: UUID) -> None:
        try:
            owned_evaluations.resolve_owned_evaluation(owner_user_id, evaluation_id)
        except OwnedEvaluationNotFoundError as error:
            raise HTTPException(status_code=404, detail="Evaluation was not found.") from error

    @router.get(
        "/evaluations/{evaluation_id}/viability-policy",
        response_model=EvaluationPolicyResponse,
        operation_id="get_evaluation_viability_policy",
    )
    def get_evaluation_policy(
        evaluation_id: UUID,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> EvaluationPolicyResponse:
        authorize(principal.user_id, evaluation_id)
        snapshot = service.policy_for_evaluation(evaluation_id)
        return EvaluationPolicyResponse(
            status="recorded" if snapshot is not None else "policy_not_recorded",
            policy=_response(snapshot) if snapshot is not None else None,
        )

    @router.get(
        "/evaluations/{evaluation_id}/viability",
        response_model=EvaluationViabilityResponse,
        operation_id="get_evaluation_viability",
    )
    def get_evaluation_viability(
        evaluation_id: UUID,
        water_regime: WaterRegime = WaterRegime.RAINFED,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> EvaluationViabilityResponse:
        authorize(principal.user_id, evaluation_id)
        snapshot = service.policy_for_evaluation(evaluation_id)
        if snapshot is None:
            return EvaluationViabilityResponse(
                status="policy_not_recorded", policy=None, assessments=[]
            )
        try:
            result = decision_support.evaluate(
                EvaluateDecisionSupport(evaluation_id, snapshot.reference, water_regime),
                DeterministicViabilityPolicy(snapshot.reference, snapshot.configuration),
            )
        except FinalizedEvaluationNotReadyError as error:
            raise HTTPException(status_code=409, detail="Evaluation is not final.") from error
        evaluation = result.policy_evaluation
        return EvaluationViabilityResponse(
            status="classified" if evaluation is not None else result.evidence.availability.value,
            policy=_response(snapshot),
            assessments=[
                CropViabilityResponse(
                    crop_id=item.crop_id,
                    comparable_mean=item.comparable_mean,
                    scientific_rank=item.scientific_rank,
                    viability=item.viability.value,
                )
                for item in evaluation.assessments
            ]
            if evaluation is not None
            else [],
        )

    return router
