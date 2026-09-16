"""Application lifecycle for immutable Decision Support viability policies."""

from __future__ import annotations

from dataclasses import dataclass

from ..domain.models import (
    PolicyReference,
    ViabilityPolicyConfiguration,
    ViabilityPolicySnapshot,
)
from .errors import (
    InvalidViabilityPolicyRevisionError,
    ViabilityPolicyVersionNotFoundError,
)
from .ports import IViabilityPolicyRepository


@dataclass(frozen=True, slots=True)
class RegisterViabilityPolicyVersion:
    """Register one explicitly identified immutable viability-policy version."""

    reference: PolicyReference
    configuration: ViabilityPolicyConfiguration


@dataclass(frozen=True, slots=True)
class ReviseViabilityPolicyVersion:
    """Create a new immutable version derived from an existing policy identity."""

    source: PolicyReference
    new_version: str
    configuration: ViabilityPolicyConfiguration


class ViabilityPolicyLifecycleService:
    """Coordinate registration and revision of immutable policy snapshots."""

    def __init__(self, repository: IViabilityPolicyRepository) -> None:
        self._repository = repository

    def register(
        self,
        command: RegisterViabilityPolicyVersion,
    ) -> ViabilityPolicySnapshot:
        snapshot = ViabilityPolicySnapshot(
            reference=command.reference,
            configuration=command.configuration,
        )
        self._repository.add(snapshot)
        return snapshot

    def revise(
        self,
        command: ReviseViabilityPolicyVersion,
    ) -> ViabilityPolicySnapshot:
        source = self._repository.get(command.source)
        if source is None:
            raise ViabilityPolicyVersionNotFoundError(
                "Cannot revise missing viability policy "
                f"{command.source.identifier}:{command.source.version}."
            )

        if command.new_version == command.source.version:
            raise InvalidViabilityPolicyRevisionError(
                "A viability policy revision must create a distinct version."
            )

        revised = ViabilityPolicySnapshot(
            reference=PolicyReference(
                identifier=source.reference.identifier,
                version=command.new_version,
            ),
            configuration=command.configuration,
        )
        self._repository.add(revised)
        return revised
