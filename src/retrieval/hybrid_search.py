
from src.retrieval.faiss_search import FaissSearch
from src.retrieval.bm25_search import BM25Search


class HybridSearch:
    def __init__(self):
        self.faiss_search = FaissSearch()
        self.bm25_search = BM25Search()

    def search(
        self,
        query: str,
        top_k: int = 5,
        document_ids: list[int] | None = None,
        rrf_k: int = 60
    ):
        faiss_results = self.faiss_search.search(
            query,
            top_k=20,
            document_ids=document_ids
        )

        bm25_results = self.bm25_search.search(
            query,
            top_k=20,
            document_ids=document_ids
        )

        combined = {}

        for results in [faiss_results, bm25_results]:
            for rank, result in enumerate(results, start=1):
                key = (
                    result["document_id"],
                    result["chunk_id"]
                )

                if key not in combined:
                    combined[key] = result.copy()
                    combined[key]["rrf_score"] = 0.0

                combined[key]["rrf_score"] += (
                    1.0 / (rrf_k + rank)
                )

        ranked_results = sorted(
            combined.values(),
            key=lambda item: item["rrf_score"],
            reverse=True
        )

        return ranked_results[:top_k]

