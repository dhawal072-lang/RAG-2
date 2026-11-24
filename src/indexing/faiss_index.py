
import faiss
import numpy as np
import json
from pathlib import Path


INDEX_DIRECTORY = Path("data/indexes/faiss")


def build_faiss_index(embedded_chunks):
    if not embedded_chunks:
        raise ValueError("No embedded chunks provided.")

    vectors = np.array(
        [chunk["embedding"] for chunk in embedded_chunks],
        dtype="float32"
    )

    dimension = vectors.shape[1]

    # Inner product works as cosine similarity
    # because our embeddings are normalized.
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    INDEX_DIRECTORY.mkdir(parents=True, exist_ok=True)

    faiss.write_index(
        index,
        str(INDEX_DIRECTORY / "documents.faiss")
    )


    metadata = [
        {
            "document_id": chunk["document_id"],
            "filename": chunk["filename"],
            "page_number": chunk["page_number"],
            "text": chunk["text"],
            "chunk_id": chunk["chunk_id"]
        }
        for chunk in embedded_chunks
    ]

    with (INDEX_DIRECTORY / "metadata.json").open(
        "w", encoding="utf-8"
    ) as file:
        json.dump(metadata, file, ensure_ascii=False, indent=2)

    return index

