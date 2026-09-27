"""Application use cases for VIA's global viability policy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID, uuid4

from ..domain.models import PolicyReference, ViabilityPolicyConfiguration, ViabilityPolicySnapshot
from .errors import DefaultViabilityPolicyConflictError
from .policy_lifecycle import ReviseViabilityPolicyVersion, ViabilityPolicyLifecycleService
from .ports import IDefaultViabilityPolicyStore

BASELINE_CONFIGURATION = ViabilityPolicyConfiguration(conditional_from=40.0, viable_from=70.0)


class EvaluationPolicyBindingStore(Protocol):
    def bind(self, evaluation_id: UUID, reference: PolicyReference) -> None: ...
    def get(self, evaluation_id: UUID) -> ViabilityPolicySnapshot | None: ...


@dataclass(slots=True)
class DefaultViabilityPolicyService:
    defaults: IDefaultViabilityPolicyStore
    lifecycle: ViabilityPolicyLifecycleService
    bindings: EvaluationPolicyBindingStore

    def current(self) -> ViabilityPolicySnapshot:
        return self.defaults.get_default_viability_policy()

    def revise(
        self,
        expected: PolicyReference,
        configuration: ViabilityPolicyConfiguration,
    ) -> ViabilityPolicySnapshot:
        current = self.current()
        if current.reference != expected:
            raise DefaultViabilityPolicyConflictError("Default viability policy changed.")
        if current.configuration == configuration:
            return current
        revised = self.lifecycle.revise(
            ReviseViabilityPolicyVersion(
                source=current.reference,
                new_version=uuid4().hex,
                configuration=configuration,
            )
        )
        self.defaults.set_default_viability_policy(
            revised.reference, expected_current=current.reference
        )
        return revised

    def bind_default_policy_to_evaluation(self, evaluation_id: UUID) -> ViabilityPolicySnapshot:
        snapshot = self.current()
        self.bindings.bind(evaluation_id, snapshot.reference)
        return snapshot

    def policy_for_evaluation(self, evaluation_id: UUID) -> ViabilityPolicySnapshot | None:
        """None means legacy policy not recorded; never substitute today's default."""
        return self.bindings.get(evaluation_id)
