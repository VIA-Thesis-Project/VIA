"""Native-text PDF extraction for the agronomic knowledge corpus."""

from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader

from ..application.knowledge_models import ExtractedDocument, ExtractedPage


class PyPdfDocumentTextExtractor:
    """Extract native PDF text while preserving one-based page provenance."""

    def __init__(self, *, minimum_text_characters: int = 40) -> None:
        if minimum_text_characters < 1:
            raise ValueError("minimum_text_characters must be positive")
        self._minimum_text_characters = minimum_text_characters

    def extract(self, content: bytes) -> ExtractedDocument:
        reader = PdfReader(BytesIO(content))
        pages: list[ExtractedPage] = []
        warnings: list[str] = []
        pages_extracted = 0
        total_characters = 0
        for index, page in enumerate(reader.pages, 1):
            try:
                text = page.extract_text() or ""
            except Exception as error:
                text = ""
                warnings.append(f"page_{index}_extraction_failed:{type(error).__name__}")
            normalized = text.replace("\x00", "").strip()
            if normalized:
                pages_extracted += 1
                total_characters += len(normalized)
            else:
                warnings.append(f"page_{index}_has_no_native_text")
            pages.append(ExtractedPage(page_number=index, text=normalized))
        needs_ocr = total_characters < self._minimum_text_characters
        if needs_ocr:
            warnings.append("native_text_layer_insufficient_needs_ocr")
        return ExtractedDocument(
            pages=tuple(pages),
            total_pages=len(reader.pages),
            pages_extracted=pages_extracted,
            warnings=tuple(warnings),
            needs_ocr=needs_ocr,
        )
