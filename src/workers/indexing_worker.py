
import json
from pathlib import Path

from src.ingestion.index_scanner import discover_documents
from src.ingestion.pdf_loader import extract_pdf
from src.ingestion.chunker import chunk_pdf
from src.db.manifest import (
    get_pending_documents,
    update_document_status,
)
from src.services.summary_service import SummaryService


CHUNK_DIRECTORY = Path("data/indexes/chunks")


def main():
    CHUNK_DIRECTORY.mkdir(parents=True, exist_ok=True)

    summary_service = SummaryService()

    print("Discovering PDF documents...")
    discover_documents("data/pdfs")

    pending_documents = get_pending_documents()

    if not pending_documents:
        print("No pending documents found.")
        return

    for document in pending_documents:
        document_id = document["document_id"]
        file_path = document["file_path"]
        filename = document["filename"]

        try:
            print(f"\nProcessing: {filename}")

            update_document_status(file_path, "processing")

            extracted = extract_pdf(file_path)
            chunks = chunk_pdf(extracted)
            pages = extracted["pages"]

            chunks = chunk_pages(pages)

            for chunk in chunks:
                chunk["document_id"] = document_id
                chunk["filename"] = filename

            chunk_path = CHUNK_DIRECTORY / f"{document_id}.json"

            with chunk_path.open("w", encoding="utf-8") as file:
                json.dump(chunks, file, indent=4, ensure_ascii=False)

            print(f"Saved {len(chunks)} chunks.")

            summary = summary_service.generate_summary(
                document_id=document_id,
                filename=filename,
                chunks=chunks
            )

            print("Summary saved:", summary["filename"])

            update_document_status(
                file_path,
                "completed",
                pages=extracted["total_pages"],
                chunks=len(chunks)
            )

            print(f"Completed: {filename}")

        except Exception as error:
            update_document_status(
                file_path,
                "failed",
                error=str(error)
            )
            print(f"Failed: {filename} — {error}")


if __name__ == "__main__":
    main()
