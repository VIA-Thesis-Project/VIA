"""PostgreSQL repositories for Decision Support."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete, func, or_, select, update
from sqlalchemy.dialects.postgresql import insert as postgresql_insert
from sqlalchemy.sql.elements import ColumnElement

from via_backend.infrastructure.database import SessionFactory

from ..application.errors import (
    DefaultViabilityPolicyConflictError,
    DefaultViabilityPolicyNotConfiguredError,
    ViabilityPolicyVersionNotFoundError,
)
from ..application.knowledge_models import (
    CorpusSource,
    EmbeddingIndex,
    KnowledgeChunk,
    KnowledgeDocument,
    KnowledgeDocumentStatus,
    LexicalSearchHit,
    RecommendationItem,
    RecommendationRun,
    RecommendationStatus,
    RetrievedKnowledge,
    StoredChunk,
    StructuredRecommendation,
    VectorSearchCandidate,
)
from ..domain.errors import PolicyVersionConflictError
from ..domain.models import (
    PolicyReference,
    ViabilityPolicyConfiguration,
    ViabilityPolicySnapshot,
)
from .orm import (
    DefaultViabilityPolicyRecord,
    EmbeddingIndexRecord,
    KnowledgeChunkRecord,
    KnowledgeDocumentRecord,
    KnowledgeEmbeddingRecord,
    RecommendationCitationRecord,
    RecommendationRunRecord,
    RetrievalHitRecord,
    RetrievalRunRecord,
    ViabilityPolicyVersionRecord,
)


class PostgreSQLViabilityPolicyRepository:
    """Durable adapter for immutable viability-policy versions."""

    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def add(self, policy: ViabilityPolicySnapshot) -> None:
        reference = policy.reference
        identity = (
            reference.identifier,
            reference.version,
        )

        with self._sessions.begin() as session:
            statement = (
                postgresql_insert(ViabilityPolicyVersionRecord)
                .values(
                    identifier=reference.identifier,
                    version=reference.version,
                    conditional_from=policy.configuration.conditional_from,
                    viable_from=policy.configuration.viable_from,
                )
                .on_conflict_do_nothing(
                    index_elements=[
                        ViabilityPolicyVersionRecord.identifier,
                        ViabilityPolicyVersionRecord.version,
                    ]
                )
                .returning(ViabilityPolicyVersionRecord.identifier)
            )
            inserted_identifier = session.execute(statement).scalar_one_or_none()

            if inserted_identifier is not None:
                return

            existing = session.get(
                ViabilityPolicyVersionRecord,
                identity,
            )
            if existing is None:
                raise RuntimeError(
                    "Policy registration conflicted, but the persisted policy "
                    f"{reference.identifier}:{reference.version} could not be restored."
                )

            if _snapshot_from_record(existing) != policy:
                raise PolicyVersionConflictError(
                    "Policy reference "
                    f"{reference.identifier}:{reference.version} "
                    "already exists with different thresholds."
                )

    def get(
        self,
        reference: PolicyReference,
    ) -> ViabilityPolicySnapshot | None:
        with self._sessions() as session:
            record = session.get(
                ViabilityPolicyVersionRecord,
                (
                    reference.identifier,
                    reference.version,
                ),
            )

            if record is None:
                return None

            return _snapshot_from_record(record)


def _snapshot_from_record(
    record: ViabilityPolicyVersionRecord,
) -> ViabilityPolicySnapshot:
    return ViabilityPolicySnapshot(
        reference=PolicyReference(
            identifier=record.identifier,
            version=record.version,
        ),
        configuration=ViabilityPolicyConfiguration(
            conditional_from=record.conditional_from,
            viable_from=record.viable_from,
        ),
    )


_DEFAULT_POLICY_SLOT = "default"


class PostgreSQLDefaultViabilityPolicyStore:
    """Persist and resolve the singleton VIA default-policy pointer."""

    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def get_default_viability_policy(
        self,
    ) -> ViabilityPolicySnapshot:
        with self._sessions() as session:
            pointer = session.get(
                DefaultViabilityPolicyRecord,
                _DEFAULT_POLICY_SLOT,
            )

            if pointer is None:
                raise DefaultViabilityPolicyNotConfiguredError(
                    "No default viability policy is configured."
                )

            policy_record = session.get(
                ViabilityPolicyVersionRecord,
                (
                    pointer.policy_identifier,
                    pointer.policy_version,
                ),
            )

            if policy_record is None:
                raise RuntimeError(
                    "Default viability-policy pointer references "
                    "missing persisted policy data."
                )

            return _snapshot_from_record(policy_record)

    def set_default_viability_policy(
        self,
        reference: PolicyReference,
        *,
        expected_current: PolicyReference | None,
    ) -> None:
        identity = (
            reference.identifier,
            reference.version,
        )

        with self._sessions.begin() as session:
            policy_record = session.get(
                ViabilityPolicyVersionRecord,
                identity,
            )

            if policy_record is None:
                raise ViabilityPolicyVersionNotFoundError(
                    "Cannot select missing viability policy "
                    f"{reference.identifier}:{reference.version}."
                )

            if expected_current is None:
                statement = (
                    postgresql_insert(DefaultViabilityPolicyRecord)
                    .values(
                        slot=_DEFAULT_POLICY_SLOT,
                        policy_identifier=reference.identifier,
                        policy_version=reference.version,
                    )
                    .on_conflict_do_nothing(
                        index_elements=[DefaultViabilityPolicyRecord.slot]
                    )
                    .returning(DefaultViabilityPolicyRecord.slot)
                )
            else:
                statement = (
                    update(DefaultViabilityPolicyRecord)
                    .where(
                        DefaultViabilityPolicyRecord.slot == _DEFAULT_POLICY_SLOT,
                        DefaultViabilityPolicyRecord.policy_identifier
                        == expected_current.identifier,
                        DefaultViabilityPolicyRecord.policy_version
                        == expected_current.version,
                    )
                    .values(
                        policy_identifier=reference.identifier,
                        policy_version=reference.version,
                        selected_at=datetime.now(UTC),
                    )
                    .returning(DefaultViabilityPolicyRecord.slot)
                )

            changed_slot = session.execute(statement).scalar_one_or_none()
            if changed_slot is not None:
                return

            pointer = session.get(
                DefaultViabilityPolicyRecord,
                _DEFAULT_POLICY_SLOT,
            )
            if pointer is not None and (
                pointer.policy_identifier == reference.identifier
                and pointer.policy_version == reference.version
            ):
                return

            raise DefaultViabilityPolicyConflictError(
                "Default viability-policy pointer changed before the expected update."
            )


class PostgreSQLKnowledgeCorpusRepository:
    """Durable corpus, embedding, and retrieval-trace adapter."""

    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def find_document(
        self,
        source_id: str,
        source_sha256: str,
        corpus_version: str,
    ) -> KnowledgeDocument | None:
        with self._sessions() as session:
            record = session.execute(
                select(KnowledgeDocumentRecord).where(
                    KnowledgeDocumentRecord.source_id == source_id,
                    KnowledgeDocumentRecord.source_sha256 == source_sha256,
                    KnowledgeDocumentRecord.corpus_version == corpus_version,
                )
            ).scalar_one_or_none()
            return None if record is None else _knowledge_document_from_record(record)

    def ensure_embedding_index(self, index: EmbeddingIndex) -> EmbeddingIndex:
        with self._sessions.begin() as session:
            statement = (
                postgresql_insert(EmbeddingIndexRecord)
                .values(
                    id=index.index_id,
                    provider=index.provider,
                    model=index.model,
                    dimensions=index.dimensions,
                    index_version=index.index_version,
                    created_at=index.created_at,
                )
                .on_conflict_do_nothing(
                    index_elements=[
                        EmbeddingIndexRecord.provider,
                        EmbeddingIndexRecord.model,
                        EmbeddingIndexRecord.dimensions,
                        EmbeddingIndexRecord.index_version,
                    ]
                )
            )
            session.execute(statement)
            record = session.execute(
                select(EmbeddingIndexRecord).where(
                    EmbeddingIndexRecord.provider == index.provider,
                    EmbeddingIndexRecord.model == index.model,
                    EmbeddingIndexRecord.dimensions == index.dimensions,
                    EmbeddingIndexRecord.index_version == index.index_version,
                )
            ).scalar_one()
            return _embedding_index_from_record(record)

    def reusable_embeddings(
        self,
        content_hashes: tuple[str, ...],
        embedding_index_id: UUID,
    ) -> dict[str, tuple[float, ...]]:
        if not content_hashes:
            return {}
        with self._sessions() as session:
            rows = session.execute(
                select(
                    KnowledgeChunkRecord.content_sha256,
                    KnowledgeEmbeddingRecord.vector,
                )
                .join(
                    KnowledgeEmbeddingRecord,
                    KnowledgeEmbeddingRecord.chunk_id == KnowledgeChunkRecord.chunk_id,
                )
                .where(
                    KnowledgeEmbeddingRecord.embedding_index_id == embedding_index_id,
                    KnowledgeChunkRecord.content_sha256.in_(content_hashes),
                )
                .order_by(KnowledgeChunkRecord.chunk_id)
            ).all()
        reusable: dict[str, tuple[float, ...]] = {}
        for content_sha256, vector in rows:
            reusable.setdefault(content_sha256, tuple(float(value) for value in vector))
        return reusable

    def save_document(
        self,
        document: KnowledgeDocument,
        chunks: tuple[KnowledgeChunk, ...],
        embedding_index: EmbeddingIndex,
        embeddings: dict[str, tuple[float, ...]],
        embedding_input_tokens: int | None,
        embedding_request_count: int,
    ) -> None:
        if document.status is KnowledgeDocumentStatus.READY:
            missing = [chunk.chunk_id for chunk in chunks if chunk.chunk_id not in embeddings]
            if missing:
                raise ValueError("READY knowledge documents require an embedding for every chunk.")

        with self._sessions.begin() as session:
            existing = session.get(KnowledgeDocumentRecord, document.document_id)
            if existing is not None and existing.status == KnowledgeDocumentStatus.READY.value:
                return

            values = _knowledge_document_values(
                document,
                embedding_input_tokens=embedding_input_tokens,
                embedding_request_count=embedding_request_count,
            )
            if existing is None:
                session.add(KnowledgeDocumentRecord(**values))
                session.flush()
            else:
                for name, value in values.items():
                    if name != "id":
                        setattr(existing, name, value)
                session.execute(
                    delete(KnowledgeChunkRecord).where(
                        KnowledgeChunkRecord.document_id == document.document_id
                    )
                )

            for chunk in chunks:
                session.add(
                    KnowledgeChunkRecord(
                        chunk_id=chunk.chunk_id,
                        document_id=document.document_id,
                        sequence=chunk.sequence,
                        page_start=chunk.page_start,
                        page_end=chunk.page_end,
                        section=chunk.section,
                        content=chunk.content,
                        content_sha256=chunk.content_sha256,
                        crops=list(chunk.crops),
                        factors=list(chunk.factors),
                    )
                )
            session.flush()
            for chunk in chunks:
                session.add(
                    KnowledgeEmbeddingRecord(
                        chunk_id=chunk.chunk_id,
                        embedding_index_id=embedding_index.index_id,
                        vector=list(embeddings[chunk.chunk_id]),
                        input_tokens=None,
                        request_count=0,
                    )
                )

    def lexical_search(
        self,
        query: str,
        crop_id: str,
        factor_codes: tuple[str, ...],
        limit: int,
    ) -> tuple[LexicalSearchHit, ...]:
        if not query or limit < 1:
            return ()
        tsquery = func.websearch_to_tsquery("simple", query)
        score = func.ts_rank_cd(KnowledgeChunkRecord.search_vector, tsquery)
        filters = _knowledge_metadata_filters(crop_id, factor_codes)
        with self._sessions() as session:
            rows = session.execute(
                select(KnowledgeChunkRecord, KnowledgeDocumentRecord, score.label("score"))
                .join(
                    KnowledgeDocumentRecord,
                    KnowledgeDocumentRecord.id == KnowledgeChunkRecord.document_id,
                )
                .where(
                    KnowledgeDocumentRecord.status == KnowledgeDocumentStatus.READY.value,
                    KnowledgeChunkRecord.search_vector.op("@@")(tsquery),
                    *filters,
                )
                .order_by(score.desc(), KnowledgeChunkRecord.chunk_id)
                .limit(limit)
            ).all()
        return tuple(
            LexicalSearchHit(
                chunk=_stored_chunk(chunk, document),
                rank=rank,
                score=float(row_score),
            )
            for rank, (chunk, document, row_score) in enumerate(rows, start=1)
        )

    def vector_candidates(
        self,
        crop_id: str,
        factor_codes: tuple[str, ...],
        embedding_index_id: UUID,
    ) -> tuple[VectorSearchCandidate, ...]:
        filters = _knowledge_metadata_filters(crop_id, factor_codes)
        with self._sessions() as session:
            rows = session.execute(
                select(
                    KnowledgeChunkRecord,
                    KnowledgeDocumentRecord,
                    KnowledgeEmbeddingRecord.vector,
                )
                .join(
                    KnowledgeDocumentRecord,
                    KnowledgeDocumentRecord.id == KnowledgeChunkRecord.document_id,
                )
                .join(
                    KnowledgeEmbeddingRecord,
                    KnowledgeEmbeddingRecord.chunk_id == KnowledgeChunkRecord.chunk_id,
                )
                .where(
                    KnowledgeDocumentRecord.status == KnowledgeDocumentStatus.READY.value,
                    KnowledgeEmbeddingRecord.embedding_index_id == embedding_index_id,
                    *filters,
                )
                .order_by(KnowledgeChunkRecord.chunk_id)
            ).all()
        return tuple(
            VectorSearchCandidate(
                chunk=_stored_chunk(chunk, document),
                vector=tuple(float(value) for value in vector),
            )
            for chunk, document, vector in rows
        )

    def persist_retrieval(self, retrieved: RetrievedKnowledge) -> None:
        with self._sessions.begin() as session:
            session.add(
                RetrievalRunRecord(
                    id=retrieved.retrieval_run_id,
                    evaluation_id=retrieved.evaluation_id,
                    crop_id=retrieved.crop_id,
                    water_regime=retrieved.water_regime,
                    limiting_factors=list(retrieved.limiting_factors),
                    retrieval_status=retrieved.retrieval_status.value,
                    query=retrieved.query,
                    corpus_version=retrieved.corpus_version,
                    retrieval_version=retrieved.retrieval_version,
                    embedding_index_id=retrieved.embedding_index.index_id,
                )
            )

            # The retrieval run is the FK parent of retrieval_hits.
            # Flush it first while keeping the whole operation atomic.
            session.flush()

            for rank, item in enumerate(retrieved.evidence, start=1):
                session.add(
                    RetrievalHitRecord(
                        retrieval_run_id=retrieved.retrieval_run_id,
                        evidence_id=item.evidence_id,
                        chunk_id=item.chunk_id,
                        final_rank=rank,
                        lexical_rank=item.lexical_rank,
                        vector_rank=item.vector_rank,
                        fused_score=item.fused_score,
                    )
                )

    def get_chunks(self, chunk_ids: tuple[str, ...]) -> tuple[StoredChunk, ...]:
        if not chunk_ids:
            return ()
        with self._sessions() as session:
            rows = session.execute(
                select(KnowledgeChunkRecord, KnowledgeDocumentRecord)
                .join(
                    KnowledgeDocumentRecord,
                    KnowledgeDocumentRecord.id == KnowledgeChunkRecord.document_id,
                )
                .where(KnowledgeChunkRecord.chunk_id.in_(chunk_ids))
            ).all()
        by_id = {chunk.chunk_id: _stored_chunk(chunk, document) for chunk, document in rows}
        return tuple(by_id[chunk_id] for chunk_id in chunk_ids if chunk_id in by_id)


class PostgreSQLRecommendationRepository:
    """Persist recommendation generations and their closed evidence citations."""

    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def find_succeeded_by_cache_key(self, cache_key: str) -> RecommendationRun | None:
        with self._sessions() as session:
            record = session.execute(
                select(RecommendationRunRecord)
                .where(
                    RecommendationRunRecord.cache_key == cache_key,
                    RecommendationRunRecord.status == RecommendationStatus.SUCCEEDED.value,
                )
                .order_by(RecommendationRunRecord.created_at.desc())
                .limit(1)
            ).scalar_one_or_none()
            return None if record is None else _recommendation_run_from_record(record)

    def save(self, run: RecommendationRun, evidence: RetrievedKnowledge) -> None:
        with self._sessions.begin() as session:
            session.add(
                RecommendationRunRecord(
                    id=run.run_id,
                    evaluation_id=run.evaluation_id,
                    crop_id=run.crop_id,
                    water_regime=run.water_regime,
                    status=run.status.value,
                    prompt_version=run.prompt_version,
                    provider=run.provider,
                    model=run.model,
                    response_id=run.response_id,
                    corpus_version=run.corpus_version,
                    retrieval_version=run.retrieval_version,
                    embedding_index_id=run.embedding_index_id,
                    retrieval_run_id=evidence.retrieval_run_id,
                    cache_key=run.cache_key,
                    structured_output=(
                        _structured_recommendation_to_dict(run.recommendation)
                        if run.recommendation is not None
                        else None
                    ),
                    failure_reason=run.failure_reason,
                    input_tokens=run.input_tokens,
                    output_tokens=run.output_tokens,
                    created_at=run.created_at,
                )
            )

            # The recommendation run is the FK parent of citations.
            session.flush()

            if run.recommendation is None:
                return

            by_evidence_id = {item.evidence_id: item for item in evidence.evidence}
            citation_ids = list(run.recommendation.citation_ids)
            for item in run.recommendation.recommendations:
                citation_ids.extend(item.citation_ids)

            for evidence_id in dict.fromkeys(citation_ids):
                item = by_evidence_id[evidence_id]
                session.add(
                    RecommendationCitationRecord(
                        recommendation_run_id=run.run_id,
                        evidence_id=evidence_id,
                        chunk_id=item.chunk_id,
                    )
                )

    def list_for_evaluation(self, evaluation_id: UUID) -> tuple[RecommendationRun, ...]:
        with self._sessions() as session:
            records = session.execute(
                select(RecommendationRunRecord)
                .where(RecommendationRunRecord.evaluation_id == evaluation_id)
                .order_by(RecommendationRunRecord.created_at.desc(), RecommendationRunRecord.id)
            ).scalars()
            return tuple(_recommendation_run_from_record(record) for record in records)


def _knowledge_document_values(
    document: KnowledgeDocument,
    *,
    embedding_input_tokens: int | None,
    embedding_request_count: int,
) -> dict[str, object]:
    source = document.source
    return {
        "id": document.document_id,
        "source_id": source.source_id,
        "organization": source.organization,
        "title": source.title,
        "language": source.language,
        "country": source.country,
        "source_type": source.source_type,
        "source_roles": list(source.source_roles),
        "relative_path": source.relative_path,
        "source_reference": source.source_reference,
        "crops": list(source.crops),
        "factors": list(source.factors),
        "source_sha256": document.source_sha256,
        "corpus_version": document.corpus_version,
        "status": document.status.value,
        "ingested_at": document.ingested_at,
        "page_count": document.page_count,
        "pages_extracted": document.pages_extracted,
        "warnings": list(document.warnings),
        "embedding_input_tokens": embedding_input_tokens,
        "embedding_request_count": embedding_request_count,
    }


def _knowledge_document_from_record(record: KnowledgeDocumentRecord) -> KnowledgeDocument:
    return KnowledgeDocument(
        document_id=record.id,
        source=CorpusSource(
            source_id=record.source_id,
            organization=record.organization,
            title=record.title,
            language=record.language,
            source_type=record.source_type,
            source_roles=tuple(record.source_roles),
            relative_path=record.relative_path,
            country=record.country,
            crops=tuple(record.crops),
            factors=tuple(record.factors),
            source_reference=record.source_reference,
        ),
        corpus_version=record.corpus_version,
        source_sha256=record.source_sha256,
        status=KnowledgeDocumentStatus(record.status),
        ingested_at=record.ingested_at,
        page_count=record.page_count,
        pages_extracted=record.pages_extracted,
        warnings=tuple(record.warnings),
    )


def _embedding_index_from_record(record: EmbeddingIndexRecord) -> EmbeddingIndex:
    return EmbeddingIndex(
        index_id=record.id,
        provider=record.provider,
        model=record.model,
        dimensions=record.dimensions,
        index_version=record.index_version,
        created_at=record.created_at,
    )


def _knowledge_metadata_filters(
    crop_id: str,
    factor_codes: tuple[str, ...],
) -> tuple[ColumnElement[bool], ColumnElement[bool]]:
    crop_filter = or_(
        func.jsonb_array_length(KnowledgeChunkRecord.crops) == 0,
        KnowledgeChunkRecord.crops.contains([crop_id]),
    )
    factor_matches = [KnowledgeChunkRecord.factors.contains([code]) for code in factor_codes]
    factor_filter = or_(
        func.jsonb_array_length(KnowledgeChunkRecord.factors) == 0,
        *factor_matches,
    )
    return crop_filter, factor_filter


def _stored_chunk(
    chunk: KnowledgeChunkRecord,
    document: KnowledgeDocumentRecord,
) -> StoredChunk:
    return StoredChunk(
        chunk_id=chunk.chunk_id,
        document_id=document.id,
        organization=document.organization,
        title=document.title,
        source_roles=tuple(document.source_roles),
        relative_path=document.relative_path,
        source_reference=document.source_reference,
        corpus_version=document.corpus_version,
        page_start=chunk.page_start,
        page_end=chunk.page_end,
        section=chunk.section,
        content=chunk.content,
        content_sha256=chunk.content_sha256,
        crops=tuple(chunk.crops),
        factors=tuple(chunk.factors),
    )


def _structured_recommendation_to_dict(
    recommendation: StructuredRecommendation,
) -> dict[str, object]:
    return {
        "summary": recommendation.summary,
        "observations": list(recommendation.observations),
        "scenario_interpretation": recommendation.scenario_interpretation,
        "recommendations": [
            {
                "text": item.text,
                "rationale": item.rationale,
                "citation_ids": list(item.citation_ids),
            }
            for item in recommendation.recommendations
        ],
        "uncertainties": list(recommendation.uncertainties),
        "citation_ids": list(recommendation.citation_ids),
    }


def _structured_recommendation_from_dict(
    value: dict[str, object],
) -> StructuredRecommendation:
    raw_items = value.get("recommendations", [])
    if not isinstance(raw_items, list):
        raise ValueError("Persisted recommendation items must be an array.")
    items = tuple(
        RecommendationItem(
            text=str(item["text"]),
            rationale=str(item["rationale"]),
            citation_ids=tuple(str(citation) for citation in item.get("citation_ids", [])),
        )
        for item in raw_items
        if isinstance(item, dict)
    )
    return StructuredRecommendation(
        summary=str(value.get("summary", "")),
        observations=tuple(str(item) for item in _json_array(value.get("observations"))),
        scenario_interpretation=str(value.get("scenario_interpretation", "")),
        recommendations=items,
        uncertainties=tuple(str(item) for item in _json_array(value.get("uncertainties"))),
        citation_ids=tuple(str(item) for item in _json_array(value.get("citation_ids"))),
    )


def _json_array(value: object) -> tuple[object, ...]:
    return tuple(value) if isinstance(value, list) else ()


def _recommendation_run_from_record(record: RecommendationRunRecord) -> RecommendationRun:
    structured = record.structured_output
    recommendation = (
        _structured_recommendation_from_dict(structured) if structured is not None else None
    )
    return RecommendationRun(
        run_id=record.id,
        evaluation_id=record.evaluation_id,
        crop_id=record.crop_id,
        water_regime=record.water_regime,
        status=RecommendationStatus(record.status),
        prompt_version=record.prompt_version,
        provider=record.provider,
        model=record.model,
        response_id=record.response_id,
        corpus_version=record.corpus_version,
        retrieval_version=record.retrieval_version,
        embedding_index_id=record.embedding_index_id,
        cache_key=record.cache_key,
        recommendation=recommendation,
        failure_reason=record.failure_reason,
        input_tokens=record.input_tokens,
        output_tokens=record.output_tokens,
        created_at=record.created_at,
    )
