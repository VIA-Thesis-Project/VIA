"""Queries supported by Agroclimatic Evaluation."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetEvaluation:
    evaluation_id: UUID


@dataclass(frozen=True, slots=True)
class GetEvaluationResult:
    evaluation_id: UUID


@dataclass(frozen=True, slots=True)
class GetEvaluationEvidence:
    evaluation_id: UUID


@dataclass(frozen=True, slots=True)
class GetEvaluationLimitations:
    evaluation_id: UUID


@dataclass(frozen=True, slots=True)
class ListEvaluations:
    pass
