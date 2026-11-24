
class CitationService:

    @staticmethod
    def build_citations(retrieved_chunks: list[dict]):
        citations = []

        for number, chunk in enumerate(retrieved_chunks, start=1):

            citations.append({
                "citation_id": number,
                "reference": f"[Source {number}]",
                "document_id": chunk["document_id"],
                "filename": chunk["filename"],
                "page_number": chunk["page_number"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "score": chunk.get("rrf_score")
            })

        return citations
