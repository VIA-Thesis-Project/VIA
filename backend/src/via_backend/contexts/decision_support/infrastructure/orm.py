"""Database records for Decision Support; these are not domain entities."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    ARRAY,
    CheckConstraint,
    Computed,
    DateTime,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class ViabilityPolicyVersionRecord(Base):
    """One immutable persisted viability-policy configuration."""

    __tablename__ = "viability_policy_versions"
    __table_args__ = (
        CheckConstraint(
            "identifier <> '' AND identifier = btrim(identifier)",
            name="policy_identifier_nonempty_trimmed",
        ),
        CheckConstraint(
            "version <> '' AND version = btrim(version)",
            name="policy_version_nonempty_trimmed",
        ),
        CheckConstraint(
            "conditional_from >= 0 AND conditional_from <= 100",
            name="policy_conditional_threshold_valid",
        ),
        CheckConstraint(
            "viable_from >= 0 AND viable_from <= 100",
            name="policy_viable_threshold_valid",
        ),
        CheckConstraint(
            "conditional_from < viable_from",
            name="policy_threshold_order_valid",
        ),
    )

    identifier: Mapped[str] = mapped_column(
        String(120),
        primary_key=True,
        nullable=False,
    )
    version: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        nullable=False,
    )
    conditional_from: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    viable_from: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

class DefaultViabilityPolicyRecord(Base):
    """Singleton pointer to the currently selected VIA default policy version."""

    __tablename__ = "default_viability_policy"
    __table_args__ = (
        CheckConstraint(
            "slot = 'default'",
            name="default_policy_singleton_slot",
        ),
        ForeignKeyConstraint(
            ["policy_identifier", "policy_version"],
            [
                "decision_support.viability_policy_versions.identifier",
                "decision_support.viability_policy_versions.version",
            ],
            name="fk_default_policy_version",
            ondelete="RESTRICT",
        ),
    )

    slot: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
        nullable=False,
    )
    policy_identifier: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )
    policy_version: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    selected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class KnowledgeDocumentRecord(Base):
    """One immutable source-content version from the external knowledge corpus."""

    __tablename__ = "knowledge_documents"
    __table_args__ = (
        UniqueConstraint(
            "source_id",
            "source_sha256",
            "corpus_version",
            name="uq_knowledge_document_version",
        ),
        CheckConstraint(
            "status IN ('ready', 'needs_ocr', 'failed')",
            name="knowledge_document_status_supported",
        ),
        CheckConstraint(
            "source_sha256 ~ '^[0-9a-f]{64}$'",
            name="knowledge_document_sha256_valid",
        ),
        CheckConstraint(
            "relative_path <> '' AND relative_path = btrim(relative_path)",
            name="knowledge_document_relative_path_valid",
        ),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    source_id: Mapped[str] = mapped_column(String(160), nullable=False)
    organization: Mapped[str] = mapped_column(String(200), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(32), nullable=False)
    country: Mapped[str | None] = mapped_column(String(16), nullable=True)
    source_type: Mapped[str] = mapped_column(String(32), nullable=False)
    source_roles: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    relative_path: Mapped[str] = mapped_column(Text, nullable=False)
    source_reference: Mapped[str | None] = mapped_column(Text, nullable=True)
    crops: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    factors: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    source_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    corpus_version: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, nullable=False)
    pages_extracted: Mapped[int] = mapped_column(Integer, nullable=False)
    warnings: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    embedding_input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    embedding_request_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class KnowledgeChunkRecord(Base):
    __tablename__ = "knowledge_chunks"
    __table_args__ = (
        UniqueConstraint("document_id", "sequence", name="uq_knowledge_chunk_sequence"),
        CheckConstraint("sequence >= 0", name="knowledge_chunk_sequence_nonnegative"),
        CheckConstraint("page_start >= 1", name="knowledge_chunk_page_start_positive"),
        CheckConstraint("page_end >= page_start", name="knowledge_chunk_page_order_valid"),
        CheckConstraint(
            "content_sha256 ~ '^[0-9a-f]{64}$'",
            name="knowledge_chunk_sha256_valid",
        ),
    )

    chunk_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    document_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("decision_support.knowledge_documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    page_start: Mapped[int] = mapped_column(Integer, nullable=False)
    page_end: Mapped[int] = mapped_column(Integer, nullable=False)
    section: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    crops: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    factors: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    search_vector: Mapped[str] = mapped_column(
        TSVECTOR,
        Computed("to_tsvector('simple'::regconfig, content)", persisted=True),
        nullable=False,
    )


class EmbeddingIndexRecord(Base):
    __tablename__ = "embedding_indexes"
    __table_args__ = (
        UniqueConstraint(
            "provider",
            "model",
            "dimensions",
            "index_version",
            name="uq_embedding_index_identity",
        ),
        CheckConstraint("dimensions > 0", name="embedding_index_dimensions_positive"),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    model: Mapped[str] = mapped_column(String(160), nullable=False)
    dimensions: Mapped[int] = mapped_column(Integer, nullable=False)
    index_version: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class KnowledgeEmbeddingRecord(Base):
    __tablename__ = "knowledge_embeddings"

    chunk_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("decision_support.knowledge_chunks.chunk_id", ondelete="CASCADE"),
        primary_key=True,
    )
    embedding_index_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("decision_support.embedding_indexes.id", ondelete="RESTRICT"),
        primary_key=True,
    )
    vector: Mapped[list[float]] = mapped_column(ARRAY(Float), nullable=False)
    input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    request_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class RetrievalRunRecord(Base):
    __tablename__ = "retrieval_runs"
    __table_args__ = (
        CheckConstraint(
            "retrieval_status IN ('available', 'insufficient_evidence', 'unavailable')",
            name="retrieval_run_status_supported",
        ),
        CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="retrieval_run_water_regime_supported",
        ),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    evaluation_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    crop_id: Mapped[str] = mapped_column(String(120), nullable=False)
    water_regime: Mapped[str] = mapped_column(String(16), nullable=False)
    limiting_factors: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    retrieval_status: Mapped[str] = mapped_column(String(32), nullable=False)
    query: Mapped[str] = mapped_column(Text, nullable=False)
    corpus_version: Mapped[str] = mapped_column(String(64), nullable=False)
    retrieval_version: Mapped[str] = mapped_column(String(64), nullable=False)
    embedding_index_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("decision_support.embedding_indexes.id", ondelete="RESTRICT"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class RetrievalHitRecord(Base):
    __tablename__ = "retrieval_hits"

    retrieval_run_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("decision_support.retrieval_runs.id", ondelete="CASCADE"),
        primary_key=True,
    )
    evidence_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    chunk_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("decision_support.knowledge_chunks.chunk_id", ondelete="RESTRICT"),
        nullable=False,
    )
    final_rank: Mapped[int] = mapped_column(Integer, nullable=False)
    lexical_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    vector_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fused_score: Mapped[float] = mapped_column(Float, nullable=False)


class RecommendationRunRecord(Base):
    __tablename__ = "recommendation_runs"
    __table_args__ = (
        CheckConstraint(
            "status IN ('succeeded', 'insufficient_evidence', 'failed')",
            name="recommendation_run_status_supported",
        ),
        CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="rec_run_water_regime_supported",
        ),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    evaluation_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    crop_id: Mapped[str] = mapped_column(String(120), nullable=False)
    water_regime: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(64), nullable=False)
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    model: Mapped[str] = mapped_column(String(160), nullable=False)
    response_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    corpus_version: Mapped[str] = mapped_column(String(64), nullable=False)
    retrieval_version: Mapped[str] = mapped_column(String(64), nullable=False)
    embedding_index_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("decision_support.embedding_indexes.id", ondelete="RESTRICT"),
        nullable=False,
    )
    retrieval_run_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("decision_support.retrieval_runs.id", ondelete="RESTRICT"),
        nullable=False,
    )
    cache_key: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    structured_output: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RecommendationGenerationAttemptRecord(Base):
    """Durable record of a provider generation attempt, including failed calls."""

    __tablename__ = "recommendation_generation_attempts"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    owner_user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    evaluation_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RecommendationCitationRecord(Base):
    __tablename__ = "recommendation_citations"

    recommendation_run_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "decision_support.recommendation_runs.id",
            name="fk_rec_citations_run",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    evidence_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    chunk_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("decision_support.knowledge_chunks.chunk_id", ondelete="RESTRICT"),
        nullable=False,
    )
