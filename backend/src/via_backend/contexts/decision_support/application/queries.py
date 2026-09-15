"""Decision Support application query messages."""

from dataclasses import dataclass
from uuid import UUID

from ..domain.models import PolicyReference


@dataclass(frozen=True, slots=True)
class EvaluateDecisionSupport:
    """Prepare evidence and apply one explicitly versioned policy when possible."""

    evaluation_id: UUID
    policy: PolicyReference
