
import json
from pathlib import Path

from src.indexing.embedder import Embedder

chunk_directory = Path("data/indexes/chunks")

all_chunks = []

for file_path in sorted(chunk_directory.glob("*.json")):
    with file_path.open("r", encoding="utf-8") as file:
        chunks = json.load(file)
        all_chunks.extend(chunks)

print("Total chunks loaded:", len(all_chunks))

embedder = Embedder()
embedded_chunks = embedder.encode_chunks(all_chunks)

print("Total embedded chunks:", len(embedded_chunks))
print("Vector dimensions:", len(embedded_chunks[0]["embedding"]))

print("\nFirst embedded chunk:")
print("Filename:", embedded_chunks[0]["filename"])
print("Page:", embedded_chunks[0]["page_number"])
print("Embedding values:", embedded_chunks[0]["embedding"][:5])

