"""Provider-neutral models for agronomic knowledge retrieval and recommendations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID


class KnowledgeDocumentStatus(StrEnum):
    READY = "ready"
    NEEDS_OCR = "needs_ocr"
    FAILED = "failed"


class RetrievalStatus(StrEnum):
    AVAILABLE = "available"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    UNAVAILABLE = "unavailable"


class RecommendationStatus(StrEnum):
    SUCCEEDED = "succeeded"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class CorpusSource:
    source_id: str
    organization: str
    title: str
    language: str
    source_type: str
    source_roles: tuple[str, ...]
    relative_path: str
    country: str | None = None
    crops: tuple[str, ...] = ()
    factors: tuple[str, ...] = ()
    source_reference: str | None = None


@dataclass(frozen=True, slots=True)
class CorpusManifest:
    corpus_version: str
    sources: tuple[CorpusSource, ...]


@dataclass(frozen=True, slots=True)
class ExtractedPage:
    page_number: int
    text: str


@dataclass(frozen=True, slots=True)
class ExtractedDocument:
    pages: tuple[ExtractedPage, ...]
    total_pages: int
    pages_extracted: int
    warnings: tuple[str, ...] = ()
    needs_ocr: bool = False


@dataclass(frozen=True, slots=True)
class KnowledgeChunk:
    chunk_id: str
    sequence: int
    page_start: int
    page_end: int
    section: str | None
    content: str
    content_sha256: str
    crops: tuple[str, ...]
    factors: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class KnowledgeDocument:
    document_id: UUID
    source: CorpusSource
    corpus_version: str
    source_sha256: str
    status: KnowledgeDocumentStatus
    ingested_at: datetime
    page_count: int
    pages_extracted: int
    warnings: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EmbeddingIndex:
    index_id: UUID
    provider: str
    model: str
    dimensions: int
    index_version: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class EmbeddingVector:
    values: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class EmbeddingBatch:
    vectors: tuple[EmbeddingVector, ...]
    input_tokens: int | None = None
    request_count: int = 1


@dataclass(frozen=True, slots=True)
class StoredChunk:
    chunk_id: str
    document_id: UUID
    organization: str
    title: str
    source_roles: tuple[str, ...]
    relative_path: str
    source_reference: str | None
    corpus_version: str
    page_start: int
    page_end: int
    section: str | None
    content: str
    content_sha256: str
    crops: tuple[str, ...]
    factors: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LexicalSearchHit:
    chunk: StoredChunk
    rank: int
    score: float


@dataclass(frozen=True, slots=True)
class VectorSearchCandidate:
    chunk: StoredChunk
    vector: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class RecommendationFactor:
    factor_code: str
    label: str
    affected_fraction: float
    dominant: bool
    display_label: str | None = None


@dataclass(frozen=True, slots=True)
class RecommendationContext:
    evaluation_id: UUID
    crop_id: str
    water_regime: str
    suitability_mean: float | None
    factors: tuple[RecommendationFactor, ...]


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    evidence_id: str
    chunk_id: str
    organization: str
    title: str
    source_roles: tuple[str, ...]
    page_start: int
    page_end: int
    section: str | None
    content: str
    source_reference: str
    lexical_rank: int | None
    vector_rank: int | None
    fused_score: float


@dataclass(frozen=True, slots=True)
class RetrievedKnowledge:
    retrieval_run_id: UUID
    evaluation_id: UUID
    crop_id: str
    water_regime: str
    limiting_factors: tuple[str, ...]
    retrieval_status: RetrievalStatus
    query: str
    corpus_version: str
    retrieval_version: str
    embedding_index: EmbeddingIndex
    evidence: tuple[EvidenceItem, ...]


@dataclass(frozen=True, slots=True)
class RecommendationItem:
    text: str
    rationale: str
    citation_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class StructuredRecommendation:
    summary: str
    observations: tuple[str, ...]
    scenario_interpretation: str
    recommendations: tuple[RecommendationItem, ...]
    uncertainties: tuple[str, ...]
    citation_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RecommendationGeneration:
    recommendation: StructuredRecommendation
    provider: str
    model: str
    response_id: str | None
    input_tokens: int | None
    output_tokens: int | None


@dataclass(frozen=True, slots=True)
class RecommendationRun:
    run_id: UUID
    evaluation_id: UUID
    crop_id: str
    water_regime: str
    status: RecommendationStatus
    prompt_version: str
    provider: str
    model: str
    response_id: str | None
    corpus_version: str
    retrieval_version: str
    embedding_index_id: UUID
    cache_key: str
    recommendation: StructuredRecommendation | None
    failure_reason: str | None
    input_tokens: int | None
    output_tokens: int | None
    created_at: datetime


@dataclass(frozen=True, slots=True)
class IngestionSourceResult:
    source_id: str
    status: KnowledgeDocumentStatus
    document_id: UUID
    source_sha256: str
    page_count: int
    pages_extracted: int
    chunks_generated: int
    chunks_embedded: int
    reused: bool
    warnings: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class IngestionReport:
    corpus_version: str
    sources: tuple[IngestionSourceResult, ...]

    @property
    def documents_discovered(self) -> int:
        return len(self.sources)

    @property
    def documents_ingested(self) -> int:
        return sum(not item.reused for item in self.sources)

    @property
    def pages_extracted(self) -> int:
        return sum(item.pages_extracted for item in self.sources)

    @property
    def chunks_generated(self) -> int:
        return sum(item.chunks_generated for item in self.sources)

    @property
    def chunks_embedded(self) -> int:
        return sum(item.chunks_embedded for item in self.sources)


JsonObject = dict[str, Any]
