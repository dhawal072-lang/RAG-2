
def chunk_pdf(
    document: dict,
    chunk_size: int = 1200,
    overlap: int = 200
) -> list:
    """
    Split an extracted PDF document into smaller text chunks.

    Args:
        document: Dictionary returned by extract_pdf().
        chunk_size: Maximum characters per chunk.
        overlap: Number of overlapping characters between chunks.

    Returns:
        List of chunks containing chunk_id, filename,
        page_number, and text.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size"
        )

    if "pages" not in document:
        raise ValueError("Document must contain a 'pages' field")

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
                    "text": chunk_text
                })

                chunk_id += 1

            start += step

    return chunks
