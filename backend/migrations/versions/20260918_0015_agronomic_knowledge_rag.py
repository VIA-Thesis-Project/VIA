"""Persist agronomic knowledge, retrieval traces, and recommendations.

Revision ID: 20260918_0015
Revises: 20260918_0014
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260918_0015"
down_revision: str | None = "20260918_0014"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "decision_support"


def upgrade() -> None:
    op.create_table(
        "knowledge_documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_id", sa.String(length=160), nullable=False),
        sa.Column("organization", sa.String(length=200), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("language", sa.String(length=32), nullable=False),
        sa.Column("country", sa.String(length=16), nullable=True),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("source_roles", postgresql.JSONB(), nullable=False),
        sa.Column("relative_path", sa.Text(), nullable=False),
        sa.Column("source_reference", sa.Text(), nullable=True),
        sa.Column("crops", postgresql.JSONB(), nullable=False),
        sa.Column("factors", postgresql.JSONB(), nullable=False),
        sa.Column("source_sha256", sa.String(length=64), nullable=False),
        sa.Column("corpus_version", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("page_count", sa.Integer(), nullable=False),
        sa.Column("pages_extracted", sa.Integer(), nullable=False),
        sa.Column("warnings", postgresql.JSONB(), nullable=False),
        sa.Column("embedding_input_tokens", sa.Integer(), nullable=True),
        sa.Column("embedding_request_count", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "status IN ('ready', 'needs_ocr', 'failed')",
            name="knowledge_document_status_supported",
        ),
        sa.CheckConstraint(
            "source_sha256 ~ '^[0-9a-f]{64}$'",
            name="knowledge_document_sha256_valid",
        ),
        sa.CheckConstraint(
            "relative_path <> '' AND relative_path = btrim(relative_path)",
            name="knowledge_document_relative_path_valid",
        ),
        sa.CheckConstraint(
            "page_count >= 0 AND pages_extracted >= 0 AND pages_extracted <= page_count",
            name="knowledge_document_page_counts_valid",
        ),
        sa.CheckConstraint(
            "embedding_request_count >= 0",
            name="knowledge_document_embedding_requests_nonnegative",
        ),
        sa.CheckConstraint(
            "jsonb_typeof(source_roles) = 'array' AND jsonb_typeof(crops) = 'array' "
            "AND jsonb_typeof(factors) = 'array' AND jsonb_typeof(warnings) = 'array'",
            name="knowledge_document_json_arrays",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_knowledge_documents"),
        sa.UniqueConstraint(
            "source_id",
            "source_sha256",
            "corpus_version",
            name="uq_knowledge_document_version",
        ),
        schema=SCHEMA,
    )

    op.create_table(
        "knowledge_chunks",
        sa.Column("chunk_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("page_start", sa.Integer(), nullable=False),
        sa.Column("page_end", sa.Integer(), nullable=False),
        sa.Column("section", sa.Text(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_sha256", sa.String(length=64), nullable=False),
        sa.Column("crops", postgresql.JSONB(), nullable=False),
        sa.Column("factors", postgresql.JSONB(), nullable=False),
        sa.Column(
            "search_vector",
            postgresql.TSVECTOR(),
            sa.Computed("to_tsvector('simple'::regconfig, content)", persisted=True),
            nullable=False,
        ),
        sa.CheckConstraint("sequence >= 0", name="knowledge_chunk_sequence_nonnegative"),
        sa.CheckConstraint("page_start >= 1", name="knowledge_chunk_page_start_positive"),
        sa.CheckConstraint(
            "page_end >= page_start", name="knowledge_chunk_page_order_valid"
        ),
        sa.CheckConstraint(
            "content_sha256 ~ '^[0-9a-f]{64}$'",
            name="knowledge_chunk_sha256_valid",
        ),
        sa.CheckConstraint(
            "jsonb_typeof(crops) = 'array' AND jsonb_typeof(factors) = 'array'",
            name="knowledge_chunk_json_arrays",
        ),
        sa.ForeignKeyConstraint(
            ["document_id"],
            [f"{SCHEMA}.knowledge_documents.id"],
            name="fk_knowledge_chunks_document_id_knowledge_documents",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("chunk_id", name="pk_knowledge_chunks"),
        sa.UniqueConstraint(
            "document_id", "sequence", name="uq_knowledge_chunk_sequence"
        ),
        schema=SCHEMA,
    )
    op.create_index(
        "ix_knowledge_chunks_search_vector",
        "knowledge_chunks",
        ["search_vector"],
        unique=False,
        schema=SCHEMA,
        postgresql_using="gin",
    )

    op.create_table(
        "embedding_indexes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("model", sa.String(length=160), nullable=False),
        sa.Column("dimensions", sa.Integer(), nullable=False),
        sa.Column("index_version", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("dimensions > 0", name="embedding_index_dimensions_positive"),
        sa.PrimaryKeyConstraint("id", name="pk_embedding_indexes"),
        sa.UniqueConstraint(
            "provider",
            "model",
            "dimensions",
            "index_version",
            name="uq_embedding_index_identity",
        ),
        schema=SCHEMA,
    )

    op.create_table(
        "knowledge_embeddings",
        sa.Column("chunk_id", sa.String(length=64), nullable=False),
        sa.Column("embedding_index_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("vector", postgresql.ARRAY(sa.Float()), nullable=False),
        sa.Column("input_tokens", sa.Integer(), nullable=True),
        sa.Column("request_count", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("request_count >= 0", name="knowledge_embedding_requests_nonnegative"),
        sa.CheckConstraint(
            "array_length(vector, 1) > 0",
            name="knowledge_embedding_vector_nonempty",
        ),
        sa.ForeignKeyConstraint(
            ["chunk_id"],
            [f"{SCHEMA}.knowledge_chunks.chunk_id"],
            name="fk_knowledge_embeddings_chunk_id_knowledge_chunks",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["embedding_index_id"],
            [f"{SCHEMA}.embedding_indexes.id"],
            name="fk_knowledge_embeddings_embedding_index_id_embedding_indexes",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "chunk_id", "embedding_index_id", name="pk_knowledge_embeddings"
        ),
        schema=SCHEMA,
    )

    op.create_table(
        "retrieval_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("crop_id", sa.String(length=120), nullable=False),
        sa.Column("water_regime", sa.String(length=16), nullable=False),
        sa.Column("limiting_factors", postgresql.JSONB(), nullable=False),
        sa.Column("retrieval_status", sa.String(length=32), nullable=False),
        sa.Column("query", sa.Text(), nullable=False),
        sa.Column("corpus_version", sa.String(length=64), nullable=False),
        sa.Column("retrieval_version", sa.String(length=64), nullable=False),
        sa.Column("embedding_index_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "retrieval_status IN ('available', 'insufficient_evidence', 'unavailable')",
            name="retrieval_run_status_supported",
        ),
        sa.CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="retrieval_run_water_regime_supported",
        ),
        sa.CheckConstraint(
            "jsonb_typeof(limiting_factors) = 'array'",
            name="retrieval_run_limiting_factors_array",
        ),
        sa.ForeignKeyConstraint(
            ["embedding_index_id"],
            [f"{SCHEMA}.embedding_indexes.id"],
            name="fk_retrieval_runs_embedding_index_id_embedding_indexes",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_retrieval_runs"),
        schema=SCHEMA,
    )
    op.create_index(
        "ix_retrieval_runs_evaluation_id",
        "retrieval_runs",
        ["evaluation_id"],
        unique=False,
        schema=SCHEMA,
    )

    op.create_table(
        "retrieval_hits",
        sa.Column("retrieval_run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("evidence_id", sa.String(length=32), nullable=False),
        sa.Column("chunk_id", sa.String(length=64), nullable=False),
        sa.Column("final_rank", sa.Integer(), nullable=False),
        sa.Column("lexical_rank", sa.Integer(), nullable=True),
        sa.Column("vector_rank", sa.Integer(), nullable=True),
        sa.Column("fused_score", sa.Float(), nullable=False),
        sa.CheckConstraint("final_rank >= 1", name="retrieval_hit_final_rank_positive"),
        sa.ForeignKeyConstraint(
            ["retrieval_run_id"],
            [f"{SCHEMA}.retrieval_runs.id"],
            name="fk_retrieval_hits_retrieval_run_id_retrieval_runs",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["chunk_id"],
            [f"{SCHEMA}.knowledge_chunks.chunk_id"],
            name="fk_retrieval_hits_chunk_id_knowledge_chunks",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "retrieval_run_id", "evidence_id", name="pk_retrieval_hits"
        ),
        sa.UniqueConstraint(
            "retrieval_run_id", "final_rank", name="uq_retrieval_hit_final_rank"
        ),
        schema=SCHEMA,
    )

    op.create_table(
        "recommendation_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("crop_id", sa.String(length=120), nullable=False),
        sa.Column("water_regime", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("prompt_version", sa.String(length=64), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("model", sa.String(length=160), nullable=False),
        sa.Column("response_id", sa.String(length=200), nullable=True),
        sa.Column("corpus_version", sa.String(length=64), nullable=False),
        sa.Column("retrieval_version", sa.String(length=64), nullable=False),
        sa.Column("embedding_index_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("retrieval_run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("cache_key", sa.String(length=64), nullable=False),
        sa.Column("structured_output", postgresql.JSONB(), nullable=True),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        sa.Column("input_tokens", sa.Integer(), nullable=True),
        sa.Column("output_tokens", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "status IN ('succeeded', 'insufficient_evidence', 'failed')",
            name="recommendation_run_status_supported",
        ),
        sa.CheckConstraint(
            "water_regime IN ('rainfed', 'irrigated')",
            name="ck_recommendation_runs_rec_run_water_regime_supported",
        ),
        sa.CheckConstraint(
            "(status = 'succeeded' AND structured_output IS NOT NULL AND failure_reason IS NULL) "
            "OR (status <> 'succeeded' AND structured_output IS NULL "
            "AND failure_reason IS NOT NULL)",
            name="recommendation_run_output_matches_status",
        ),
        sa.ForeignKeyConstraint(
            ["embedding_index_id"],
            [f"{SCHEMA}.embedding_indexes.id"],
            name="fk_recommendation_runs_embedding_index_id_embedding_indexes",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["retrieval_run_id"],
            [f"{SCHEMA}.retrieval_runs.id"],
            name="fk_recommendation_runs_retrieval_run_id_retrieval_runs",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_recommendation_runs"),
        schema=SCHEMA,
    )
    op.create_index(
        "ix_recommendation_runs_cache_key",
        "recommendation_runs",
        ["cache_key"],
        unique=False,
        schema=SCHEMA,
    )
    op.create_index(
        "ix_recommendation_runs_evaluation_id",
        "recommendation_runs",
        ["evaluation_id"],
        unique=False,
        schema=SCHEMA,
    )

    op.create_table(
        "recommendation_citations",
        sa.Column("recommendation_run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("evidence_id", sa.String(length=32), nullable=False),
        sa.Column("chunk_id", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(
            ["recommendation_run_id"],
            [f"{SCHEMA}.recommendation_runs.id"],
            name="fk_rec_citations_run",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["chunk_id"],
            [f"{SCHEMA}.knowledge_chunks.chunk_id"],
            name="fk_recommendation_citations_chunk_id_knowledge_chunks",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "recommendation_run_id", "evidence_id", name="pk_recommendation_citations"
        ),
        schema=SCHEMA,
    )


def downgrade() -> None:
    op.drop_table("recommendation_citations", schema=SCHEMA)
    op.drop_index(
        "ix_recommendation_runs_evaluation_id",
        table_name="recommendation_runs",
        schema=SCHEMA,
    )
    op.drop_index(
        "ix_recommendation_runs_cache_key",
        table_name="recommendation_runs",
        schema=SCHEMA,
    )
    op.drop_table("recommendation_runs", schema=SCHEMA)
    op.drop_table("retrieval_hits", schema=SCHEMA)
    op.drop_index("ix_retrieval_runs_evaluation_id", table_name="retrieval_runs", schema=SCHEMA)
    op.drop_table("retrieval_runs", schema=SCHEMA)
    op.drop_table("knowledge_embeddings", schema=SCHEMA)
    op.drop_table("embedding_indexes", schema=SCHEMA)
    op.drop_index("ix_knowledge_chunks_search_vector", table_name="knowledge_chunks", schema=SCHEMA)
    op.drop_table("knowledge_chunks", schema=SCHEMA)
    op.drop_table("knowledge_documents", schema=SCHEMA)
