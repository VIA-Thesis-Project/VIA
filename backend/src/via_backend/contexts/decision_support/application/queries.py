"""Decision Support application query messages."""

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from ..domain.models import PolicyReference, ViabilityPolicySnapshot


@dataclass(frozen=True, slots=True)
class EvaluateDecisionSupport:
    """Prepare evidence and apply one explicitly versioned policy when possible."""

    evaluation_id: UUID
    policy: PolicyReference


class ViabilityPolicySelectionMode(StrEnum):
    """How the viability policy configuration is selected for one execution."""

    DEFAULT = "default"
    CUSTOM = "custom"


@dataclass(frozen=True, slots=True)
class ViabilityPolicySelection:
    """Select either VIA's current default policy or an explicit custom snapshot."""

    mode: ViabilityPolicySelectionMode
    custom_policy: ViabilityPolicySnapshot | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.mode, ViabilityPolicySelectionMode):
            raise ValueError("Policy selection mode must be recognized.")

        if self.mode is ViabilityPolicySelectionMode.DEFAULT:
            if self.custom_policy is not None:
                raise ValueError(
                    "Default policy selection must not include a custom policy."
                )
            return

        if self.custom_policy is None:
            raise ValueError(
                "Custom policy selection requires an explicit policy snapshot."
            )

    @classmethod
    def default(cls) -> "ViabilityPolicySelection":
        return cls(mode=ViabilityPolicySelectionMode.DEFAULT)

    @classmethod
    def custom(
        cls,
        policy: ViabilityPolicySnapshot,
    ) -> "ViabilityPolicySelection":
        return cls(
            mode=ViabilityPolicySelectionMode.CUSTOM,
            custom_policy=policy,
        )


@dataclass(frozen=True, slots=True)
class EvaluateConfiguredDecisionSupport:
    """Evaluate Decision Support using a selected viability-policy configuration."""

    evaluation_id: UUID
    policy_selection: ViabilityPolicySelection