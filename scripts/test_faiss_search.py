
from src.retrieval.faiss_search import FaissSearch


def main():
    search_engine = FaissSearch()

    queries = [
        "What are the advantages of Kotlin programming?",
        "How are augmented reality and virtual reality used?"
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
            print("Similarity score:", round(result["score"], 4))
            print("Text:", result["text"][:500])


if __name__ == "__main__":
    main()
