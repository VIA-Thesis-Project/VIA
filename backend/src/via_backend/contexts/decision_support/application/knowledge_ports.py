"""Ports for the Decision Support agronomic knowledge subsystem."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from .knowledge_models import (
    CorpusManifest,
    CorpusSource,
    EmbeddingBatch,
    EmbeddingIndex,
    ExtractedDocument,
    KnowledgeChunk,
    KnowledgeDocument,
    LexicalSearchHit,
    RecommendationContext,
    RecommendationGeneration,
    RecommendationRun,
    RetrievedKnowledge,
    StoredChunk,
    VectorSearchCandidate,
)


@runtime_checkable
class IKnowledgeSourceCatalog(Protocol):
    def load_manifest(self) -> CorpusManifest: ...

    def read_source(self, source: CorpusSource) -> bytes: ...


@runtime_checkable
class IDocumentTextExtractor(Protocol):
    def extract(self, content: bytes) -> ExtractedDocument: ...


@runtime_checkable
class IKnowledgeChunker(Protocol):
    def chunk(
        self,
        source: CorpusSource,
        source_sha256: str,
        corpus_version: str,
        extracted: ExtractedDocument,
    ) -> tuple[KnowledgeChunk, ...]: ...


@runtime_checkable
class IEmbeddingProvider(Protocol):
    @property
    def provider_name(self) -> str: ...

    @property
    def model(self) -> str: ...

    @property
    def dimensions(self) -> int: ...

    def embed(self, texts: tuple[str, ...]) -> EmbeddingBatch: ...


@runtime_checkable
class IKnowledgeCorpusRepository(Protocol):
    def find_document(
        self,
        source_id: str,
        source_sha256: str,
        corpus_version: str,
    ) -> KnowledgeDocument | None: ...

    def ensure_embedding_index(self, index: EmbeddingIndex) -> EmbeddingIndex: ...

    def reusable_embeddings(
        self,
        chunk_ids: tuple[str, ...],
        embedding_index_id: UUID,
    ) -> dict[str, tuple[float, ...]]: ...

    def save_document(
        self,
        document: KnowledgeDocument,
        chunks: tuple[KnowledgeChunk, ...],
        embedding_index: EmbeddingIndex,
        embeddings: dict[str, tuple[float, ...]],
        embedding_input_tokens: int | None,
        embedding_request_count: int,
    ) -> None: ...

    def lexical_search(
        self,
        query: str,
        crop_id: str,
        factor_codes: tuple[str, ...],
        corpus_version: str,
        limit: int,
    ) -> tuple[LexicalSearchHit, ...]: ...

    def vector_candidates(
        self,
        crop_id: str,
        factor_codes: tuple[str, ...],
        corpus_version: str,
        embedding_index_id: UUID,
    ) -> tuple[VectorSearchCandidate, ...]: ...

    def persist_retrieval(self, retrieved: RetrievedKnowledge) -> None: ...


@runtime_checkable
class IRecommendationGenerator(Protocol):
    @property
    def provider_name(self) -> str: ...

    @property
    def model(self) -> str: ...

    def generate(
        self,
        context: RecommendationContext,
        evidence: RetrievedKnowledge,
    ) -> RecommendationGeneration: ...


@runtime_checkable
class IRecommendationRepository(Protocol):
    def find_succeeded_by_cache_key(self, cache_key: str) -> RecommendationRun | None: ...

    def save(self, run: RecommendationRun, evidence: RetrievedKnowledge) -> None: ...

    def list_for_evaluation(self, evaluation_id: UUID) -> tuple[RecommendationRun, ...]: ...


@runtime_checkable
class IKnowledgeRetriever(Protocol):
    def retrieve(self, context: RecommendationContext) -> RetrievedKnowledge: ...


@runtime_checkable
class IStoredChunkReader(Protocol):
    def get_chunks(self, chunk_ids: tuple[str, ...]) -> tuple[StoredChunk, ...]: ...
