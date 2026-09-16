"""Application ports for deterministic Decision Support policies."""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from ..domain.models import (
    DecisionEvidence,
    PolicyReference,
    ViabilityPolicySnapshot,
)

PolicyEvaluationT_co = TypeVar("PolicyEvaluationT_co", covariant=True)


@runtime_checkable
class IDecisionPolicy(Protocol[PolicyEvaluationT_co]):
    """Evaluate comparable evidence without changing its scientific values."""

    @property
    def reference(self) -> PolicyReference: ...

    def evaluate(self, evidence: DecisionEvidence) -> PolicyEvaluationT_co: ...


@runtime_checkable
class IDefaultViabilityPolicyProvider(Protocol):
    """Provide the current VIA default viability policy without owning its storage."""

    def get_default_viability_policy(self) -> ViabilityPolicySnapshot: ...

@runtime_checkable
class IViabilityPolicyRepository(Protocol):
    """Store and restore immutable viability-policy versions."""

    def add(self, policy: ViabilityPolicySnapshot) -> None: ...

    def get(
        self,
        reference: PolicyReference,
    ) -> ViabilityPolicySnapshot | None: ...

@runtime_checkable
class IDefaultViabilityPolicyStore(
    IDefaultViabilityPolicyProvider,
    Protocol,
):
    """Read and change the current default viability-policy pointer."""

    def set_default_viability_policy(
        self,
        reference: PolicyReference,
    ) -> None: ...