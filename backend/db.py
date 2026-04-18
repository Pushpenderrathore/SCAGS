import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row  # returns dict-like rows
    conn.execute("PRAGMA journal_mode=WAL")
    return conn
