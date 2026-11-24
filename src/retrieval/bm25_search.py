
import json
import re
from pathlib import Path
from rank_bm25 import BM25Okapi


CHUNK_DIRECTORY = Path("data/indexes/chunks")


def tokenize(text: str) -> list[str]:
    return re.findall(r"\b\w+\b", text.lower())


class BM25Search:
    def __init__(self):
        self.chunks = []

        for file_path in sorted(CHUNK_DIRECTORY.glob("*.json")):
            document_id = int(file_path.stem)

            with file_path.open("r", encoding="utf-8") as file:
                chunks = json.load(file)

            for chunk in chunks:
                chunk["document_id"] = document_id

            self.chunks.extend(chunks)

        if not self.chunks:
            raise ValueError("No document chunks found.")

        self.tokenized_chunks = [
            tokenize(chunk["text"])
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(self.tokenized_chunks)

    def search(
        self,
        query: str,
        top_k: int = 5,
        document_ids: list[int] | None = None
    ):
        query_tokens = tokenize(query)
        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        results = []

        for index in ranked_indices:
            result = self.chunks[index]

            if (
                document_ids is not None
                and result["document_id"] not in document_ids
            ):
                continue

            item = result.copy()
            item["score"] = float(scores[index])
            results.append(item)

            if len(results) >= top_k:
                break

        return results
