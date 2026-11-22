from pathlib import Path
import hashlib


def calculate_file_hash(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def scan_pdf_directory(directory: str):
    root = Path(directory)

    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    pdf_files = sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() == ".pdf"
    )

    results = []

    for pdf_path in pdf_files:
        results.append({
            "filename": pdf_path.name,
            "path": str(pdf_path.resolve()),
            "size_bytes": pdf_path.stat().st_size,
            "sha256": calculate_file_hash(pdf_path),
        })

    return results