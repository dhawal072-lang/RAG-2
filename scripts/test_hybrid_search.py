
from src.retrieval.hybrid_search import HybridSearch


def main():
    search_engine = HybridSearch()

    queries = [
        "What are the safety advantages of Kotlin?",
        "What are the applications and challenges of augmented reality?",
        "How does virtual reality create immersive experiences?"
    ]

    for query in queries:
        print("\n" + "=" * 80)
        print("QUESTION:", query)
        print("=" * 80)

        results = search_engine.search(query, top_k=5)

        for number, result in enumerate(results, start=1):
            print(f"\nResult {number}")
            print("PDF:", result["filename"])
            print("Page:", result["page_number"])
            print("RRF score:", round(result["rrf_score"], 6))
            print("Text:", result["text"][:500])


if __name__ == "__main__":
    main()
