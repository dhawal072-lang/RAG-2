def chunk_pdf(document: dict, chunk_size: int = 1200, overlap: int = 200) -> list:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    chunks = []
    chunk_id = 0
    step = chunk_size - overlap

    for page in document["pages"]:
        text = page["text"]

        if not text:
            continue

        start = 0

        while start < len(text):
            chunk_text = text[start:start + chunk_size].strip()

            if chunk_text:
                chunks.append({
                    "chunk_id": chunk_id,
                    "filename": document["filename"],
                    "page_number": page["page_number"],
                    "text": chunk_text,
                })
                chunk_id += 1

            start += step

    return chunks