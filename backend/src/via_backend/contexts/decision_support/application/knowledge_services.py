"""Deterministic knowledge ingestion, retrieval, and recommendation coordination."""

from __future__ import annotations

import hashlib
import math
import re
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from threading import RLock
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

from via_backend.contexts.agroclimatic_evaluation.application.public import (
    FinalizedCropOutcomeStatus,
    FinalizedEvaluationNotFoundError,
    FinalizedEvaluationNotReadyError,
    FinalizedEvaluationResultReader,
    FinalizedLimitationEvidenceAvailability,
    GetFinalizedEvaluationResult,
    WaterRegime,
)

from .knowledge_models import (
    CorpusSource,
    EmbeddingIndex,
    EvidenceItem,
    IngestionReport,
    IngestionSourceResult,
    KnowledgeChunk,
    KnowledgeDocument,
    KnowledgeDocumentStatus,
    RecommendationCitation,
    RecommendationContext,
    RecommendationFactor,
    RecommendationRun,
    RecommendationStatus,
    RetrievalStatus,
    RetrievedKnowledge,
    StoredChunk,
    StructuredRecommendation,
    VectorSearchCandidate,
)
from .knowledge_ports import (
    IDocumentTextExtractor,
    IEmbeddingProvider,
    IKnowledgeChunker,
    IKnowledgeCorpusRepository,
    IKnowledgeRetriever,
    IKnowledgeSourceCatalog,
    IRecommendationGenerator,
    IRecommendationRepository,
)

DEFAULT_RETRIEVAL_VERSION = "hybrid-rrf-v4"
DEFAULT_PROMPT_VERSION = "agronomic-recommendation-v2"
_RRF_K = 60

_LOW_VALUE_SECTION_TITLES = frozenset(
    {
        "references",
        "referencias",
        "bibliography",
        "bibliografia",
        "contents",
        "table of contents",
        "index",
        "indice",
        "glossary",
        "glosario",
    }
)

_LOW_VALUE_SECTION_PREFIX = re.compile(
    r"^\s*\d{1,2}(?:\.\d{1,2}){0,3}[.)]?\s+"
)

_FRONT_MATTER_TOC_ENTRY = re.compile(
    r"\b\d{1,2}(?:\.\d{1,2}){0,3}\.?"
    r"\s+[^\d]{2,80}\s+\d{1,3}\b"
)


_GENERIC_SINGLE_WORD_HEADINGS = frozenset(
    {
        "BIBLIOGRAPHY",
        "BIBLIOGRAFIA",
        "CONCLUSIONS",
        "CONCLUSIONES",
        "GLOSSARY",
        "GLOSARIO",
        "INTRODUCTION",
        "INTRODUCCION",
        "REFERENCES",
        "REFERENCIAS",
    }
)
_NUMBERED_HEADING = re.compile(
    r"^(?P<number>\d{1,2}(?:\.\d{1,2}){0,3})(?P<terminator>[.)]?)\s+"
    r"(?P<title>\S(?:.*\S)?)$"
)
_DATA_PREFIXES = frozenset(
    {
        "cm",
        "g",
        "ha",
        "kg",
        "l",
        "m",
        "meq",
        "mg",
        "mm",
        "ppm",
        "t",
        "x",
    }
)
_TRAILING_CONNECTORS = frozenset(
    {
        "and",
        "de",
        "del",
        "o",
        "of",
        "or",
        "the",
        "y",
    }
)


class KnowledgeContextUnavailableError(LookupError):
    """Raised when the finalized scientific result cannot form a scenario context."""


class KnowledgeContextConflictError(RuntimeError):
    """Raised when an existing evaluation does not yet have finalized evidence."""


class KnowledgeProviderUnavailableError(RuntimeError):
    """External provider required by the knowledge use case is unavailable."""


class InvalidRecommendationError(ValueError):
    """Raised when generated structured output violates evidence/citation constraints."""


@dataclass(frozen=True, slots=True)
class Taxonomy:
    version: str
    factors: dict[str, tuple[str, ...]]
    crops: dict[str, tuple[str, ...]]
    water_regimes: dict[str, tuple[str, ...]]

    def expand_factor(self, factor_code: str) -> tuple[str, ...]:
        normalized = factor_code.strip().casefold()
        configured = self.factors.get(normalized)

        if configured is not None:
            return _unique_terms((normalized, *configured))

        if normalized.startswith("parameter_"):
            readable = normalized.removeprefix("parameter_").replace("_", " ")
            return _unique_terms((normalized, readable))

        return (normalized,) if normalized else ()

    def expand_crop(self, crop_id: str) -> tuple[str, ...]:
        normalized = crop_id.strip().casefold()
        return _unique_terms((normalized, *self.crops.get(normalized, ())))

    def expand_water_regime(self, water_regime: str) -> tuple[str, ...]:
        normalized = water_regime.strip().casefold()
        return _unique_terms((normalized, *self.water_regimes.get(normalized, ())))


class DeterministicKnowledgeChunker:
    """Page-aware deterministic chunker using recoverable headings and overlap."""

    def __init__(
        self,
        *,
        target_tokens: int = 650,
        min_tokens: int = 500,
        max_tokens: int = 800,
        overlap_tokens: int = 80,
    ) -> None:
        if not 0 <= overlap_tokens < min_tokens <= target_tokens <= max_tokens:
            raise ValueError(
                "Chunk token thresholds must be ordered and overlap must be smaller."
            )

        self._target = target_tokens
        self._minimum = min_tokens
        self._maximum = max_tokens
        self._overlap = overlap_tokens

    def chunk(
        self,
        source: CorpusSource,
        source_sha256: str,
        corpus_version: str,
        extracted: object,
    ) -> tuple[KnowledgeChunk, ...]:
        from .knowledge_models import ExtractedDocument

        if not isinstance(extracted, ExtractedDocument):
            raise TypeError("extracted must be an ExtractedDocument")

        cleaned = _remove_repeated_page_edges(extracted.pages)
        tokens = _structured_tokens(cleaned)

        if not tokens:
            return ()

        chunks: list[KnowledgeChunk] = []
        sequence = 0

        for span in _contiguous_section_spans(tokens):
            start = 0

            while start < len(span):
                remaining = len(span) - start

                if remaining <= self._maximum:
                    end = len(span)
                else:
                    end = _choose_boundary(
                        span,
                        start=start,
                        minimum=self._minimum,
                        target=self._target,
                        maximum=self._maximum,
                    )

                selected = span[start:end]
                content = " ".join(token.text for token in selected).strip()

                if content:
                    content_sha = hashlib.sha256(
                        content.encode("utf-8")
                    ).hexdigest()

                    chunk_id = hashlib.sha256(
                        (
                            f"{corpus_version}|"
                            f"{source.source_id}|"
                            f"{source_sha256}|"
                            f"{sequence}|"
                            f"{content_sha}"
                        ).encode()
                    ).hexdigest()

                    chunks.append(
                        KnowledgeChunk(
                            chunk_id=chunk_id,
                            sequence=sequence,
                            page_start=min(token.page for token in selected),
                            page_end=max(token.page for token in selected),
                            section=selected[0].section,
                            content=content,
                            content_sha256=content_sha,
                            crops=source.crops,
                            factors=source.factors,
                        )
                    )

                    sequence += 1

                if end >= len(span):
                    break

                start = max(start + 1, end - self._overlap)

        return tuple(chunks)


class KnowledgeIngestionService:
    """Ingest declarative corpus sources without coupling Application to files or providers."""

    def __init__(
        self,
        *,
        catalog: IKnowledgeSourceCatalog,
        extractor: IDocumentTextExtractor,
        chunker: IKnowledgeChunker,
        embeddings: IEmbeddingProvider,
        repository: IKnowledgeCorpusRepository,
        embedding_index_version: str,
        embedding_batch_size: int = 64,
    ) -> None:
        if embedding_batch_size < 1:
            raise ValueError("embedding_batch_size must be positive")

        self._catalog = catalog
        self._extractor = extractor
        self._chunker = chunker
        self._embeddings = embeddings
        self._repository = repository
        self._index_version = embedding_index_version
        self._batch_size = embedding_batch_size

    def ingest(self, *, dry_run: bool = False) -> IngestionReport:
        manifest = self._catalog.load_manifest()
        index = configured_embedding_index(
            self._embeddings,
            self._index_version,
        )

        if not dry_run:
            index = self._repository.ensure_embedding_index(index)

        results = tuple(
            self._ingest_source(
                source,
                manifest.corpus_version,
                index,
                dry_run=dry_run,
            )
            for source in manifest.sources
        )

        return IngestionReport(
            corpus_version=manifest.corpus_version,
            sources=results,
        )

    def _ingest_source(
        self,
        source: CorpusSource,
        corpus_version: str,
        index: EmbeddingIndex,
        *,
        dry_run: bool,
    ) -> IngestionSourceResult:
        source_bytes = self._catalog.read_source(source)
        source_sha = hashlib.sha256(source_bytes).hexdigest()
        document_id = _document_id(
            source.source_id,
            source_sha,
            corpus_version,
        )

        if not dry_run:
            existing = self._repository.find_document(
                source.source_id,
                source_sha,
                corpus_version,
            )

            if (
                existing is not None
                and existing.status is KnowledgeDocumentStatus.READY
            ):
                return IngestionSourceResult(
                    source_id=source.source_id,
                    status=existing.status,
                    document_id=existing.document_id,
                    source_sha256=source_sha,
                    page_count=existing.page_count,
                    pages_extracted=existing.pages_extracted,
                    chunks_generated=0,
                    chunks_embedded=0,
                    reused=True,
                    warnings=existing.warnings,
                )

        try:
            extracted = self._extractor.extract(source_bytes)

            status = (
                KnowledgeDocumentStatus.NEEDS_OCR
                if extracted.needs_ocr
                else KnowledgeDocumentStatus.READY
            )

            chunks = (
                ()
                if status is KnowledgeDocumentStatus.NEEDS_OCR
                else self._chunker.chunk(
                    source,
                    source_sha,
                    corpus_version,
                    extracted,
                )
            )

            if (
                status is KnowledgeDocumentStatus.READY
                and not chunks
            ):
                status = KnowledgeDocumentStatus.NEEDS_OCR

            document = KnowledgeDocument(
                document_id=document_id,
                source=source,
                corpus_version=corpus_version,
                source_sha256=source_sha,
                status=status,
                ingested_at=datetime.now(UTC),
                page_count=extracted.total_pages,
                pages_extracted=extracted.pages_extracted,
                warnings=extracted.warnings,
            )

            if dry_run or status is not KnowledgeDocumentStatus.READY:
                if not dry_run:
                    self._repository.save_document(
                        document,
                        (),
                        index,
                        {},
                        None,
                        0,
                    )

                return IngestionSourceResult(
                    source_id=source.source_id,
                    status=status,
                    document_id=document_id,
                    source_sha256=source_sha,
                    page_count=extracted.total_pages,
                    pages_extracted=extracted.pages_extracted,
                    chunks_generated=len(chunks),
                    chunks_embedded=0,
                    reused=False,
                    warnings=extracted.warnings,
                )

            (
                embeddings,
                input_tokens,
                request_count,
                embedded_count,
            ) = self._embed_chunks(
                source,
                chunks,
                index,
            )

            self._repository.save_document(
                document,
                chunks,
                index,
                embeddings,
                input_tokens,
                request_count,
            )

            return IngestionSourceResult(
                source_id=source.source_id,
                status=status,
                document_id=document_id,
                source_sha256=source_sha,
                page_count=extracted.total_pages,
                pages_extracted=extracted.pages_extracted,
                chunks_generated=len(chunks),
                chunks_embedded=embedded_count,
                reused=False,
                warnings=extracted.warnings,
            )

        except Exception as error:
            if dry_run:
                raise

            failed = KnowledgeDocument(
                document_id=document_id,
                source=source,
                corpus_version=corpus_version,
                source_sha256=source_sha,
                status=KnowledgeDocumentStatus.FAILED,
                ingested_at=datetime.now(UTC),
                page_count=0,
                pages_extracted=0,
                warnings=(
                    f"ingestion_failed:{type(error).__name__}",
                ),
            )

            self._repository.save_document(
                failed,
                (),
                index,
                {},
                None,
                0,
            )

            return IngestionSourceResult(
                source_id=source.source_id,
                status=KnowledgeDocumentStatus.FAILED,
                document_id=document_id,
                source_sha256=source_sha,
                page_count=0,
                pages_extracted=0,
                chunks_generated=0,
                chunks_embedded=0,
                reused=False,
                warnings=failed.warnings,
            )

    def _embed_chunks(
        self,
        source: CorpusSource,
        chunks: tuple[KnowledgeChunk, ...],
        index: EmbeddingIndex,
    ) -> tuple[
        dict[str, tuple[float, ...]],
        int | None,
        int,
        int,
    ]:
        chunk_ids = tuple(chunk.chunk_id for chunk in chunks)

        reusable = self._repository.reusable_embeddings(
            chunk_ids,
            index.index_id,
        )

        by_chunk: dict[str, tuple[float, ...]] = {}
        missing: list[KnowledgeChunk] = []

        for chunk in chunks:
            reused = reusable.get(chunk.chunk_id)

            if reused is None:
                missing.append(chunk)
            else:
                by_chunk[chunk.chunk_id] = reused

        total_tokens: int | None = 0
        request_count = 0

        for offset in range(0, len(missing), self._batch_size):
            batch_chunks = tuple(
                missing[offset : offset + self._batch_size]
            )

            batch = self._embeddings.embed(
                tuple(
                    _embedding_text(source, chunk)
                    for chunk in batch_chunks
                )
            )

            if len(batch.vectors) != len(batch_chunks):
                raise RuntimeError(
                    "Embedding provider returned an unexpected vector count."
                )

            request_count += batch.request_count

            if batch.input_tokens is None:
                total_tokens = None
            elif total_tokens is not None:
                total_tokens += batch.input_tokens

            for chunk, vector in zip(
                batch_chunks,
                batch.vectors,
                strict=True,
            ):
                if len(vector.values) != index.dimensions:
                    raise RuntimeError(
                        "Embedding dimension does not match the configured index."
                    )

                by_chunk[chunk.chunk_id] = vector.values

        return (
            by_chunk,
            total_tokens,
            request_count,
            len(missing),
        )


class RecommendationContextBuilder:
    """Translate finalized public scientific evidence into one scenario context."""

    def __init__(
        self,
        finalized_results: FinalizedEvaluationResultReader,
    ) -> None:
        self._finalized_results = finalized_results

    def build(
        self,
        evaluation_id: UUID,
        crop_id: str,
        water_regime: WaterRegime,
    ) -> RecommendationContext:
        try:
            finalized = self._finalized_results.get_finalized_evaluation_result(
                GetFinalizedEvaluationResult(
                    evaluation_id=evaluation_id,
                    water_regime=water_regime,
                )
            )
        except FinalizedEvaluationNotFoundError as error:
            raise KnowledgeContextUnavailableError(str(error)) from error
        except FinalizedEvaluationNotReadyError as error:
            raise KnowledgeContextConflictError(str(error)) from error

        outcome = next(
            (
                item
                for item in finalized.outcomes
                if item.crop_id == crop_id
            ),
            None,
        )

        if outcome is None:
            raise KnowledgeContextUnavailableError(
                f"Crop {crop_id!r} is not part of evaluation {evaluation_id}."
            )

        if outcome.status is not FinalizedCropOutcomeStatus.SUCCEEDED:
            raise KnowledgeContextUnavailableError(
                f"Crop {crop_id!r} does not have a successful scientific outcome."
            )

        limitation = outcome.limitation_evidence
        factors: tuple[RecommendationFactor, ...] = ()

        if limitation.availability in {
            FinalizedLimitationEvidenceAvailability.AVAILABLE,
            FinalizedLimitationEvidenceAvailability.PARTIAL,
        }:
            factors = tuple(
                RecommendationFactor(
                    factor_code=item.factor_code,
                    label=item.label,
                    affected_fraction=item.affected_fraction,
                    dominant=item.dominant,
                    display_label=item.display_label,
                )
                for item in limitation.factors
            )

        return RecommendationContext(
            evaluation_id=evaluation_id,
            crop_id=crop_id,
            water_regime=water_regime.value,
            suitability_mean=(
                outcome.suitability.mean
                if outcome.suitability
                else None
            ),
            factors=factors,
        )


class HybridKnowledgeRetriever(IKnowledgeRetriever):
    """Deterministic lexical + vector retrieval with reciprocal-rank fusion."""

    def __init__(
        self,
        *,
        repository: IKnowledgeCorpusRepository,
        embeddings: IEmbeddingProvider,
        taxonomy: Taxonomy,
        embedding_index: EmbeddingIndex,
        corpus_version: str,
        vector_top_k: int,
        lexical_top_k: int,
        final_top_k: int,
        retrieval_version: str = DEFAULT_RETRIEVAL_VERSION,
    ) -> None:
        self._repository = repository
        self._embeddings = embeddings
        self._taxonomy = taxonomy
        self._index = embedding_index
        self._corpus_version = corpus_version
        self._vector_top_k = vector_top_k
        self._lexical_top_k = lexical_top_k
        self._final_top_k = final_top_k
        self._retrieval_version = retrieval_version

    def retrieve(
        self,
        context: RecommendationContext,
    ) -> RetrievedKnowledge:
        factor_codes = tuple(
            item.factor_code
            for item in context.factors
        )

        lexical_query = build_lexical_retrieval_query(
            context,
            self._taxonomy,
        )
        semantic_query = build_semantic_retrieval_query(
            context,
            self._taxonomy,
        )

        trace_query = (
            f"lexical: {lexical_query}\n"
            f"semantic: {semantic_query}"
        )

        run_id = uuid4()

        if (
            not factor_codes
            or not lexical_query
            or not semantic_query
        ):
            result = RetrievedKnowledge(
                retrieval_run_id=run_id,
                evaluation_id=context.evaluation_id,
                crop_id=context.crop_id,
                water_regime=context.water_regime,
                limiting_factors=factor_codes,
                retrieval_status=(
                    RetrievalStatus.INSUFFICIENT_EVIDENCE
                ),
                query=trace_query,
                corpus_version=self._corpus_version,
                retrieval_version=self._retrieval_version,
                embedding_index=self._index,
                evidence=(),
            )

            self._repository.persist_retrieval(result)
            return result

        raw_lexical = self._repository.lexical_search(
            lexical_query,
            context.crop_id,
            factor_codes,
            self._corpus_version,
            max(
                self._lexical_top_k,
                self._lexical_top_k * 3,
            ),
        )

        lexical = _filter_low_value_lexical_hits(
            raw_lexical,
            self._lexical_top_k,
        )

        embedded_query = self._embeddings.embed(
            (semantic_query,)
        )

        if len(embedded_query.vectors) != 1:
            raise RuntimeError(
                "Embedding provider did not return the query vector."
            )

        query_vector = embedded_query.vectors[0].values

        raw_candidates = self._repository.vector_candidates(
            context.crop_id,
            factor_codes,
            self._corpus_version,
            self._index.index_id,
        )

        candidates = tuple(
            candidate
            for candidate in raw_candidates
            if not _is_low_value_chunk(candidate.chunk)
        )

        vector = _rank_vectors(
            query_vector,
            candidates,
            self._vector_top_k,
        )

        evidence = _fuse_hits(
            lexical,
            vector,
            self._final_top_k,
        )

        result = RetrievedKnowledge(
            retrieval_run_id=run_id,
            evaluation_id=context.evaluation_id,
            crop_id=context.crop_id,
            water_regime=context.water_regime,
            limiting_factors=factor_codes,
            retrieval_status=(
                RetrievalStatus.AVAILABLE
                if evidence
                else RetrievalStatus.INSUFFICIENT_EVIDENCE
            ),
            query=trace_query,
            corpus_version=self._corpus_version,
            retrieval_version=self._retrieval_version,
            embedding_index=self._index,
            evidence=evidence,
        )

        self._repository.persist_retrieval(result)

        return result


class RecommendationApplicationService:
    """Coordinate retrieval, safe generation, caching, citation validation, and trace."""

    def __init__(
        self,
        *,
        retriever: IKnowledgeRetriever,
        generator: IRecommendationGenerator,
        repository: IRecommendationRepository,
        prompt_version: str = DEFAULT_PROMPT_VERSION,
    ) -> None:
        self._retriever = retriever
        self._generator = generator
        self._repository = repository
        self._prompt_version = prompt_version
        self._generation_lock = RLock()

    def retrieve(
        self,
        context: RecommendationContext,
    ) -> RetrievedKnowledge:
        return self._retriever.retrieve(context)

    def generate(
        self,
        context: RecommendationContext,
        *,
        force_regenerate: bool = False,
        owner_user_id: UUID | None = None,
    ) -> RecommendationRun:
        # One API instance: serialize cache lookup and provider call so concurrent
        # requests for the same recommendation do not both pay for generation.
        with self._generation_lock:
            return self._generate_unlocked(
                context, force_regenerate=force_regenerate,
                owner_user_id=owner_user_id,
            )

    def _generate_unlocked(
        self,
        context: RecommendationContext,
        *,
        force_regenerate: bool,
        owner_user_id: UUID | None,
    ) -> RecommendationRun:
        evidence = self._retriever.retrieve(context)

        cache_key = recommendation_cache_key(
            context,
            evidence,
            self._prompt_version,
            self._generator.model,
        )

        if not force_regenerate:
            cached = (
                self._repository.find_succeeded_by_cache_key(
                    cache_key
                )
            )

            if cached is not None:
                return cached

        created_at = datetime.now(UTC)

        if (
            evidence.retrieval_status
            is not RetrievalStatus.AVAILABLE
        ):
            run = RecommendationRun(
                run_id=uuid4(),
                evaluation_id=context.evaluation_id,
                crop_id=context.crop_id,
                water_regime=context.water_regime,
                status=RecommendationStatus.INSUFFICIENT_EVIDENCE,
                prompt_version=self._prompt_version,
                provider=self._generator.provider_name,
                model=self._generator.model,
                response_id=None,
                corpus_version=evidence.corpus_version,
                retrieval_version=evidence.retrieval_version,
                embedding_index_id=evidence.embedding_index.index_id,
                cache_key=cache_key,
                recommendation=None,
                failure_reason="insufficient_retrieved_evidence",
                input_tokens=None,
                output_tokens=None,
                created_at=created_at,
            )

            self._repository.save(
                run,
                evidence,
            )

            return run

        if owner_user_id is not None:
            self._repository.record_generation_attempt(
                owner_user_id, context.evaluation_id, created_at,
            )

        try:
            generated = self._generator.generate(
                context,
                evidence,
            )

            validate_recommendation(
                generated.recommendation,
                evidence,
            )

            run = RecommendationRun(
                run_id=uuid4(),
                evaluation_id=context.evaluation_id,
                crop_id=context.crop_id,
                water_regime=context.water_regime,
                status=RecommendationStatus.SUCCEEDED,
                prompt_version=self._prompt_version,
                provider=generated.provider,
                model=generated.model,
                response_id=generated.response_id,
                corpus_version=evidence.corpus_version,
                retrieval_version=evidence.retrieval_version,
                embedding_index_id=evidence.embedding_index.index_id,
                cache_key=cache_key,
                recommendation=generated.recommendation,
                failure_reason=None,
                input_tokens=generated.input_tokens,
                output_tokens=generated.output_tokens,
                created_at=created_at,
                citations=_recommendation_citations(
                    generated.recommendation,
                    evidence,
                ),
            )

        except Exception as error:
            run = RecommendationRun(
                run_id=uuid4(),
                evaluation_id=context.evaluation_id,
                crop_id=context.crop_id,
                water_regime=context.water_regime,
                status=RecommendationStatus.FAILED,
                prompt_version=self._prompt_version,
                provider=self._generator.provider_name,
                model=self._generator.model,
                response_id=None,
                corpus_version=evidence.corpus_version,
                retrieval_version=evidence.retrieval_version,
                embedding_index_id=evidence.embedding_index.index_id,
                cache_key=cache_key,
                recommendation=None,
                failure_reason=(
                    f"generation_failed:{type(error).__name__}"
                ),
                input_tokens=None,
                output_tokens=None,
                created_at=created_at,
            )

        self._repository.save(
            run,
            evidence,
        )

        return run

    def list_for_evaluation(
        self,
        evaluation_id: UUID,
    ) -> tuple[RecommendationRun, ...]:
        return self._repository.list_for_evaluation(
            evaluation_id
        )


def _recommendation_citations(
    recommendation: StructuredRecommendation,
    evidence: RetrievedKnowledge,
) -> tuple[RecommendationCitation, ...]:
    by_evidence_id = {
        item.evidence_id: item
        for item in evidence.evidence
    }
    citation_ids = list(recommendation.citation_ids)
    for item in recommendation.recommendations:
        citation_ids.extend(item.citation_ids)

    return tuple(
        RecommendationCitation(
            evidence_id=evidence_item.evidence_id,
            chunk_id=evidence_item.chunk_id,
            organization=evidence_item.organization,
            title=evidence_item.title,
            page_start=evidence_item.page_start,
            page_end=evidence_item.page_end,
            section=evidence_item.section,
            source_reference=evidence_item.source_reference,
        )
        for evidence_id in dict.fromkeys(citation_ids)
        if (evidence_item := by_evidence_id.get(evidence_id)) is not None
    )


def build_lexical_retrieval_query(
    context: RecommendationContext,
    taxonomy: Taxonomy,
) -> str:
    terms: list[str] = []

    for factor in context.factors:
        expanded = taxonomy.expand_factor(
            factor.factor_code
        )

        for term in expanded:
            if (
                factor.factor_code.startswith("parameter_")
                and term == factor.factor_code
            ):
                continue

            terms.append(term)

    escaped = [
        f'"{term.replace(chr(34), "")}"'
        for term in _unique_terms(tuple(terms))
        if term
    ]

    return " OR ".join(escaped)


def build_semantic_retrieval_query(
    context: RecommendationContext,
    taxonomy: Taxonomy,
) -> str:
    factor_terms: list[str] = []

    for factor in context.factors:
        expanded = taxonomy.expand_factor(
            factor.factor_code
        )

        for term in expanded:
            if (
                factor.factor_code.startswith("parameter_")
                and term == factor.factor_code
            ):
                continue

            factor_terms.append(term)

    factor_terms = list(
        _unique_terms(tuple(factor_terms))
    )

    if not factor_terms:
        return ""

    crop = (
        context.crop_id
        .replace("_", " ")
        .strip()
    )
    water_regime = (
        context.water_regime
        .replace("_", " ")
        .strip()
    )

    focus = ", ".join(factor_terms)

    return (
        f"Agronomic evidence about {focus} for {crop}. "
        "Focus on the limiting factor and its agronomic implications. "
        f"Scenario context: {water_regime} conditions."
    )


def build_retrieval_query(
    context: RecommendationContext,
    taxonomy: Taxonomy,
) -> str:
    """Backward-compatible lexical query builder."""
    return build_lexical_retrieval_query(
        context,
        taxonomy,
    )


def validate_recommendation(
    recommendation: StructuredRecommendation,
    evidence: RetrievedKnowledge,
) -> None:
    allowed = {
        item.evidence_id
        for item in evidence.evidence
    }

    if (
        recommendation.recommendations
        and not recommendation.citation_ids
    ):
        raise InvalidRecommendationError(
            "Recommendation output must cite supplied evidence."
        )

    unknown_top = (
        set(recommendation.citation_ids)
        - allowed
    )

    if unknown_top:
        raise InvalidRecommendationError(
            "Recommendation output contains an unknown citation id."
        )

    for item in recommendation.recommendations:
        if not item.citation_ids:
            raise InvalidRecommendationError(
                "Every recommendation must contain a citation id."
            )

        if set(item.citation_ids) - allowed:
            raise InvalidRecommendationError(
                "A recommendation contains an unknown citation id."
            )


def recommendation_cache_key(
    context: RecommendationContext,
    evidence: RetrievedKnowledge,
    prompt_version: str,
    model: str,
) -> str:
    payload = "|".join(
        (
            str(context.evaluation_id),
            context.crop_id,
            context.water_regime,
            prompt_version,
            model,
            evidence.corpus_version,
            evidence.retrieval_version,
            evidence.embedding_index.index_version,
            *(
                f"{item.evidence_id}:{item.chunk_id}"
                for item in evidence.evidence
            ),
        )
    )

    return hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()


def configured_embedding_index(
    embeddings: IEmbeddingProvider,
    index_version: str,
) -> EmbeddingIndex:
    return EmbeddingIndex(
        index_id=_embedding_index_id(
            embeddings.provider_name,
            embeddings.model,
            embeddings.dimensions,
            index_version,
        ),
        provider=embeddings.provider_name,
        model=embeddings.model,
        dimensions=embeddings.dimensions,
        index_version=index_version,
        created_at=datetime.now(UTC),
    )


@dataclass(frozen=True, slots=True)
class _Token:
    text: str
    page: int
    section: str | None


def _unique_terms(
    values: tuple[str, ...],
) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []

    for value in values:
        normalized = " ".join(
            value.strip().casefold().split()
        )

        if normalized and normalized not in seen:
            seen.add(normalized)
            ordered.append(normalized)

    return tuple(ordered)


def _embedding_text(
    source: CorpusSource,
    chunk: KnowledgeChunk,
) -> str:
    parts = [
        f"Document: {source.title}"
    ]

    if chunk.section:
        parts.append(
            f"Section: {chunk.section}"
        )

    parts.append(
        chunk.content
    )

    return "\n\n".join(parts)


def _remove_repeated_page_edges(
    pages: tuple[object, ...],
) -> tuple[tuple[int, str], ...]:
    from .knowledge_models import ExtractedPage

    typed = tuple(
        page
        for page in pages
        if isinstance(page, ExtractedPage)
    )

    if not typed:
        return ()

    first_counts: dict[str, int] = {}
    last_counts: dict[str, int] = {}
    page_lines: list[
        tuple[int, list[str]]
    ] = []

    for page in typed:
        lines = [
            line.strip()
            for line in page.text.splitlines()
            if line.strip()
        ]

        page_lines.append(
            (
                page.page_number,
                lines,
            )
        )

        if lines:
            first_counts[lines[0]] = (
                first_counts.get(
                    lines[0],
                    0,
                )
                + 1
            )

            last_counts[lines[-1]] = (
                last_counts.get(
                    lines[-1],
                    0,
                )
                + 1
            )

    threshold = max(
        3,
        math.ceil(len(typed) / 2),
    )

    repeated_first = {
        line
        for line, count in first_counts.items()
        if count >= threshold
    }

    repeated_last = {
        line
        for line, count in last_counts.items()
        if count >= threshold
    }

    cleaned: list[
        tuple[int, str]
    ] = []

    for page_number, lines in page_lines:
        if (
            lines
            and lines[0] in repeated_first
        ):
            lines = lines[1:]

        if (
            lines
            and lines[-1] in repeated_last
        ):
            lines = lines[:-1]

        cleaned.append(
            (
                page_number,
                "\n".join(lines),
            )
        )

    return tuple(cleaned)


def _structured_tokens(
    pages: tuple[tuple[int, str], ...],
) -> tuple[_Token, ...]:
    tokens: list[_Token] = []
    section: str | None = None

    for page_number, text in pages:
        for raw_line in text.splitlines():
            line = " ".join(
                raw_line.split()
            )

            if not line:
                continue

            if _looks_like_heading(
                raw_line,
                line,
            ):
                section = line

            tokens.extend(
                _Token(
                    word,
                    page_number,
                    section,
                )
                for word in line.split()
            )

    return tuple(tokens)


def _contiguous_section_spans(
    tokens: tuple[_Token, ...],
) -> tuple[tuple[_Token, ...], ...]:
    if not tokens:
        return ()

    spans: list[
        tuple[_Token, ...]
    ] = []

    start = 0
    current_section = tokens[0].section

    for index in range(
        1,
        len(tokens),
    ):
        if (
            tokens[index].section
            != current_section
        ):
            spans.append(
                tokens[start:index]
            )

            start = index
            current_section = (
                tokens[index].section
            )

    spans.append(
        tokens[start:]
    )

    return tuple(spans)


def _looks_like_heading(
    raw_line: str,
    normalized_line: str | None = None,
) -> bool:
    line = (
        " ".join(raw_line.split())
        if normalized_line is None
        else normalized_line.strip()
    )

    if (
        not line
        or len(line) > 80
        or len(line.split()) > 10
    ):
        return False

    numbered = _NUMBERED_HEADING.fullmatch(line)

    if numbered is not None:
        return _looks_like_numbered_heading(
            raw_line,
            numbered.group("number"),
            numbered.group("terminator"),
            numbered.group("title"),
        )

    if (
        any(char.isdigit() for char in line)
        or _has_table_spacing(raw_line)
        or _has_formula_or_url(line)
        or _has_unbalanced_delimiters(line)
        or "." in line
        or line.endswith(("/", "\\"))
        or line.count(",") >= 2
    ):
        return False

    letters = [
        char
        for char in line
        if char.isalpha()
    ]

    if (
        not letters
        or len(letters) < 4
        or (
            sum(
                char.isupper()
                for char in letters
            )
            / len(letters)
        )
        < 0.95
    ):
        return False

    words = [
        word.strip("'\".,:;()[]{}")
        for word in line.split()
        if word.strip("'\".,:;()[]{}")
    ]

    if len(words) == 1:
        return _heading_key(words[0]) in _GENERIC_SINGLE_WORD_HEADINGS

    alpha_words = [
        "".join(
            char
            for char in word
            if char.isalpha()
        )
        for word in words
    ]
    alpha_words = [word for word in alpha_words if word]

    return not (
        len(alpha_words) >= 2
        and all(len(word) <= 4 for word in alpha_words)
    )


def _looks_like_numbered_heading(
    raw_line: str,
    number: str,
    terminator: str,
    title: str,
) -> bool:
    components = number.split(".")

    if (
        components[0] == "0"
        or (len(components) == 1 and not terminator)
        or _has_table_spacing(raw_line)
        or _has_formula_or_url(title)
        or re.search(r"\.{3,}", title)
        or re.search(r"\s\d{1,3}$", title)
        or title.endswith((".", ",", ";"))
        or not title[0].isalpha()
        or _has_unbalanced_delimiters(title)
        or _has_mixed_alphanumeric_token(title)
        or title.casefold().rstrip(" ,;:").split()[-1] in _TRAILING_CONNECTORS
        or re.search(
            r"(?:^|\s)\d{1,2}(?:\.\d{1,2}){0,3}[.)]\s+",
            title,
        )
    ):
        return False

    first_word = title.split()[0].strip("'\".,:;()[]{}")
    first_key = _heading_key(first_word).casefold()
    first_letter = next(
        (
            char
            for char in first_word
            if char.isalpha()
        ),
        "",
    )

    if (
        not first_letter
        or first_letter.islower()
        or first_key in _DATA_PREFIXES
    ):
        return False

    title_tokens = title.split()
    numeric_tokens = sum(
        any(char.isdigit() for char in token)
        for token in title_tokens
    )

    return numeric_tokens <= max(1, len(title_tokens) // 3)


def _has_table_spacing(raw_line: str) -> bool:
    return "\t" in raw_line or re.search(r"\S {3,}\S", raw_line) is not None


def _has_formula_or_url(line: str) -> bool:
    lowered = line.casefold()

    return (
        "://" in lowered
        or "www." in lowered
        or "doi.org" in lowered
        or "=" in line
        or "<" in line
        or ">" in line
        or "%" in line
        or re.search(r"\d\s*[x×*/+]\s*\d", line, re.IGNORECASE) is not None
    )


def _has_unbalanced_delimiters(line: str) -> bool:
    return line.count("(") != line.count(")") or line.count("[") != line.count("]")


def _has_mixed_alphanumeric_token(line: str) -> bool:
    return any(
        any(char.isalpha() for char in token)
        and any(char.isdigit() for char in token)
        for token in line.split()
    )


def _heading_key(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    return "".join(
        char
        for char in decomposed
        if not unicodedata.combining(char)
    ).upper()


def _choose_boundary(
    tokens: tuple[_Token, ...],
    *,
    start: int,
    minimum: int,
    target: int,
    maximum: int,
) -> int:
    remaining = len(tokens) - start

    if remaining <= maximum:
        return len(tokens)

    low = start + minimum
    high = min(
        len(tokens),
        start + maximum,
    )

    preferred = min(
        high,
        start + target,
    )

    boundaries = [
        index
        for index in range(
            low,
            high,
        )
        if (
            tokens[index - 1].page
            != tokens[index].page
            or tokens[index - 1].section
            != tokens[index].section
        )
    ]

    if boundaries:
        return min(
            boundaries,
            key=lambda index: (
                abs(index - preferred),
                index,
            ),
        )

    return preferred


def _fold_retrieval_text(
    value: str,
) -> str:
    decomposed = unicodedata.normalize(
        "NFKD",
        value,
    )

    without_accents = "".join(
        character
        for character in decomposed
        if not unicodedata.combining(character)
    )

    return " ".join(
        without_accents.casefold().split()
    )


def _normalized_section_name(
    value: str,
) -> str:
    without_number = _LOW_VALUE_SECTION_PREFIX.sub(
        "",
        value.strip(),
    )

    return _fold_retrieval_text(
        without_number
    )


def _is_probable_front_matter(
    chunk: StoredChunk,
) -> bool:
    if (
        not chunk.section
        or chunk.page_start > 10
    ):
        return False

    section_name = _fold_retrieval_text(
        chunk.section
    )
    title_name = _fold_retrieval_text(
        chunk.title
    )

    if section_name != title_name:
        return False

    content = _fold_retrieval_text(
        chunk.content
    )

    markers = (
        "isbn",
        "autores",
        "authors",
        "editor",
        "publicado",
        "published",
        "primera edicion",
        "first edition",
        "copyright",
    )

    marker_count = sum(
        marker in content
        for marker in markers
    )

    toc_entries = len(
        _FRONT_MATTER_TOC_ENTRY.findall(
            chunk.content
        )
    )

    return (
        marker_count >= 2
        or toc_entries >= 4
    )


def _is_low_value_chunk(
    chunk: StoredChunk,
) -> bool:
    if chunk.section:
        section_name = _normalized_section_name(
            chunk.section
        )

        if section_name in _LOW_VALUE_SECTION_TITLES:
            return True

    return _is_probable_front_matter(chunk)


def _filter_low_value_lexical_hits(
    hits: tuple[object, ...],
    limit: int,
) -> tuple[object, ...]:
    from .knowledge_models import LexicalSearchHit

    accepted = [
        hit
        for hit in hits
        if isinstance(hit, LexicalSearchHit)
        and not _is_low_value_chunk(hit.chunk)
    ]

    return tuple(
        LexicalSearchHit(
            chunk=hit.chunk,
            rank=rank,
            score=hit.score,
        )
        for rank, hit in enumerate(
            accepted[:limit],
            start=1,
        )
    )


def _rank_vectors(
    query_vector: tuple[float, ...],
    candidates: tuple[
        VectorSearchCandidate,
        ...,
    ],
    limit: int,
) -> tuple[
    tuple[
        StoredChunk,
        int,
        float,
    ],
    ...,
]:
    scored = [
        (
            candidate.chunk,
            _cosine_similarity(
                query_vector,
                candidate.vector,
            ),
        )
        for candidate in candidates
    ]

    scored.sort(
        key=lambda item: (
            -item[1],
            item[0].chunk_id,
        )
    )

    return tuple(
        (
            chunk,
            rank,
            score,
        )
        for rank, (
            chunk,
            score,
        ) in enumerate(
            scored[:limit],
            1,
        )
    )


def _cosine_similarity(
    left: tuple[float, ...],
    right: tuple[float, ...],
) -> float:
    if (
        len(left) != len(right)
        or not left
    ):
        return -1.0

    numerator = sum(
        a * b
        for a, b in zip(
            left,
            right,
            strict=True,
        )
    )

    left_norm = math.sqrt(
        sum(
            value * value
            for value in left
        )
    )

    right_norm = math.sqrt(
        sum(
            value * value
            for value in right
        )
    )

    if (
        left_norm == 0
        or right_norm == 0
    ):
        return -1.0

    return numerator / (
        left_norm * right_norm
    )


def _fuse_hits(
    lexical: tuple[object, ...],
    vector: tuple[
        tuple[
            StoredChunk,
            int,
            float,
        ],
        ...,
    ],
    limit: int,
) -> tuple[EvidenceItem, ...]:
    from .knowledge_models import LexicalSearchHit

    chunks: dict[
        str,
        StoredChunk,
    ] = {}

    lexical_ranks: dict[
        str,
        int,
    ] = {}

    vector_ranks: dict[
        str,
        int,
    ] = {}

    scores: dict[
        str,
        float,
    ] = {}

    for hit in lexical:
        if not isinstance(
            hit,
            LexicalSearchHit,
        ):
            continue

        chunk_id = hit.chunk.chunk_id

        chunks[chunk_id] = hit.chunk

        lexical_ranks[chunk_id] = (
            hit.rank
        )

        scores[chunk_id] = (
            scores.get(
                chunk_id,
                0.0,
            )
            + 1.0
            / (
                _RRF_K
                + hit.rank
            )
        )

    for (
        chunk,
        rank,
        _similarity,
    ) in vector:
        chunks[chunk.chunk_id] = chunk

        vector_ranks[
            chunk.chunk_id
        ] = rank

        scores[
            chunk.chunk_id
        ] = (
            scores.get(
                chunk.chunk_id,
                0.0,
            )
            + 1.0
            / (
                _RRF_K
                + rank
            )
        )

    ordered = sorted(
        scores,
        key=lambda chunk_id: (
            -scores[chunk_id],
            chunk_id,
        ),
    )[:limit]

    evidence: list[
        EvidenceItem
    ] = []

    for (
        ordinal,
        chunk_id,
    ) in enumerate(
        ordered,
        1,
    ):
        chunk = chunks[
            chunk_id
        ]

        evidence.append(
            EvidenceItem(
                evidence_id=(
                    f"SOURCE_{ordinal}"
                ),
                chunk_id=chunk.chunk_id,
                organization=chunk.organization,
                title=chunk.title,
                source_roles=chunk.source_roles,
                page_start=chunk.page_start,
                page_end=chunk.page_end,
                section=chunk.section,
                content=chunk.content,
                source_reference=(
                    chunk.source_reference
                    or chunk.relative_path
                ),
                lexical_rank=(
                    lexical_ranks.get(
                        chunk_id
                    )
                ),
                vector_rank=(
                    vector_ranks.get(
                        chunk_id
                    )
                ),
                fused_score=(
                    scores[chunk_id]
                ),
            )
        )

    return tuple(evidence)


def _document_id(
    source_id: str,
    source_sha256: str,
    corpus_version: str,
) -> UUID:
    return uuid5(
        NAMESPACE_URL,
        (
            "via:knowledge:"
            f"{source_id}:"
            f"{source_sha256}:"
            f"{corpus_version}"
        ),
    )


def _embedding_index_id(
    provider: str,
    model: str,
    dimensions: int,
    index_version: str,
) -> UUID:
    return uuid5(
        NAMESPACE_URL,
        (
            "via:embedding-index:"
            f"{provider}:"
            f"{model}:"
            f"{dimensions}:"
            f"{index_version}"
        ),
    )
