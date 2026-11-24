
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.retrieval.hybrid_search import HybridSearch
from src.services.citation_service import CitationService
from src.services.llm_service import LLMService


router = APIRouter()

search_engine = HybridSearch()
llm_service = LLMService()


class ChatRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=5, ge=1, le=20)
    document_ids: list[int] | None = None


def build_rag_prompt(question: str, citations: list[dict]) -> str:
    context = "\n\n".join(
        [
            f"""
[SOURCE {citation['citation_id']}]
PDF: {citation['filename']}
PAGE: {citation['page_number']}

CONTENT:
{citation['text']}
"""
            for citation in citations
        ]
    )

    return f"""
You are an expert document intelligence assistant.

Answer the user's question using ONLY the supplied document passages.

STRICT RULES:

1. Do not invent facts or use outside knowledge.
2. Every factual claim must be supported by the supplied passages.
3. Cite supporting sources using [Source 1], [Source 2], etc.
4. Use the exact source numbers provided in the passages.
5. If the documents do not contain enough information, clearly say so.
6. If multiple documents discuss the same subject, compare them carefully.
7. Distinguish facts from interpretations.
8. Never fabricate PDF names or page numbers.

RESPONSE FORMAT:

## Answer
Provide a clear, direct answer.

## Key Points
List the important findings relevant to the question.

## Conclusion
Summarize the answer briefly.

## Sources
List the source numbers used, with their PDF filenames and page numbers.

USER QUESTION:
{question}

SUPPLIED DOCUMENT PASSAGES:
{context}

Now answer the user's question following all the rules above.
"""


@router.post("/ask")
def ask_question(request: ChatRequest):
    try:
        if request.document_ids is not None:
            if not request.document_ids:
                raise HTTPException(
                    status_code=400,
                    detail="Select at least one document."
                )

            if len(request.document_ids) != len(set(request.document_ids)):
                raise HTTPException(
                    status_code=400,
                    detail="Duplicate document IDs are not allowed."
                )

            if any(document_id < 1 for document_id in request.document_ids):
                raise HTTPException(
                    status_code=400,
                    detail="Document IDs must be positive."
                )

        retrieved_chunks = search_engine.search(
            request.question,
            top_k=request.top_k,
            document_ids=request.document_ids
        )

        if not retrieved_chunks:
            raise HTTPException(
                status_code=404,
                detail="No relevant passages found in the selected documents."
            )

        citations = CitationService.build_citations(retrieved_chunks)

        prompt = build_rag_prompt(
            request.question,
            citations
        )

        answer = llm_service.generate(prompt)

        return {
            "question": request.question,
            "selected_document_ids": request.document_ids,
            "answer": answer,
            "sources": citations
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your question."
        )
