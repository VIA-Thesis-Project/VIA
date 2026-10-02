"""Personal viability settings and immutable selection for new evaluations."""

from dataclasses import dataclass
from uuid import UUID, uuid4

from ..domain.models import PolicyReference, ViabilityPolicyConfiguration, ViabilityPolicySnapshot
from .default_policy import DefaultViabilityPolicyService
from .errors import UserViabilityPolicyConflictError
from .policy_lifecycle import ReviseViabilityPolicyVersion
from .ports import IUserViabilityPolicyStore


@dataclass(slots=True)
class UserViabilityPolicyService:
    defaults: DefaultViabilityPolicyService
    users: IUserViabilityPolicyStore

    def current(self, user_id: UUID) -> ViabilityPolicySnapshot:
        return self.users.get_user_viability_policy(user_id) or self.defaults.current()

    def revise(
        self,
        user_id: UUID,
        expected: PolicyReference,
        configuration: ViabilityPolicyConfiguration,
    ) -> ViabilityPolicySnapshot:
        personal = self.users.get_user_viability_policy(user_id)
        current = personal or self.defaults.current()
        if current.reference != expected:
            raise UserViabilityPolicyConflictError("Your viability settings changed.")
        if personal is not None and personal.configuration == configuration:
            return personal
        revised = current
        if current.configuration != configuration:
            revised = self.defaults.lifecycle.revise(
                ReviseViabilityPolicyVersion(
                    source=current.reference,
                    new_version=uuid4().hex,
                    configuration=configuration,
                )
            )
        self.users.set_user_viability_policy(
            user_id,
            revised.reference,
            expected_current=personal.reference if personal is not None else None,
        )
        return revised

    def bind_policy_to_evaluation(
        self, evaluation_id: UUID, owner_user_id: UUID
    ) -> ViabilityPolicySnapshot:
        snapshot = self.current(owner_user_id)
        self.defaults.bindings.bind(evaluation_id, snapshot.reference)
        return snapshot
