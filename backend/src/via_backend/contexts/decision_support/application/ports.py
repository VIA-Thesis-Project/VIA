"""Application ports for deterministic Decision Support policies."""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from ..domain.models import DecisionEvidence, PolicyReference

PolicyEvaluationT_co = TypeVar("PolicyEvaluationT_co", covariant=True)


@runtime_checkable
class IDecisionPolicy(Protocol[PolicyEvaluationT_co]):
    """Evaluate comparable evidence without changing its scientific values."""

    @property
    def reference(self) -> PolicyReference: ...

    def evaluate(self, evidence: DecisionEvidence) -> PolicyEvaluationT_co: ...
