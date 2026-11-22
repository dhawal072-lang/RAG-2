from src.db.manifest import initialize_manifest, register_document
from src.ingestion.scanner import scan_pdf_directory


def discover_documents(directory: str):
    initialize_manifest()

    results = []

    for pdf in scan_pdf_directory(directory):
        status = register_document(pdf)

        results.append({
            "filename": pdf["filename"],
            "status": status,
            "sha256": pdf["sha256"]
        })

    return results


if __name__ == "__main__":
    for document in discover_documents("data/pdfs"):
        print(f"{document['status']}: {document['filename']}")