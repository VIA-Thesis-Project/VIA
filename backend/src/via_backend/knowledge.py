"""Administrative CLI for the VIA agronomic knowledge corpus."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import cast

from via_backend.config import Settings
from via_backend.contexts.decision_support.application.knowledge_models import (
    KnowledgeDocumentStatus,
)
from via_backend.contexts.decision_support.application.knowledge_ports import (
    IKnowledgeCorpusRepository,
)
from via_backend.contexts.decision_support.application.knowledge_services import (
    DeterministicKnowledgeChunker,
    KnowledgeIngestionService,
)
from via_backend.contexts.decision_support.infrastructure.knowledge_manifest import (
    YamlFilesystemKnowledgeSourceCatalog,
)
from via_backend.contexts.decision_support.infrastructure.openai_knowledge import (
    OpenAIEmbeddingProvider,
)
from via_backend.contexts.decision_support.infrastructure.pdf_extractor import (
    PyPdfDocumentTextExtractor,
)
from via_backend.contexts.decision_support.infrastructure.postgresql_repositories import (
    PostgreSQLKnowledgeCorpusRepository,
)
from via_backend.infrastructure import create_database


class _DryRunRepository:
    """Fail loudly if a dry run ever tries to touch persistence."""

    def __getattr__(self, name: str) -> object:
        raise RuntimeError(f"Dry-run ingestion attempted repository operation {name!r}.")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="via-knowledge")
    subcommands = parser.add_subparsers(dest="command", required=True)
    ingest = subcommands.add_parser("ingest", help="Ingest the configured knowledge corpus.")
    ingest.add_argument("--manifest", type=Path)
    ingest.add_argument("--source-dir", type=Path)
    ingest.add_argument("--dry-run", action="store_true")
    return parser


def _run_ingest(args: argparse.Namespace) -> int:
    settings = Settings.from_env()
    manifest_path = args.manifest or settings.knowledge_manifest
    source_dir = args.source_dir or settings.knowledge_source_dir
    if source_dir is None:
        raise SystemExit(
            "VIA_KNOWLEDGE_SOURCE_DIR or --source-dir is required for knowledge ingestion."
        )

    catalog = YamlFilesystemKnowledgeSourceCatalog(manifest_path, source_dir)
    embeddings = OpenAIEmbeddingProvider(
        api_key=settings.openai_api_key,
        model=settings.openai_embedding_model,
        dimensions=settings.openai_embedding_dimensions,
    )
    engine = None
    if args.dry_run:
        repository = cast(IKnowledgeCorpusRepository, _DryRunRepository())
    else:
        if settings.database_url is None:
            raise SystemExit("VIA_DATABASE_URL is required for knowledge ingestion.")
        engine, sessions = create_database(settings.database_url)
        repository = PostgreSQLKnowledgeCorpusRepository(sessions)

    service = KnowledgeIngestionService(
        catalog=catalog,
        extractor=PyPdfDocumentTextExtractor(),
        chunker=DeterministicKnowledgeChunker(),
        embeddings=embeddings,
        repository=repository,
        embedding_index_version=settings.rag_embedding_index_version,
    )
    try:
        report = service.ingest(dry_run=args.dry_run)
    finally:
        if engine is not None:
            engine.dispose()

    reused = sum(item.reused for item in report.sources)
    ready = sum(item.status is KnowledgeDocumentStatus.READY for item in report.sources)
    failures = sum(item.status is KnowledgeDocumentStatus.FAILED for item in report.sources)
    needs_ocr = sum(item.status is KnowledgeDocumentStatus.NEEDS_OCR for item in report.sources)
    warning_count = sum(len(item.warnings) for item in report.sources)
    print(f"corpus_version={report.corpus_version}")
    print(f"discovered={report.documents_discovered}")
    print(f"ready={ready}")
    print(f"reused={reused}")
    print(f"pages_extracted={report.pages_extracted}")
    print(f"chunks={report.chunks_generated}")
    print(f"embedded={report.chunks_embedded}")
    print(f"needs_ocr={needs_ocr}")
    print(f"warnings={warning_count}")
    print(f"failures={failures}")
    for item in report.sources:
        if item.warnings:
            print(
                f"source={item.source_id} status={item.status.value} "
                f"warnings={' | '.join(item.warnings)}"
            )
    return 1 if failures else 0


def main() -> int:
    args = _parser().parse_args()
    if args.command == "ingest":
        return _run_ingest(args)
    raise AssertionError(f"Unhandled command {args.command!r}")


if __name__ == "__main__":
    raise SystemExit(main())
