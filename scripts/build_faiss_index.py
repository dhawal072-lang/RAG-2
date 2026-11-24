
import json
from pathlib import Path

from src.indexing.embedder import Embedder
from src.indexing.faiss_index import build_faiss_index

CHUNK_DIRECTORY = Path("data/indexes/chunks")


def main():
    all_chunks = []

    for file_path in sorted(CHUNK_DIRECTORY.glob("*.json")):
        document_id = int(file_path.stem)

        with file_path.open("r", encoding="utf-8") as file:
            chunks = json.load(file)

        for chunk in chunks:
            chunk["document_id"] = document_id

        all_chunks.extend(chunks)

    if not all_chunks:
        print("No chunks found.")
        return

    print(f"Loaded {len(all_chunks)} chunks.")

    embedder = Embedder()
    embedded_chunks = embedder.encode_chunks(all_chunks)

    print("Embeddings generated.")

    index = build_faiss_index(embedded_chunks)

    print("FAISS index built successfully.")
    print("Vectors indexed:", index.ntotal)
    print("Vector dimensions:", index.d)


if __name__ == "__main__":
    main()
