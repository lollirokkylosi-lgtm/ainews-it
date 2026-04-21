import feedparser
import requests
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import Optional
import time


@dataclass
class Article:
    title: str
    url: str
    summary: str
    source: str
    published_at: Optional[datetime] = None
    full_text: str = ""
    relevance_score: float = 0.0
    tags: list = field(default_factory=list)


def fetch_full_text(url: str, timeout: int = 10) -> str:
    """Try to fetch article full text for better translation context."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ainews-bot/1.0)"}
        r = requests.get(url, timeout=timeout, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        # Remove script, style, nav, footer
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        # Try article tag first, then main, then body
        for selector in ["article", "main", ".post-content", ".entry-content", "body"]:
            el = soup.select_one(selector)
            if el:
                text = el.get_text(separator="\n", strip=True)
                if len(text) > 200:
                    return text[:3000]  # cap at 3000 chars
        return ""
    except Exception:
        return ""


def parse_date(entry) -> Optional[datetime]:
    for attr in ("published_parsed", "updated_parsed"):
        val = getattr(entry, attr, None)
        if val:
            return datetime(*val[:6], tzinfo=timezone.utc)
    return None


def fetch_source(source: dict, max_age_hours: int = 48) -> list[Article]:
    articles = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    try:
        feed = feedparser.parse(source["url"])
        for entry in feed.entries:
            pub = parse_date(entry)
            if pub and pub < cutoff:
                continue
            summary = ""
            if hasattr(entry, "summary"):
                soup = BeautifulSoup(entry.summary, "lxml")
                summary = soup.get_text(strip=True)[:600]
            art = Article(
                title=entry.get("title", ""),
                url=entry.get("link", ""),
                summary=summary,
                source=source["name"],
                published_at=pub,
            )
            articles.append(art)
    except Exception as e:
        print(f"[fetcher] Error fetching {source['name']}: {e}")
    return articles
