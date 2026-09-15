"""Configured Decision Support policy-selection workflow."""

from __future__ import annotations

from dataclasses import dataclass

from ..domain.models import (
    ViabilityPolicyEvaluation,
    ViabilityPolicySnapshot,
)
from ..domain.policy import DeterministicViabilityPolicy
from .ports import IDefaultViabilityPolicyProvider
from .queries import (
    EvaluateConfiguredDecisionSupport,
    EvaluateDecisionSupport,
    ViabilityPolicySelection,
    ViabilityPolicySelectionMode,
)
from .service import DecisionSupportResult, DecisionSupportService


@dataclass(frozen=True, slots=True)
class ConfiguredDecisionSupportResult:
    """Decision Support result together with the policy selection actually used."""

    selection_mode: ViabilityPolicySelectionMode
    policy: ViabilityPolicySnapshot
    result: DecisionSupportResult[ViabilityPolicyEvaluation]


class DecisionSupportWorkflow:
    """Resolve default/custom policy selection and delegate deterministic execution."""

    def __init__(
        self,
        decision_support: DecisionSupportService,
        default_policy_provider: IDefaultViabilityPolicyProvider,
    ) -> None:
        self._decision_support = decision_support
        self._default_policy_provider = default_policy_provider

    def evaluate(
        self,
        query: EvaluateConfiguredDecisionSupport,
    ) -> ConfiguredDecisionSupportResult:
        snapshot = self._resolve_policy(query.policy_selection)

        policy = DeterministicViabilityPolicy(
            reference=snapshot.reference,
            configuration=snapshot.configuration,
        )

        result = self._decision_support.evaluate(
            EvaluateDecisionSupport(
                evaluation_id=query.evaluation_id,
                policy=snapshot.reference,
            ),
            policy,
        )

        return ConfiguredDecisionSupportResult(
            selection_mode=query.policy_selection.mode,
            policy=snapshot,
            result=result,
        )

    def _resolve_policy(
        self,
        selection: ViabilityPolicySelection,
    ) -> ViabilityPolicySnapshot:
        if selection.mode is ViabilityPolicySelectionMode.DEFAULT:
            return self._default_policy_provider.get_default_viability_policy()

        if selection.custom_policy is None:
            raise ValueError(
                "Custom policy selection requires an explicit policy snapshot."
            )

        return selection.custom_policy