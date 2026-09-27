"""In-memory policy adapters for local and test application composition."""

from __future__ import annotations

from uuid import UUID

from ..application.errors import (
    DefaultViabilityPolicyConflictError,
    DefaultViabilityPolicyNotConfiguredError,
    EvaluationPolicyBindingConflictError,
)
from ..domain.errors import PolicyVersionConflictError
from ..domain.models import PolicyReference, ViabilityPolicySnapshot


class InMemoryViabilityPolicyRepository:
    def __init__(self) -> None:
        self.policies: dict[PolicyReference, ViabilityPolicySnapshot] = {}

    def add(self, policy: ViabilityPolicySnapshot) -> None:
        prior = self.policies.get(policy.reference)
        if prior is not None and prior != policy:
            raise PolicyVersionConflictError("Policy version already exists.")
        self.policies[policy.reference] = policy

    def get(self, reference: PolicyReference) -> ViabilityPolicySnapshot | None:
        return self.policies.get(reference)


class InMemoryDefaultViabilityPolicyStore:
    def __init__(self, policies: InMemoryViabilityPolicyRepository) -> None:
        self.policies = policies
        self.current: PolicyReference | None = None

    def get_default_viability_policy(self) -> ViabilityPolicySnapshot:
        if self.current is None:
            raise DefaultViabilityPolicyNotConfiguredError(
                "No default viability policy is configured."
            )
        policy = self.policies.get(self.current)
        if policy is None:
            raise RuntimeError("Default policy is missing.")
        return policy

    def set_default_viability_policy(
        self, reference: PolicyReference, *, expected_current: PolicyReference | None
    ) -> None:
        if self.policies.get(reference) is None:
            raise ValueError("Policy version is missing.")
        if self.current != expected_current and self.current != reference:
            raise DefaultViabilityPolicyConflictError("Default viability policy changed.")
        self.current = reference


class InMemoryEvaluationPolicyBindingStore:
    def __init__(self, policies: InMemoryViabilityPolicyRepository) -> None:
        self.policies = policies
        self.bindings: dict[UUID, PolicyReference] = {}

    def bind(self, evaluation_id: UUID, reference: PolicyReference) -> None:
        previous = self.bindings.get(evaluation_id)
        if previous is not None and previous != reference:
            raise EvaluationPolicyBindingConflictError(
                "Evaluation already has a different viability policy."
            )
        self.bindings[evaluation_id] = reference

    def get(self, evaluation_id: UUID) -> ViabilityPolicySnapshot | None:
        reference = self.bindings.get(evaluation_id)
        return self.policies.get(reference) if reference is not None else None

    def release_orphan(self, evaluation_id: UUID) -> None:
        self.bindings.pop(evaluation_id, None)
