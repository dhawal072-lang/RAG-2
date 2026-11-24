
from src.retrieval.hybrid_search import HybridSearch
from src.services.llm_service import LLMService


class CombinedSummaryService:

    def __init__(self):
        self.search_engine = HybridSearch()
        self.llm_service = LLMService()

    def generate_combined_summary(
        self,
        document_ids: list[int],
        top_k: int = 20
    ):

        if not document_ids:
            raise ValueError("Select at least one document.")

        if len(document_ids) != len(set(document_ids)):
            raise ValueError("Duplicate document IDs are not allowed.")

        if any(document_id < 1 for document_id in document_ids):
            raise ValueError("Document IDs must be positive.")

        query = (
            "Provide the main topics, key findings, "
            "important concepts, applications, advantages, "
            "limitations, and conclusions discussed "
            "in these documents."
        )

        retrieved_chunks = self.search_engine.search(
            query,
            top_k=top_k,
            document_ids=document_ids
        )

        if not retrieved_chunks:
            raise ValueError("No relevant passages found.")

        context = "\n\n".join(
            [
                f"""
PDF: {chunk['filename']}
Page: {chunk['page_number']}
Content:
{chunk['text']}
"""
                for chunk in retrieved_chunks
            ]
        )

        prompt = f"""
You are a document analysis assistant.

Create one comprehensive combined summary
covering the selected PDF documents.

Requirements:
1. Identify the main topic of each document.
2. Explain the important findings.
3. Identify common themes.
4. Compare differences between documents.
5. Include important applications and advantages.
6. Mention limitations and challenges.
7. Provide an overall conclusion.

Use only the supplied document passages.
Do not invent information.

Selected document IDs:
{document_ids}

Document passages:
{context}
"""

        summary = self.llm_service.generate(prompt)

        sources = [
            {
                "filename": chunk["filename"],
                "page_number": chunk["page_number"],
                "document_id": chunk["document_id"],
                "chunk_id": chunk["chunk_id"]
            }
            for chunk in retrieved_chunks
        ]

        return {
            "document_ids": document_ids,
            "summary": summary,
            "sources": sources
        }
