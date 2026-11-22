from pathlib import Path
import pymupdf


def extract_pdf(pdf_path: str) -> dict:
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pages = []

    with pymupdf.open(path) as document:
        if document.is_encrypted:
            raise ValueError(f"Encrypted PDF: {pdf_path}")

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            pages.append({
                "page_number": page_number,
                "text": text,
                "character_count": len(text),
                "needs_ocr": len(text) < 30,
            })

        return {
            "filename": path.name,
            "path": str(path.resolve()),
            "total_pages": len(document),
            "pages": pages,
        }