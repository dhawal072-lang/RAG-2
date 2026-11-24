
from src.retrieval.bm25_search import BM25Search


def main():
    search_engine = BM25Search()

    queries = [
        "Kotlin advantages and safety",
        "augmented reality virtual reality applications"
    ]

    for query in queries:
        print("\n" + "=" * 70)
        print("QUESTION:", query)
        print("=" * 70)

        results = search_engine.search(query, top_k=3)

        for number, result in enumerate(results, start=1):
            print(f"\nResult {number}")
            print("PDF:", result["filename"])
            print("Page:", result["page_number"])
            print("BM25 score:", round(result["score"], 4))
            print("Text:", result["text"][:500])


if __name__ == "__main__":
    main()
