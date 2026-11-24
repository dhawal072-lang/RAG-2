
import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager

from dotenv import load_dotenv

load_dotenv()

DEFAULT_DB_PATH = Path("data/indexes/manifest.db")


def get_database_path() -> Path:
    """Resolve the SQLite database path from environment configuration."""
    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite:///./data/indexes/manifest.db"
    )

    prefix = "sqlite:///"

    if not database_url.startswith(prefix):
        raise ValueError("Only SQLite database URLs are supported.")

    configured_path = database_url[len(prefix):]

    if configured_path.startswith("./"):
        configured_path = configured_path[2:]

    path = Path(configured_path)

    if not path.is_absolute():
        path = Path.cwd() / path

    return path.resolve()


DB_PATH = get_database_path()


def initialize_manifest():
    with get_connection() as connection:
        connection.execute("PRAGMA journal_mode = WAL")

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
                pdf["filename"],
                pdf["path"],
                pdf["sha256"],
                pdf["size_bytes"]
            ))
            return "NEW"

        if existing["sha256"] == pdf["sha256"]:
            return "UNCHANGED"

        connection.execute("""
            UPDATE documents
            SET filename = ?,
                sha256 = ?,
                size_bytes = ?,
                status = 'pending',
                total_pages = 0,
                total_chunks = 0,
                error_message = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE file_path = ?
        """, (
            pdf["filename"],
            pdf["sha256"],
            pdf["size_bytes"],
            pdf["path"]
        ))
        return "MODIFIED"


def update_document_status(
    file_path,
    status,
    pages=0,
    chunks=0,
    error=None
):
    with get_connection() as connection:
        connection.execute("""
            UPDATE documents
            SET status = ?,
                total_pages = ?,
                total_chunks = ?,
                error_message = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE file_path = ?
        """, (status, pages, chunks, error, file_path))


def get_pending_documents():
    with get_connection() as connection:
        return connection.execute("""
            SELECT *
            FROM documents
            WHERE status IN ('pending', 'failed')
            ORDER BY document_id
        """).fetchall()

def get_all_documents():
    """Return all indexed document records."""
    with get_connection() as connection:
        return connection.execute("""
            SELECT
                document_id,
                filename,
                status,
                total_pages,
                total_chunks,
                error_message,
                created_at,
                updated_at
            FROM documents
            ORDER BY document_id
        """).fetchall()
    
@contextmanager
def get_connection():
    """Open a SQLite connection with safe transaction handling."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        DB_PATH,
        timeout=30
    )

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 30000")

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()