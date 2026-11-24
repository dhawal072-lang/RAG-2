
import json
import faiss
from pathlib import Path

from src.indexing.embedder import Embedder


INDEX_PATH = Path("data/indexes/faiss/documents.faiss")
METADATA_PATH = Path("data/indexes/faiss/metadata.json")


class FaissSearch:
    def __init__(self):
        self.embedder = Embedder()
        self.index = faiss.read_index(str(INDEX_PATH))

        with METADATA_PATH.open("r", encoding="utf-8") as file:
            self.metadata = json.load(file)

    def search(
        self,
        query: str,
        top_k: int = 5,
        document_ids: list[int] | None = None
    ):
        query_vector = self.embedder.encode([query])
        query_vector = query_vector.astype("float32")

        # Search the full index, then filter by document.
        search_count = self.index.ntotal

        scores, indices = self.index.search(
            query_vector,
            search_count
        )

        results = []

        for score, index_position in zip(scores[0], indices[0]):
            if index_position == -1:
                continue

            result = self.metadata[index_position]

            if (
                document_ids is not None
                and result["document_id"] not in document_ids
            ):
                continue

            item = result.copy()
            item["score"] = float(score)
            results.append(item)

            if len(results) >= top_k:
                break

        return results
