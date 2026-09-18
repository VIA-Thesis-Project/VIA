# VIA agronomic knowledge corpus

The canonical declarative catalog and retrieval taxonomy are packaged at `backend/src/via_backend/resources/knowledge/`. This directory documents their maintenance contract. The source PDFs stay outside the repository and are resolved exclusively below `VIA_KNOWLEDGE_SOURCE_DIR`.

The current local corpus is expected at `C:\Users\Usuario\Documents\Tesis\Implementation\KnowledgeCorpus`. Production can mount the same logical corpus at `/var/lib/via/knowledge/sources` and set `VIA_KNOWLEDGE_SOURCE_DIR` to that path.

To add a document without changing application code:

1. Copy the PDF into the external corpus directory.
2. Add one entry with a safe `relative_path` to `backend/src/via_backend/resources/knowledge/corpus.yaml`.
3. Run `via-knowledge ingest` (or first use `via-knowledge ingest --dry-run`).

`--dry-run` validates the manifest and paths, extracts native PDF text, and performs deterministic chunking without a database write or OpenAI request. PDFs with insufficient native text are reported as `needs_ocr`; OCR is intentionally not performed by default.

Installed applications load `corpus.yaml` and `taxonomy.yaml` through Python package resources. Deployments may override them with `VIA_KNOWLEDGE_MANIFEST_PATH` and `VIA_KNOWLEDGE_TAXONOMY_PATH`; those overrides do not change the external PDF source root.
