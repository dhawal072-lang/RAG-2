
import json
from pathlib import Path

from src.services.summary_service import SummaryService


CHUNK_DIRECTORY = Path("data/indexes/chunks")


def main():
    summary_service = SummaryService()

    chunk_files = sorted(CHUNK_DIRECTORY.glob("*.json"))

    if not chunk_files:
        print("No existing chunk files found.")
        return

    for chunk_file in chunk_files:
        document_id = int(chunk_file.stem)

        with chunk_file.open("r", encoding="utf-8") as file:
            chunks = json.load(file)

        if not chunks:
            print(f"Skipping document {document_id}: no chunks.")
            continue

        filename = chunks[0]["filename"]

        print(f"\nGenerating summary for: {filename}")

        summary = summary_service.generate_summary(
            document_id=document_id,
            filename=filename,
            chunks=chunks
        )

        print("Summary saved:", summary["filename"])


if __name__ == "__main__":
    main()
