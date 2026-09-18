# VIA agronomic knowledge corpus

This directory versions only the declarative catalog and retrieval taxonomy. The source PDFs stay outside the repository and are resolved below `VIA_KNOWLEDGE_SOURCE_DIR`.

The current local corpus is expected at `C:\Users\Usuario\Documents\Tesis\Implementation\KnowledgeCorpus`. Production can mount the same logical corpus at `/var/lib/via/knowledge/sources` and set `VIA_KNOWLEDGE_SOURCE_DIR` to that path.

To add a document without changing application code:

1. Copy the PDF into the external corpus directory.
2. Add one entry with a safe `relative_path` to `knowledge/corpus.yaml`.
3. Run `via-knowledge ingest` (or first use `via-knowledge ingest --dry-run`).

`--dry-run` validates the manifest and paths, extracts native PDF text, and performs deterministic chunking without a database write or OpenAI request. PDFs with insufficient native text are reported as `needs_ocr`; OCR is intentionally not performed by default.

