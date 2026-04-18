import sqlite3
import os

# Honour DB_URL env var; strip SQLAlchemy-style sqlite:/// prefix if present
_raw = os.getenv("DB_URL", "data.db")
DB_PATH = _raw.replace("sqlite:///", "") if _raw.startswith("sqlite:///") else _raw

# Resolve relative paths from project root (one level above this file)
if not os.path.isabs(DB_PATH):
    DB_PATH = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", DB_PATH)
    )


def get_db() -> sqlite3.Connection:
    """
    Return a per-request SQLite connection.
    WAL journal mode and foreign key enforcement are set on every connection.
    Rows are returned as dict-like sqlite3.Row objects.

    Usage:
        conn = get_db()
        try:
            rows = conn.execute(...).fetchall()
        finally:
            conn.close()
    """
    conn = sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn
