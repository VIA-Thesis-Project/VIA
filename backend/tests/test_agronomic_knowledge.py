"""Focused tests for the Decision Support agronomic knowledge increment."""

from __future__ import annotations

import importlib.util
import io
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest
from alembic.migration import MigrationContext
from alembic.operations import Operations
from pypdf import PdfWriter
from sqlalchemy.dialects import postgresql

from via_backend.contexts.decision_support.application.knowledge_models import (
    CorpusManifest,
    CorpusSource,
    EmbeddingBatch,
    EmbeddingIndex,
    EmbeddingVector,
    EvidenceItem,
    ExtractedDocument,
    ExtractedPage,
    KnowledgeDocument,
    LexicalSearchHit,
    RecommendationContext,
    RecommendationFactor,
    RecommendationGeneration,
    RecommendationItem,
    RecommendationRun,
    RecommendationStatus,
    RetrievalStatus,
    RetrievedKnowledge,
    StoredChunk,
    StructuredRecommendation,
    VectorSearchCandidate,
)
from via_backend.contexts.decision_support.application.knowledge_services import (
    DeterministicKnowledgeChunker,
    HybridKnowledgeRetriever,
    KnowledgeIngestionService,
    RecommendationApplicationService,
    Taxonomy,
    _looks_like_heading,
    configured_embedding_index,
)
from via_backend.contexts.decision_support.infrastructure import openai_knowledge
from via_backend.contexts.decision_support.infrastructure import orm as decision_support_orm
from via_backend.contexts.decision_support.infrastructure.knowledge_manifest import (
    ManifestValidationError,
    YamlFilesystemKnowledgeSourceCatalog,
    load_taxonomy,
)
from via_backend.contexts.decision_support.infrastructure.openai_knowledge import (
    MissingOpenAIAPIKeyError,
    OpenAIEmbeddingProvider,
    OpenAIRecommendationGenerator,
)
from via_backend.contexts.decision_support.infrastructure.pdf_extractor import (
    PyPdfDocumentTextExtractor,
)

ROOT = Path(__file__).parents[2]
RAG_TABLES = {
    "embedding_indexes",
    "knowledge_chunks",
    "knowledge_documents",
    "knowledge_embeddings",
    "recommendation_citations",
    "recommendation_runs",
    "retrieval_hits",
    "retrieval_runs",
}


def test_migration_0015_compiles_with_postgresql_identifier_limits() -> None:
    migration_path = (
        ROOT
        / "backend"
        / "migrations"
        / "versions"
        / "20260918_0015_agronomic_knowledge_rag.py"
    )
    spec = importlib.util.spec_from_file_location("migration_0015", migration_path)
    assert spec is not None and spec.loader is not None
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)

    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql",
        opts={"as_sql": True, "output_buffer": output},
    )
    with Operations.context(context):
        migration.upgrade()

    sql = output.getvalue()
    assert "CONSTRAINT fk_rec_citations_run" in sql
    assert "CONSTRAINT ck_recommendation_runs_rec_run_water_regime_supported" in sql


def test_rag_orm_identifiers_fit_postgresql_limit() -> None:
    max_length = postgresql.dialect().max_identifier_length
    too_long: list[str] = []

    for table in decision_support_orm.Base.metadata.tables.values():
        if table.name not in RAG_TABLES:
            continue
        names = [
            *(constraint.name for constraint in table.constraints),
            *(index.name for index in table.indexes),
        ]
        too_long.extend(
            str(name)
            for name in names
            if name is not None and len(str(name)) > max_length
        )

    assert too_long == []

    citations = decision_support_orm.Base.metadata.tables[
        "decision_support.recommendation_citations"
    ]
    run_fk = next(
        constraint
        for constraint in citations.foreign_key_constraints
        if constraint.column_keys == ["recommendation_run_id"]
    )
    assert str(run_fk.name) == "fk_rec_citations_run"


def _source(*, relative_path: str = "inia/document.pdf") -> CorpusSource:
    return CorpusSource(
        source_id="source-1",
        organization="INIA",
        title="Document",
        language="es",
        source_type="pdf",
        source_roles=("management_guidance",),
        relative_path=relative_path,
        country="Peru",
        crops=("maize",),
        factors=("precipitation",),
    )


def _context() -> RecommendationContext:
    return RecommendationContext(
        evaluation_id=uuid4(),
        crop_id="maize",
        water_regime="rainfed",
        suitability_mean=0.0,
        factors=(
            RecommendationFactor(
                factor_code="precipitation",
                label="precipitation",
                affected_fraction=1.0,
                dominant=True,
            ),
        ),
    )


def _stored_chunk(
    chunk_id: str,
    *,
    content: str,
    title: str = "Guidance",
    page_start: int = 3,
    page_end: int = 4,
    section: str | None = "Water",
) -> StoredChunk:
    return StoredChunk(
        chunk_id=chunk_id,
        document_id=uuid4(),
        organization="FAO",
        title=title,
        source_roles=("methodology",),
        relative_path="fao/guidance.pdf",
        source_reference=None,
        corpus_version="test-v1",
        page_start=page_start,
        page_end=page_end,
        section=section,
        content=content,
        content_sha256="a" * 64,
        crops=(),
        factors=("precipitation",),
    )


def _index() -> EmbeddingIndex:
    return EmbeddingIndex(
        index_id=uuid4(),
        provider="fake",
        model="fake-embedding",
        dimensions=3,
        index_version="test-v1",
        created_at=datetime.now(UTC),
    )


def _retrieved(context: RecommendationContext) -> RetrievedKnowledge:
    return RetrievedKnowledge(
        retrieval_run_id=uuid4(),
        evaluation_id=context.evaluation_id,
        crop_id=context.crop_id,
        water_regime=context.water_regime,
        limiting_factors=("precipitation",),
        retrieval_status=RetrievalStatus.AVAILABLE,
        query='"maize" OR "precipitation"',
        corpus_version="test-v1",
        retrieval_version="hybrid-rrf-v1",
        embedding_index=_index(),
        evidence=(
            EvidenceItem(
                evidence_id="SOURCE_1",
                chunk_id="chunk-a",
                organization="FAO",
                title="Guidance",
                source_roles=("methodology",),
                page_start=3,
                page_end=4,
                section="Water",
                content="Evidence text",
                source_reference="fao/guidance.pdf",
                lexical_rank=1,
                vector_rank=1,
                fused_score=1.0,
            ),
        ),
    )


def _recommendation(citation_id: str = "SOURCE_1") -> StructuredRecommendation:
    return StructuredRecommendation(
        summary="Summary",
        observations=("Observation",),
        scenario_interpretation="Rainfed scientific outcome remains authoritative.",
        recommendations=(
            RecommendationItem(
                text="Review water management options.",
                rationale="The supplied evidence discusses water management.",
                citation_ids=(citation_id,),
            ),
        ),
        uncertainties=("Local irrigation availability is unknown.",),
        citation_ids=(citation_id,),
    )


class _FakeEmbeddings:
    provider_name = "fake"
    model = "fake-embedding"
    dimensions = 3

    def __init__(self) -> None:
        self.calls: list[tuple[str, ...]] = []

    def embed(self, texts: tuple[str, ...]) -> EmbeddingBatch:
        self.calls.append(texts)
        return EmbeddingBatch(
            vectors=tuple(EmbeddingVector((1.0, 0.0, 0.0)) for _ in texts),
            input_tokens=len(texts),
            request_count=1,
        )


class _Catalog:
    def __init__(self, content: bytes) -> None:
        self.content = content

    def load_manifest(self) -> CorpusManifest:
        return CorpusManifest(corpus_version="test-v1", sources=(_source(),))

    def read_source(self, source: CorpusSource) -> bytes:
        assert source.source_id == "source-1"
        return self.content


class _Extractor:
    def extract(self, content: bytes) -> ExtractedDocument:
        token = content.decode("utf-8")
        text = "Heading\n" + " ".join([token] * 1350)
        return ExtractedDocument(
            pages=(ExtractedPage(page_number=1, text=text),),
            total_pages=1,
            pages_extracted=1,
        )


class _KnowledgeRepository:
    def __init__(self) -> None:
        self.documents: dict[tuple[str, str, str], KnowledgeDocument] = {}
        self.saved_chunks = 0
        self.persisted: list[RetrievedKnowledge] = []
        self.lexical: tuple[LexicalSearchHit, ...] = ()
        self.vectors: tuple[VectorSearchCandidate, ...] = ()
        self.last_filters: tuple[str, tuple[str, ...], str] | None = None

    def find_document(
        self, source_id: str, source_sha256: str, corpus_version: str
    ) -> KnowledgeDocument | None:
        return self.documents.get((source_id, source_sha256, corpus_version))

    def ensure_embedding_index(self, index: EmbeddingIndex) -> EmbeddingIndex:
        return index

    def reusable_embeddings(
        self, chunk_ids: tuple[str, ...], embedding_index_id: UUID
    ) -> dict[str, tuple[float, ...]]:
        assert embedding_index_id
        assert all(chunk_ids)
        return {}

    def save_document(
        self,
        document: KnowledgeDocument,
        chunks: tuple[object, ...],
        embedding_index: EmbeddingIndex,
        embeddings: dict[str, tuple[float, ...]],
        embedding_input_tokens: int | None,
        embedding_request_count: int,
    ) -> None:
        del embedding_index, embeddings, embedding_input_tokens, embedding_request_count
        key = (document.source.source_id, document.source_sha256, document.corpus_version)
        self.documents[key] = document
        self.saved_chunks += len(chunks)

    def lexical_search(
        self,
        query: str,
        crop_id: str,
        factor_codes: tuple[str, ...],
        corpus_version: str,
        limit: int,
    ) -> tuple[LexicalSearchHit, ...]:
        assert query and limit > 0
        self.last_filters = (crop_id, factor_codes, corpus_version)
        return self.lexical[:limit]

    def vector_candidates(
        self,
        crop_id: str,
        factor_codes: tuple[str, ...],
        corpus_version: str,
        embedding_index_id: UUID,
    ) -> tuple[VectorSearchCandidate, ...]:
        assert embedding_index_id
        self.last_filters = (crop_id, factor_codes, corpus_version)
        return self.vectors

    def persist_retrieval(self, retrieved: RetrievedKnowledge) -> None:
        self.persisted.append(retrieved)

class _Retriever:
    def __init__(self, evidence: RetrievedKnowledge) -> None:
        self.evidence = evidence
        self.calls = 0

    def retrieve(self, context: RecommendationContext) -> RetrievedKnowledge:
        assert context.evaluation_id == self.evidence.evaluation_id
        self.calls += 1
        return self.evidence


class _Generator:
    provider_name = "fake"
    model = "fake-recommendation"

    def __init__(self, recommendation: StructuredRecommendation) -> None:
        self.recommendation = recommendation
        self.calls = 0

    def generate(
        self, context: RecommendationContext, evidence: RetrievedKnowledge
    ) -> RecommendationGeneration:
        assert context.evaluation_id == evidence.evaluation_id
        self.calls += 1
        return RecommendationGeneration(
            recommendation=self.recommendation,
            provider=self.provider_name,
            model=self.model,
            response_id="response-1",
            input_tokens=10,
            output_tokens=20,
        )


class _RecommendationRepository:
    def __init__(self) -> None:
        self.runs: list[RecommendationRun] = []

    def find_succeeded_by_cache_key(self, cache_key: str) -> RecommendationRun | None:
        return next(
            (
                run
                for run in self.runs
                if run.cache_key == cache_key and run.status is RecommendationStatus.SUCCEEDED
            ),
            None,
        )

    def save(self, run: RecommendationRun, evidence: RetrievedKnowledge) -> None:
        assert run.evaluation_id == evidence.evaluation_id
        self.runs.append(run)

    def list_for_evaluation(self, evaluation_id: UUID) -> tuple[RecommendationRun, ...]:
        return tuple(run for run in self.runs if run.evaluation_id == evaluation_id)


def test_manifest_resolves_relative_paths_and_rejects_traversal(tmp_path: Path) -> None:
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    pdf = source_dir / "doc.pdf"
    pdf.write_bytes(b"pdf")
    manifest = tmp_path / "corpus.yaml"
    manifest.write_text(
        """corpus_version: test
sources:
  - source_id: one
    organization: FAO
    title: Doc
    language: en
    source_type: pdf
    source_role: methodology
    relative_path: doc.pdf
""",
        encoding="utf-8",
    )
    catalog = YamlFilesystemKnowledgeSourceCatalog(manifest, source_dir)
    source = catalog.load_manifest().sources[0]
    assert catalog.read_source(source) == b"pdf"
    assert source.relative_path == "doc.pdf"

    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace("doc.pdf", "../doc.pdf"),
        encoding="utf-8",
    )
    with pytest.raises(ManifestValidationError):
        catalog.load_manifest()


def test_manifest_missing_source_fails_when_read(tmp_path: Path) -> None:
    manifest = tmp_path / "corpus.yaml"
    manifest.write_text(
        """corpus_version: test
sources:
  - source_id: one
    organization: FAO
    title: Doc
    language: en
    source_type: pdf
    source_role: methodology
    relative_path: missing.pdf
""",
        encoding="utf-8",
    )
    catalog = YamlFilesystemKnowledgeSourceCatalog(manifest, tmp_path)
    with pytest.raises(FileNotFoundError):
        catalog.read_source(catalog.load_manifest().sources[0])


def test_packaged_manifest_loads_without_external_source_directory() -> None:
    catalog = YamlFilesystemKnowledgeSourceCatalog()
    manifest = catalog.load_manifest()

    assert manifest.corpus_version == "2026-09-19"
    assert manifest.sources
    with pytest.raises(RuntimeError, match="VIA_KNOWLEDGE_SOURCE_DIR"):
        catalog.read_source(manifest.sources[0])


def test_repo_taxonomy_covers_known_and_future_factors() -> None:
    taxonomy = load_taxonomy()
    assert "déficit hídrico" in taxonomy.expand_factor("precipitation")
    assert "profundidad efectiva" in taxonomy.expand_factor("parameter_soildepth")
    assert "maíz amarillo duro" in taxonomy.expand_crop("maize")
    assert "riego" in taxonomy.expand_water_regime("irrigated")
    assert taxonomy.expand_factor("parameter_custom")


def test_blank_pdf_is_marked_as_needing_ocr() -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    buffer = io.BytesIO()
    writer.write(buffer)
    extracted = PyPdfDocumentTextExtractor().extract(buffer.getvalue())
    assert extracted.total_pages == 1
    assert extracted.needs_ocr is True
    assert extracted.pages[0].page_number == 1


def test_chunking_is_deterministic_and_preserves_page_provenance() -> None:
    chunker = DeterministicKnowledgeChunker()
    text = "Section heading\n" + " ".join(f"word{index}" for index in range(1500))
    extracted = ExtractedDocument(
        pages=(
            ExtractedPage(1, text),
            ExtractedPage(2, "Continuation\n" + " ".join(["water"] * 700)),
        ),
        total_pages=2,
        pages_extracted=2,
    )
    first = chunker.chunk(_source(), "b" * 64, "test-corpus-v1", extracted)
    second = chunker.chunk(_source(), "b" * 64, "test-corpus-v1", extracted)
    assert first == second
    assert len(first) >= 2
    assert all(chunk.page_start >= 1 and chunk.page_end >= chunk.page_start for chunk in first)
    assert all(len(chunk.chunk_id) == 64 and len(chunk.content_sha256) == 64 for chunk in first)
    assert set(first[0].content.split()) & set(first[1].content.split())


@pytest.mark.parametrize(
    "line",
    (
        "8. Riegos",
        "6.1.2 Agua",
        "14. Referencias",
        "10. Fertilización",
        "10.1 Fertilización química",
        "10.1.1 Macronutrientes (Nutrientes primarios)",
        "2. REQUERIMIENTOS AGROCLIMÁTICOS",
        "2.1 Exigencias en clima",
        "4.5 Riego",
        "1. Introduction",
        "10. Agro-ecological Zones",
    ),
)
def test_numbered_heading_detection_preserves_structural_headings(line: str) -> None:
    assert _looks_like_heading(line) is True


@pytest.mark.parametrize(
    "line",
    (
        "2018 Producción nacional de maíz",
        "20 kg por hectárea",
        "2024 resultados del cultivo",
        "0.3 1.0",
        "1.0 meq de Ca/100 g = 500 kg de Ca/ha",
        "4. U daytime>emisee",
        "3. U daytime5-Imina",
        "139. https://doi.org/10.1080/00103620009370424",
        "1. Introducción 9",
        "10. Fertilización 82",
        "34. Corrigendum 288",
        "1. Plumas libre de virus 1. Se uniformiza la variedad",
        "4. Number of individual growing periods;",
        "4. Snow balance (Sb), and",
        "5. Module III (Agro-climatic",
        "1.2.3.4.5 Too deep",
        "1.123 Invalid component",
    ),
)
def test_numbered_heading_detection_rejects_data_and_list_items(line: str) -> None:
    assert _looks_like_heading(line) is False


@pytest.mark.parametrize(
    "line",
    (
        "MANEJO DEL RIEGO",
        "CALCULATION PROCEDURES",
        "REFERENCES",
        "REFERENCIAS",
        "INTRODUCTION",
        "CONCLUSIONES",
    ),
)
def test_uppercase_heading_detection_preserves_textual_headings(line: str) -> None:
    assert _looks_like_heading(line) is True


@pytest.mark.parametrize(
    "line",
    (
        "TOTAL",
        "MEAN",
        "CROP-",
        "LAND",
        "SHRUB",
        "COVER",
        "DATA",
        "DAVIS",
        "COPENHAGEN",
        "YANGAMBI",
        "HIGH INT LOW",
        "H, I, L H, I H, I H, I",
        "CROP NAME",
        "JJA SOND",
        "BRAW LEY",
        "MOM. MIMSNOINIMPINMKIIMBO",
        "STATIONDAVIS CALIFORNIA.",
        "NON-FORAGE CROP///",
        "𝑅) IIASA",
        "+----BL-:CR.",
        "DDTDDF",
        "RLANX",
        "DOSIS 20 KG/HA",
        (
            "MANEJO DEL RIEGO Y RECOMENDACIONES AGRONÓMICAS PARA EL CULTIVO "
            "BAJO CONDICIONES DE DISPONIBILIDAD HÍDRICA LIMITADA"
        ),
    ),
)
def test_uppercase_heading_detection_rejects_table_and_ocr_fragments(
    line: str,
) -> None:
    assert _looks_like_heading(line) is False


def test_heading_detection_uses_raw_spacing_before_content_normalization() -> None:
    raw_table_row = "NITRÓGENO    FÓSFORO    POTASIO"
    normalized_table_row = "NITRÓGENO FÓSFORO POTASIO"

    assert _looks_like_heading(raw_table_row, normalized_table_row) is False

    chunker = DeterministicKnowledgeChunker()
    extracted = ExtractedDocument(
        pages=(
            ExtractedPage(
                1,
                "MANEJO DEL RIEGO\n"
                f"{raw_table_row}\n"
                "Contenido agronómico que continúa bajo el heading real.",
            ),
        ),
        total_pages=1,
        pages_extracted=1,
    )

    chunks = chunker.chunk(_source(), "b" * 64, "test-corpus-v1", extracted)

    assert len(chunks) == 1
    assert chunks[0].section == "MANEJO DEL RIEGO"
    assert normalized_table_row in chunks[0].content


def test_chunking_does_not_cross_detected_sections() -> None:
    chunker = DeterministicKnowledgeChunker()

    water_content = " ".join(["water"] * 220)
    irrigation_content = " ".join(["irrigation"] * 240)

    extracted = ExtractedDocument(
        pages=(
            ExtractedPage(
                1,
                f"6.1.2 Agua\n{water_content}\n"
                f"8. Riegos\n{irrigation_content}",
            ),
        ),
        total_pages=1,
        pages_extracted=1,
    )

    chunks = chunker.chunk(_source(), "b" * 64, "test-corpus-v1", extracted)

    assert len(chunks) == 2
    assert chunks[0].section == "6.1.2 Agua"
    assert chunks[1].section == "8. Riegos"

    assert "water" in chunks[0].content
    assert "irrigation" not in chunks[0].content

    assert "irrigation" in chunks[1].content
    assert "water" not in chunks[1].content

def test_ingestion_is_sha_idempotent_and_reingests_changed_source() -> None:
    catalog = _Catalog(b"alpha")
    embeddings = _FakeEmbeddings()
    repository = _KnowledgeRepository()
    service = KnowledgeIngestionService(
        catalog=catalog,
        extractor=_Extractor(),
        chunker=DeterministicKnowledgeChunker(),
        embeddings=embeddings,
        repository=repository,
        embedding_index_version="test-v1",
        embedding_batch_size=1,
    )
    first = service.ingest()
    first_embedding_calls = len(embeddings.calls)
    second = service.ingest()
    assert first.sources[0].source_sha256 != ""
    assert first.sources[0].reused is False
    assert second.sources[0].reused is True
    assert len(embeddings.calls) == first_embedding_calls

    catalog.content = b"beta"
    third = service.ingest()
    assert third.sources[0].source_sha256 != first.sources[0].source_sha256
    assert third.sources[0].reused is False
    assert len(embeddings.calls) > first_embedding_calls

def test_ingestion_embeds_document_and_section_context() -> None:
    catalog = _Catalog(b"alpha")
    embeddings = _FakeEmbeddings()
    repository = _KnowledgeRepository()

    service = KnowledgeIngestionService(
        catalog=catalog,
        extractor=_Extractor(),
        chunker=DeterministicKnowledgeChunker(),
        embeddings=embeddings,
        repository=repository,
        embedding_index_version="test-v2",
        embedding_batch_size=10,
    )

    service.ingest()

    embedded_texts = tuple(
        text
        for call in embeddings.calls
        for text in call
    )

    assert embedded_texts
    assert any("Document:" in text for text in embedded_texts)
    assert any("Heading" in text for text in embedded_texts)

def test_dry_run_does_not_embed_or_persist() -> None:
    catalog = _Catalog(b"alpha")
    embeddings = _FakeEmbeddings()
    repository = _KnowledgeRepository()
    service = KnowledgeIngestionService(
        catalog=catalog,
        extractor=_Extractor(),
        chunker=DeterministicKnowledgeChunker(),
        embeddings=embeddings,
        repository=repository,
        embedding_index_version="test-v1",
    )
    report = service.ingest(dry_run=True)
    assert report.documents_discovered == 1
    assert report.chunks_generated > 0
    assert report.chunks_embedded == 0
    assert embeddings.calls == []
    assert repository.documents == {}


def test_hybrid_retrieval_uses_crop_factor_filters_and_deterministic_rrf() -> None:
    context = _context()
    repository = _KnowledgeRepository()
    first = _stored_chunk("chunk-a", content="water deficit evidence")
    second = _stored_chunk("chunk-b", content="rainfall evidence")
    repository.lexical = (
        LexicalSearchHit(chunk=second, rank=1, score=1.0),
        LexicalSearchHit(chunk=first, rank=2, score=0.8),
    )
    repository.vectors = (
        VectorSearchCandidate(chunk=first, vector=(1.0, 0.0, 0.0)),
        VectorSearchCandidate(chunk=second, vector=(0.0, 1.0, 0.0)),
    )
    embeddings = _FakeEmbeddings()
    retriever = HybridKnowledgeRetriever(
        repository=repository,
        embeddings=embeddings,
        taxonomy=Taxonomy(
            version="test",
            factors={"precipitation": ("rainfall", "water deficit")},
            crops={"maize": ("corn",)},
            water_regimes={"rainfed": ("rainfed",)},
        ),
        embedding_index=configured_embedding_index(embeddings, "test-v1"),
        corpus_version="test-v1",
        vector_top_k=2,
        lexical_top_k=2,
        final_top_k=2,
    )
    result = retriever.retrieve(context)
    assert result.retrieval_status is RetrievalStatus.AVAILABLE
    assert [item.evidence_id for item in result.evidence] == ["SOURCE_1", "SOURCE_2"]
    assert result.evidence[0].chunk_id == "chunk-a"
    assert repository.last_filters == ("maize", ("precipitation",), "test-v1")
    assert repository.persisted == [result]
    assert all(not Path(item.source_reference).is_absolute() for item in result.evidence)


def test_hybrid_retrieval_v3_filters_noise_with_factor_focused_query() -> None:
    context = _context()
    repository = _KnowledgeRepository()

    references = _stored_chunk(
        "chunk-references",
        content="Maize rainfall water deficit bibliography references.",
        title="Maize Manual",
        page_start=134,
        page_end=146,
        section="14. Referencias",
    )
    front_matter = _stored_chunk(
        "chunk-front-matter",
        content=(
            "ISBN 123 Authors Example Editor Example Published 2020 "
            "1. Introduction 9 2. Water 54 3. Irrigation 68 "
            "4. References 132"
        ),
        title="Maize Manual",
        page_start=4,
        page_end=7,
        section="Maize Manual",
    )
    irrigation = _stored_chunk(
        "chunk-irrigation",
        content=(
            "Water availability is critical for maize. Rainfall deficits "
            "during sensitive stages can reduce yield."
        ),
        title="Maize Manual",
        page_start=70,
        page_end=71,
        section="8. Riegos",
    )
    gaez = _stored_chunk(
        "chunk-gaez",
        content=(
            "Rain-fed and irrigated land evaluation considers water supply "
            "and soil limitations."
        ),
        title="GAEZ v4 Model Documentation",
        page_start=132,
        page_end=134,
        section="SOIL AND TERRAIN EVALUATION",
    )

    repository.lexical = (
        LexicalSearchHit(chunk=references, rank=1, score=1.0),
        LexicalSearchHit(chunk=front_matter, rank=2, score=0.9),
        LexicalSearchHit(chunk=irrigation, rank=3, score=0.8),
        LexicalSearchHit(chunk=gaez, rank=4, score=0.7),
    )
    repository.vectors = (
        VectorSearchCandidate(
            chunk=references,
            vector=(1.0, 0.0, 0.0),
        ),
        VectorSearchCandidate(
            chunk=front_matter,
            vector=(0.99, 0.01, 0.0),
        ),
        VectorSearchCandidate(
            chunk=irrigation,
            vector=(0.95, 0.05, 0.0),
        ),
        VectorSearchCandidate(
            chunk=gaez,
            vector=(0.90, 0.10, 0.0),
        ),
    )

    embeddings = _FakeEmbeddings()

    retriever = HybridKnowledgeRetriever(
        repository=repository,
        embeddings=embeddings,
        taxonomy=Taxonomy(
            version="test",
            factors={
                "precipitation": (
                    "rainfall",
                    "water deficit",
                    "water availability",
                )
            },
            crops={
                "maize": (
                    "corn",
                    "yellow maize",
                )
            },
            water_regimes={
                "rainfed": (
                    "rain-fed",
                    "secano",
                )
            },
        ),
        embedding_index=configured_embedding_index(
            embeddings,
            "test-v1",
        ),
        corpus_version="test-v1",
        vector_top_k=2,
        lexical_top_k=2,
        final_top_k=2,
    )

    first = retriever.retrieve(context)
    second = retriever.retrieve(context)

    assert first.retrieval_status is RetrievalStatus.AVAILABLE
    assert first.retrieval_version == "hybrid-rrf-v3"

    assert [
        item.chunk_id
        for item in first.evidence
    ] == [
        "chunk-irrigation",
        "chunk-gaez",
    ]

    assert [
        item.chunk_id
        for item in second.evidence
    ] == [
        item.chunk_id
        for item in first.evidence
    ]

    assert [
        item.section
        for item in first.evidence
    ] == [
        "8. Riegos",
        "SOIL AND TERRAIN EVALUATION",
    ]

    assert "chunk-references" not in {
        item.chunk_id
        for item in first.evidence
    }
    assert "chunk-front-matter" not in {
        item.chunk_id
        for item in first.evidence
    }

    assert len(embeddings.calls) == 2

    semantic_query = embeddings.calls[0][0]

    assert semantic_query.startswith(
        "Agronomic evidence about precipitation, rainfall, water deficit"
    )
    assert "for maize." in semantic_query
    assert "Scenario context: rainfed conditions." in semantic_query
    assert "rainfall" in semantic_query
    assert "water deficit" in semantic_query
    assert "rainfed" in semantic_query
    assert " OR " not in semantic_query
    assert '"' not in semantic_query

    lexical_line, semantic_line = first.query.splitlines()

    assert lexical_line.startswith("lexical: ")
    assert semantic_line.startswith("semantic: ")

    assert '"maize"' in lexical_line
    assert '"precipitation"' in lexical_line
    assert '"rainfall"' in lexical_line
    assert '"water deficit"' in lexical_line
    assert '"rainfed"' in lexical_line

    assert '"corn"' not in lexical_line
    assert '"yellow maize"' not in lexical_line

    assert semantic_line.removeprefix("semantic: ") == semantic_query


def test_hybrid_retrieval_v3_keeps_water_regime_secondary_to_soil_factor() -> None:
    context = RecommendationContext(
        evaluation_id=uuid4(),
        crop_id="maize",
        water_regime="irrigated",
        suitability_mean=12.5,
        factors=(
            RecommendationFactor(
                factor_code="parameter_soildepth",
                label="soil depth",
                affected_fraction=1.0,
                dominant=True,
            ),
        ),
    )

    repository = _KnowledgeRepository()

    soil = _stored_chunk(
        "chunk-soil-depth",
        content=(
            "Rooting conditions and effective soil depth can limit "
            "crop suitability."
        ),
        title="GAEZ",
        section="Rooting conditions",
    )

    repository.lexical = (
        LexicalSearchHit(
            chunk=soil,
            rank=1,
            score=1.0,
        ),
    )
    repository.vectors = (
        VectorSearchCandidate(
            chunk=soil,
            vector=(1.0, 0.0, 0.0),
        ),
    )

    embeddings = _FakeEmbeddings()

    retriever = HybridKnowledgeRetriever(
        repository=repository,
        embeddings=embeddings,
        taxonomy=Taxonomy(
            version="test",
            factors={
                "parameter_soildepth": (
                    "soil depth",
                    "effective soil depth",
                    "rooting depth",
                    "shallow soil",
                )
            },
            crops={
                "maize": (
                    "corn",
                )
            },
            water_regimes={
                "irrigated": (
                    "irrigation",
                    "bajo riego",
                    "irrigado",
                    "riego",
                )
            },
        ),
        embedding_index=configured_embedding_index(
            embeddings,
            "test-v1",
        ),
        corpus_version="test-v1",
        vector_top_k=1,
        lexical_top_k=1,
        final_top_k=1,
    )

    result = retriever.retrieve(context)

    semantic_query = embeddings.calls[0][0]
    lexical_line, semantic_line = result.query.splitlines()

    assert result.retrieval_version == "hybrid-rrf-v3"

    assert "soil depth" in semantic_query
    assert "effective soil depth" in semantic_query
    assert "rooting depth" in semantic_query
    assert "shallow soil" in semantic_query

    assert "parameter_soildepth" not in semantic_query

    assert "Scenario context: irrigated conditions." in semantic_query

    assert "irrigation" not in semantic_query
    assert "bajo riego" not in semantic_query
    assert "irrigado" not in semantic_query
    assert "riego" not in semantic_query

    assert '"irrigated"' in lexical_line
    assert '"irrigation"' in lexical_line
    assert '"riego"' in lexical_line

    assert semantic_line.removeprefix("semantic: ") == semantic_query


def test_hybrid_retrieval_v3_preserves_useful_introduction_sections() -> None:
    context = _context()
    repository = _KnowledgeRepository()

    introduction = _stored_chunk(
        "chunk-introduction",
        content=(
            "Maize adapts to a range of agroclimatic conditions and "
            "water availability affects crop development."
        ),
        title="Maize Manual",
        page_start=11,
        page_end=14,
        section="1. Introduction",
    )

    repository.lexical = (
        LexicalSearchHit(
            chunk=introduction,
            rank=1,
            score=1.0,
        ),
    )
    repository.vectors = (
        VectorSearchCandidate(
            chunk=introduction,
            vector=(1.0, 0.0, 0.0),
        ),
    )

    embeddings = _FakeEmbeddings()

    retriever = HybridKnowledgeRetriever(
        repository=repository,
        embeddings=embeddings,
        taxonomy=Taxonomy(
            version="test",
            factors={
                "precipitation": (
                    "rainfall",
                    "water deficit",
                )
            },
            crops={"maize": ("corn",)},
            water_regimes={"rainfed": ("rain-fed",)},
        ),
        embedding_index=configured_embedding_index(
            embeddings,
            "test-v1",
        ),
        corpus_version="test-v1",
        vector_top_k=1,
        lexical_top_k=1,
        final_top_k=1,
    )

    result = retriever.retrieve(context)

    assert result.retrieval_status is RetrievalStatus.AVAILABLE
    assert len(result.evidence) == 1
    assert result.evidence[0].chunk_id == "chunk-introduction"
    assert result.evidence[0].section == "1. Introduction"


def test_recommendation_validates_citations_and_reuses_cache() -> None:
    context = _context()
    evidence = _retrieved(context)
    retriever = _Retriever(evidence)
    generator = _Generator(_recommendation())
    repository = _RecommendationRepository()
    service = RecommendationApplicationService(
        retriever=retriever,
        generator=generator,
        repository=repository,
    )
    first = service.generate(context)
    second = service.generate(context)
    third = service.generate(context, force_regenerate=True)
    assert first.status is RecommendationStatus.SUCCEEDED
    assert second.run_id == first.run_id
    assert third.run_id != first.run_id
    assert generator.calls == 2

    invalid_generator = _Generator(_recommendation("SOURCE_999"))
    invalid_service = RecommendationApplicationService(
        retriever=_Retriever(evidence),
        generator=invalid_generator,
        repository=_RecommendationRepository(),
    )
    failed = invalid_service.generate(context)
    assert failed.status is RecommendationStatus.FAILED
    assert failed.recommendation is None
    assert failed.failure_reason == "generation_failed:InvalidRecommendationError"


def test_recommendation_without_item_citation_is_rejected() -> None:
    context = _context()
    evidence = _retrieved(context)
    invalid = StructuredRecommendation(
        summary="Summary",
        observations=(),
        scenario_interpretation="Interpretation",
        recommendations=(RecommendationItem("Action", "Reason", ()),),
        uncertainties=(),
        citation_ids=("SOURCE_1",),
    )
    service = RecommendationApplicationService(
        retriever=_Retriever(evidence),
        generator=_Generator(invalid),
        repository=_RecommendationRepository(),
    )
    assert service.generate(context).status is RecommendationStatus.FAILED


def test_openai_embedding_key_is_lazy() -> None:
    provider = OpenAIEmbeddingProvider(api_key=None, model="embedding", dimensions=3)
    assert provider.model == "embedding"
    with pytest.raises(MissingOpenAIAPIKeyError):
        provider.embed(("query",))


def test_openai_responses_adapter_uses_strict_schema_and_no_tools(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    response = SimpleNamespace(
        id="resp-1",
        status="completed",
        output_text=json.dumps(
            {
                "summary": "Summary",
                "observations": ["Observation"],
                "scenario_interpretation": "Rainfed remains rainfed.",
                "recommendations": [
                    {
                        "text": "Action",
                        "rationale": "Reason",
                        "citation_ids": ["SOURCE_1"],
                    }
                ],
                "uncertainties": ["Irrigation availability is unknown."],
                "citation_ids": ["SOURCE_1"],
            }
        ),
        usage=SimpleNamespace(input_tokens=11, output_tokens=7),
    )

    class _Responses:
        def create(self, **kwargs: object) -> object:
            captured.update(kwargs)
            return response

    class _FakeOpenAI:
        def __init__(self, *, api_key: str) -> None:
            assert api_key == "test-key"
            self.responses = _Responses()

    monkeypatch.setattr(openai_knowledge, "OpenAI", _FakeOpenAI)
    context = _context()
    generation = OpenAIRecommendationGenerator(
        api_key="test-key", model="test-model"
    ).generate(context, _retrieved(context))
    assert generation.recommendation.citation_ids == ("SOURCE_1",)
    assert captured["tools"] == []
    assert captured["store"] is False
    text_config = captured["text"]
    assert isinstance(text_config, dict)
    assert text_config["format"]["strict"] is True
    assert text_config["format"]["schema"]["additionalProperties"] is False
    payload = json.loads(str(captured["input"]))
    assert payload["scientific_context"]["suitability_mean"] == 0.0
    assert payload["scientific_context"]["water_regime"] == "rainfed"
    instructions = str(captured["instructions"]).lower()
    assert "untrusted" in instructions
    assert "irrigation" in instructions


@pytest.mark.integration
def test_real_openai_embedding_only_with_explicit_opt_in() -> None:
    if os.getenv("VIA_RUN_OPENAI_INTEGRATION") != "1":
        pytest.skip("real OpenAI integration requires VIA_RUN_OPENAI_INTEGRATION=1")
    api_key = os.getenv("VIA_OPENAI_API_KEY")
    if not api_key:
        pytest.skip("real OpenAI integration requires VIA_OPENAI_API_KEY")
    result = OpenAIEmbeddingProvider(
        api_key=api_key,
        model=os.getenv("VIA_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        dimensions=1536,
    ).embed(("VIA integration smoke",))
    assert len(result.vectors) == 1
    assert len(result.vectors[0].values) == 1536
