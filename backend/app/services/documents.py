from pathlib import Path

import fitz


class DocumentExtractionError(Exception):
    pass


class DocumentService:
    def extract_pdf(self, path: Path) -> tuple[str, int]:
        try:
            pdf = fitz.open(path)
            pages = [f"[Page {index + 1}]\\n{page.get_text().strip()}" for index, page in enumerate(pdf)]
        except (fitz.FileDataError, OSError) as error:
            raise DocumentExtractionError("The uploaded file could not be read as a PDF.") from error

        text = "\\n\\n".join(pages).strip()
        if not text:
            raise DocumentExtractionError("No extractable text was found. OCR support is planned for scanned PDFs.")
        return text, len(pages)
