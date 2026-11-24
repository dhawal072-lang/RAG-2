
from sentence_transformers import SentenceTransformer

MODEL_PATH = "models/bge-base-en-v1.5"


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(
            MODEL_PATH,
            local_files_only=True
        )

    def encode(self, texts: list[str]):
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )

    def encode_chunks(self, chunks: list[dict]):
        texts = [chunk["text"] for chunk in chunks]

        vectors = self.encode(texts)

        return [
            {
                **chunk,
                "embedding": vector.tolist()
            }
            for chunk, vector in zip(chunks, vectors)
        ]


if __name__ == "__main__":
    embedder = Embedder()

    test_texts = [
        "Kotlin is a modern programming language.",
        "Augmented reality combines digital content with the real world."
    ]

    vectors = embedder.encode(test_texts)

    print("Number of vectors:", len(vectors))
    print("Vector dimensions:", vectors.shape[1])

