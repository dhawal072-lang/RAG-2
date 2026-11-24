
from src.retrieval.hybrid_search import HybridSearch
from src.services.citation_service import CitationService


def main():
    search_engine = HybridSearch()

    query = "What are the advantages of Kotlin?"

    retrieved_chunks = search_engine.search(
        query,
        top_k=5
    )

    citations = CitationService.build_citations(
        retrieved_chunks
    )

    print("\nQUESTION:", query)
    print("\nSOURCES:")

    for citation in citations:
        print("\nCitation:", citation["citation_id"])
        print("PDF:", citation["filename"])
        print("Page:", citation["page_number"])
        print("Text:", citation["text"][:300])


if __name__ == "__main__":
    main()
