import json
import os
import tempfile
from pathlib import Path

from src.db.manifest import (
    initialize_manifest,
    get_pending_documents,
    update_document_status,
)
from src.ingestion.pdf_loader import extract_pdf
from src.ingestion.chunker import chunk_pdf


CHUNK_STORAGE = Path("data/indexes/chunks")


def save_chunks(document_id, chunks):
    CHUNK_STORAGE.mkdir(parents=True, exist_ok=True)

    output_path = CHUNK_STORAGE / f"{document_id}.json"

    fd, temporary_path = tempfile.mkstemp(
        dir=CHUNK_STORAGE,
        suffix=".tmp"
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(chunks, file, ensure_ascii=False, indent=2)

        os.replace(temporary_path, output_path)

    except Exception:
        if os.path.exists(temporary_path):
            os.remove(temporary_path)
        raise

    return output_path


def process_documents():
    initialize_manifest()
    documents = get_pending_documents()

    if not documents:
        print("No pending documents to process.")
        return

    print(f"Found {len(documents)} document(s) to process.")

    for document in documents:
        file_path = document["file_path"]
        filename = document["filename"]
        document_id = document["document_id"]

        print(f"\nProcessing: {filename}")

        try:
            update_document_status(file_path, "processing")

            extracted = extract_pdf(file_path)
            chunks = chunk_pdf(extracted)

            output_path = save_chunks(document_id, chunks)

            update_document_status(
                file_path,
                "completed",
                pages=extracted["total_pages"],
                chunks=len(chunks),
            )

            print(f"  Pages: {extracted['total_pages']}")
            print(f"  Chunks: {len(chunks)}")
            print(f"  Saved: {output_path}")
            print("  Status: completed")

        except Exception as error:
            update_document_status(
                file_path,
                "failed",
                error=str(error),
            )

            print(f"  Status: failed")
            print(f"  Error: {error}")


if __name__ == "__main__":
    process_documents()