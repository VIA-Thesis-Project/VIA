"""PostgreSQL integration coverage for agronomic knowledge RAG persistence."""

from __future__ import annotations

import hashlib
import os
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, text

from database_test_support import require_test_database_url
from via_backend.contexts.decision_support.application.knowledge_models import (
    CorpusSource,
    EmbeddingIndex,
    EvidenceItem,
    KnowledgeChunk,
    KnowledgeDocument,
    KnowledgeDocumentStatus,
    RecommendationItem,
    RecommendationRun,
    RecommendationStatus,
    RetrievalStatus,
    RetrievedKnowledge,
    StructuredRecommendation,
)
from via_backend.contexts.decision_support.infrastructure import (
    PostgreSQLKnowledgeCorpusRepository,
    PostgreSQLRecommendationRepository,
)
from via_backend.infrastructure import SessionFactory, create_database

pytestmark = pytest.mark.integration
BACKEND_ROOT = Path(__file__).parents[1]


@pytest.fixture(scope="session")
def database() -> Iterator[tuple[Engine, SessionFactory]]:
    database_url = require_test_database_url()
    previous = os.environ.get("VIA_DATABASE_URL")
    os.environ["VIA_DATABASE_URL"] = database_url
    try:
        command.upgrade(Config(str(BACKEND_ROOT / "alembic.ini")), "head")
    finally:
        if previous is None:
            os.environ.pop("VIA_DATABASE_URL", None)
        else:
            os.environ["VIA_DATABASE_URL"] = previous

    engine, sessions = create_database(database_url)
    yield engine, sessions
    engine.dispose()


@pytest.fixture(autouse=True)
def clean_knowledge_tables(database: tuple[Engine, SessionFactory]) -> None:
    engine, _ = database
    with engine.begin() as connection:
        connection.execute(
            text(
                "TRUNCATE TABLE "
                "decision_support.recommendation_citations, "
                "decision_support.recommendation_runs, "
                "decision_support.retrieval_hits, "
                "decision_support.retrieval_runs, "
                "decision_support.knowledge_embeddings, "
                "decision_support.knowledge_chunks, "
                "decision_support.knowledge_documents, "
                "decision_support.embedding_indexes CASCADE"
            )
        )


def _source(source_id: str = "fao-water") -> CorpusSource:
    return CorpusSource(
        source_id=source_id,
        organization="FAO",
        title="Agronomic guidance",
        language="en",
        source_type="manual",
        source_roles=("methodology",),
        relative_path=f"fao/{source_id}.pdf",
        source_reference=f"fao/{source_id}.pdf",
    )


def _index() -> EmbeddingIndex:
    return EmbeddingIndex(
        index_id=uuid4(),
        provider="test",
        model="test-embedding",
        dimensions=3,
        index_version="test-v1",
        created_at=datetime.now(UTC),
    )


def _chunk(
    chunk_id: str,
    content: str,
    *,
    crops: tuple[str, ...] = (),
    factors: tuple[str, ...] = (),
    sequence: int = 0,
) -> KnowledgeChunk:
    return KnowledgeChunk(
        chunk_id=chunk_id,
        sequence=sequence,
        page_start=sequence + 1,
        page_end=sequence + 1,
        section=None,
        content=content,
        content_sha256=hashlib.sha256(content.encode("utf-8")).hexdigest(),
        crops=crops,
        factors=factors,
    )


def _save_document(
    repository: PostgreSQLKnowledgeCorpusRepository,
    *,
    chunks: tuple[KnowledgeChunk, ...],
    index: EmbeddingIndex,
) -> KnowledgeDocument:
    document = KnowledgeDocument(
        document_id=uuid4(),
        source=_source(),
        corpus_version="test-corpus-v1",
        source_sha256="a" * 64,
        status=KnowledgeDocumentStatus.READY,
        ingested_at=datetime.now(UTC),
        page_count=len(chunks),
        pages_extracted=len(chunks),
        warnings=(),
    )
    repository.save_document(
        document,
        chunks,
        index,
        {chunk.chunk_id: (1.0, 0.0, 0.0) for chunk in chunks},
        embedding_input_tokens=12,
        embedding_request_count=1,
    )
    return document


def test_migration_0015_schema_exists(database: tuple[Engine, SessionFactory]) -> None:
    engine, _ = database
    expected = {
        "knowledge_documents",
        "knowledge_chunks",
        "embedding_indexes",
        "knowledge_embeddings",
        "retrieval_runs",
        "retrieval_hits",
        "recommendation_runs",
        "recommendation_citations",
    }
    with engine.connect() as connection:
        rows = connection.execute(
            text(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname = 'decision_support' "
                "AND tablename = ANY(:tables)"
            ),
            {"tables": list(expected)},
        ).scalars()
        assert set(rows) == expected


def test_document_persistence_is_idempotent_and_filtering_isolated(
    database: tuple[Engine, SessionFactory],
) -> None:
    engine, sessions = database
    repository = PostgreSQLKnowledgeCorpusRepository(sessions)
    index = repository.ensure_embedding_index(_index())
    chunks = (
        _chunk(
            "maize-precip",
            "seasonal rainfall deficit management for maize",
            crops=("maize",),
            factors=("precipitation",),
        ),
        _chunk(
            "avocado-precip",
            "seasonal rainfall deficit management for avocado",
            crops=("avocado",),
            factors=("precipitation",),
            sequence=1,
        ),
        _chunk(
            "generic",
            "general rainfall deficit management guidance",
            sequence=2,
        ),
        _chunk(
            "maize-soildepth",
            "effective soil depth and root restriction",
            crops=("maize",),
            factors=("parameter_soildepth",),
            sequence=3,
        ),
    )
    document = _save_document(repository, chunks=chunks, index=index)
    repository.save_document(
        document,
        chunks,
        index,
        {chunk.chunk_id: (1.0, 0.0, 0.0) for chunk in chunks},
        embedding_input_tokens=12,
        embedding_request_count=1,
    )

    restored = repository.find_document(
        document.source.source_id,
        document.source_sha256,
        document.corpus_version,
    )
    assert restored == document

    lexical = repository.lexical_search(
        "rainfall deficit",
        "maize",
        ("precipitation",),
        10,
    )
    assert {hit.chunk.chunk_id for hit in lexical} == {"maize-precip", "generic"}

    vectors = repository.vector_candidates("maize", ("precipitation",), index.index_id)
    assert {candidate.chunk.chunk_id for candidate in vectors} == {
        "maize-precip",
        "generic",
    }

    with engine.connect() as connection:
        assert connection.execute(
            text(
                "SELECT count(*) FROM decision_support.knowledge_documents "
                "WHERE id = :document_id"
            ),
            {"document_id": document.document_id},
        ).scalar_one() == 1
        assert connection.execute(
            text(
                "SELECT count(*) FROM decision_support.knowledge_chunks "
                "WHERE document_id = :document_id"
            ),
            {"document_id": document.document_id},
        ).scalar_one() == len(chunks)


def test_retrieval_and_recommendation_traces_persist_closed_citations(
    database: tuple[Engine, SessionFactory],
) -> None:
    engine, sessions = database
    knowledge_repository = PostgreSQLKnowledgeCorpusRepository(sessions)
    recommendation_repository = PostgreSQLRecommendationRepository(sessions)
    index = knowledge_repository.ensure_embedding_index(_index())
    chunk = _chunk(
        "maize-precip",
        "seasonal rainfall deficit management for maize",
        crops=("maize",),
        factors=("precipitation",),
    )
    _save_document(knowledge_repository, chunks=(chunk,), index=index)

    evaluation_id = uuid4()
    retrieval = RetrievedKnowledge(
        retrieval_run_id=uuid4(),
        evaluation_id=evaluation_id,
        crop_id="maize",
        water_regime="rainfed",
        limiting_factors=("precipitation",),
        retrieval_status=RetrievalStatus.AVAILABLE,
        query="maize rainfall deficit",
        corpus_version="test-corpus-v1",
        retrieval_version="hybrid-rrf-v1",
        embedding_index=index,
        evidence=(
            EvidenceItem(
                evidence_id="SOURCE_1",
                chunk_id=chunk.chunk_id,
                organization="FAO",
                title="Agronomic guidance",
                source_roles=("methodology",),
                page_start=1,
                page_end=1,
                section=None,
                content=chunk.content,
                source_reference="fao/fao-water.pdf",
                lexical_rank=1,
                vector_rank=1,
                fused_score=1.0,
            ),
        ),
    )
    knowledge_repository.persist_retrieval(retrieval)

    structured = StructuredRecommendation(
        summary="Rainfall is a limiting factor.",
        observations=("The rainfed scenario is water-limited.",),
        scenario_interpretation="The scientific evaluation remains authoritative.",
        recommendations=(
            RecommendationItem(
                text="Review water-management options.",
                rationale="The retrieved source addresses rainfall deficit management.",
                citation_ids=("SOURCE_1",),
            ),
        ),
        uncertainties=("Actual irrigation availability is unknown.",),
        citation_ids=("SOURCE_1",),
    )
    run = RecommendationRun(
        run_id=uuid4(),
        evaluation_id=evaluation_id,
        crop_id="maize",
        water_regime="rainfed",
        status=RecommendationStatus.SUCCEEDED,
        prompt_version="agronomic-recommendation-v1",
        provider="test",
        model="test-model",
        response_id="response-1",
        corpus_version="test-corpus-v1",
        retrieval_version="hybrid-rrf-v1",
        embedding_index_id=index.index_id,
        cache_key="cache-key",
        recommendation=structured,
        failure_reason=None,
        input_tokens=20,
        output_tokens=10,
        created_at=datetime.now(UTC),
    )
    recommendation_repository.save(run, retrieval)

    assert recommendation_repository.find_succeeded_by_cache_key("cache-key") == run
    assert recommendation_repository.list_for_evaluation(evaluation_id) == (run,)

    with engine.connect() as connection:
        persisted_retrieval_id = connection.execute(
            text(
                "SELECT retrieval_run_id FROM decision_support.recommendation_runs "
                "WHERE id = :run_id"
            ),
            {"run_id": run.run_id},
        ).scalar_one()
        citations = connection.execute(
            text(
                "SELECT evidence_id, chunk_id "
                "FROM decision_support.recommendation_citations "
                "WHERE recommendation_run_id = :run_id"
            ),
            {"run_id": run.run_id},
        ).all()

    assert persisted_retrieval_id == retrieval.retrieval_run_id
    assert citations == [("SOURCE_1", chunk.chunk_id)]
