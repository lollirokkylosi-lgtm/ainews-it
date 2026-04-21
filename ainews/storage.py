import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = os.environ.get("DB_PATH", "./ainews_seen.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS seen_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_hash TEXT UNIQUE NOT NULL,
            url TEXT NOT NULL,
            title TEXT,
            source TEXT,
            fetched_at TEXT,
            wp_post_id INTEGER
        )
    """)
    conn.commit()
    conn.close()


def is_seen(url: str) -> bool:
    h = hashlib.sha256(url.encode()).hexdigest()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT 1 FROM seen_articles WHERE url_hash=?", (h,))
    result = cur.fetchone() is not None
    conn.close()
    return result


def mark_seen(url: str, title: str, source: str, wp_post_id: int = None):
    h = hashlib.sha256(url.encode()).hexdigest()
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "INSERT OR IGNORE INTO seen_articles (url_hash, url, title, source, fetched_at, wp_post_id) VALUES (?,?,?,?,?,?)",
            (h, url, title, source, datetime.utcnow().isoformat(), wp_post_id)
        )
        conn.commit()
    finally:
        conn.close()


def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT COUNT(*), MAX(fetched_at) FROM seen_articles")
    row = cur.fetchone()
    conn.close()
    return {"total": row[0], "last_fetch": row[1]}
