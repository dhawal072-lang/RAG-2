
import sqlite3
from pathlib import Path

DB_PATH = Path("data/indexes/manifest.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_manifest():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                document_id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL UNIQUE,
                sha256 TEXT NOT NULL,
                size_bytes INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                total_pages INTEGER DEFAULT 0,
                total_chunks INTEGER DEFAULT 0,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def register_document(pdf):
    with get_connection() as connection:
        existing = connection.execute(
            "SELECT * FROM documents WHERE file_path = ?",
            (pdf["path"],)
        ).fetchone()

        if existing is None:
            connection.execute("""
                INSERT INTO documents
                (filename, file_path, sha256, size_bytes, status)
                VALUES (?, ?, ?, ?, 'pending')
            """, (
                pdf["filename"], pdf["path"],
                pdf["sha256"], pdf["size_bytes"]
            ))
            return "NEW"

        if existing["sha256"] == pdf["sha256"]:
            return "UNCHANGED"

        connection.execute("""
            UPDATE documents
            SET filename = ?, sha256 = ?, size_bytes = ?,
                status = 'pending', total_pages = 0,
                total_chunks = 0, error_message = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE file_path = ?
        """, (
            pdf["filename"], pdf["sha256"],
            pdf["size_bytes"], pdf["path"]
        ))
        return "MODIFIED"


def update_document_status(file_path, status, pages=0, chunks=0, error=None):
    with get_connection() as connection:
        connection.execute("""
            UPDATE documents
            SET status = ?, total_pages = ?, total_chunks = ?,
                error_message = ?, updated_at = CURRENT_TIMESTAMP
            WHERE file_path = ?
        """, (status, pages, chunks, error, file_path))


def get_pending_documents():
    with get_connection() as connection:
        return connection.execute("""
            SELECT * FROM documents
            WHERE status IN ('pending', 'failed')
            ORDER BY document_id
        """).fetchall()
