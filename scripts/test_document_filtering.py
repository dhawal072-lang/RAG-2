
from src.retrieval.hybrid_search import HybridSearch


def main():
    search = HybridSearch()

    query = "What are the applications and advantages?"

    tests = [
        ("Kotlin only", [1]),
        ("AR/VR only", [2]),
        ("Both documents", [1, 2])
    ]

    for label, document_ids in tests:
        print("\n" + "=" * 60)
        print(label)
        print("=" * 60)

        results = search.search(
            query,
            top_k=5,
            document_ids=document_ids
        )

        for result in results:
            print("Document ID:", result["document_id"])
            print("PDF:", result["filename"])
            print("Page:", result["page_number"])
            print("RRF score:", round(result["rrf_score"], 5))


if __name__ == "__main__":
    main()
