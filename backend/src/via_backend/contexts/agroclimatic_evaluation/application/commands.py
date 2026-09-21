"""Commands expressing Agroclimatic Evaluation use-case intent."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ..domain.models import EvaluationStatus
from ..domain.water_regime import WaterRegime


@dataclass(frozen=True, slots=True)
class ParcelReferenceInput:
    """Minimum Farm Management reference supplied by an authenticated caller."""

    project_id: UUID
    parcel_id: UUID
    parcel_version: int


@dataclass(frozen=True, slots=True)
class EnvironmentalInputReferenceInput:
    input_key: str
    dataset_id: UUID
    dataset_version_id: UUID


@dataclass(frozen=True, slots=True)
class RequestEvaluation:
    owner_user_id: UUID
    parcel_reference: ParcelReferenceInput
    requested_crops: tuple[str, ...]
    environmental_inputs: tuple[EnvironmentalInputReferenceInput, ...]
    requested_water_regimes: tuple[WaterRegime, ...] = (WaterRegime.RAINFED,)


@dataclass(frozen=True, slots=True)
class ExecuteEvaluation:
    """Request synchronous execution of one already-persisted evaluation."""

    evaluation_id: UUID


@dataclass(frozen=True, slots=True)
class RecoverEvaluation:
    """Fail one operator-confirmed orphaned active evaluation."""

    evaluation_id: UUID
    expected_status: EvaluationStatus
    reason: str
