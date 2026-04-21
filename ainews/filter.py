from ainews.fetcher import Article
from ainews.storage import is_seen
import re


def score_article(article: Article, config: dict) -> float:
    text = (article.title + " " + article.summary).lower()
    score = 0.5  # base

    boost_keywords = [k.lower() for k in config.get("keywords_boost", [])]
    exclude_keywords = [k.lower() for k in config.get("keywords_exclude", [])]

    for kw in exclude_keywords:
        if kw in text:
            return 0.0

    for kw in boost_keywords:
        if kw.lower() in text:
            score += 0.1

    # Penalize very short summaries
    if len(article.summary) < 50:
        score -= 0.2

    # Filter out non-news HN-style posts
    if re.match(r'^(Ask HN|Tell HN|Who is|Hiring)', article.title):
        return 0.0

    return min(score, 1.0)


def filter_articles(articles: list[Article], config: dict) -> list[Article]:
    min_score = config.get("min_relevance_score", 0.6)
    results = []
    seen_titles = set()

    for art in articles:
        # Skip already processed
        if is_seen(art.url):
            continue
        # Skip duplicates within this batch (by title similarity)
        title_key = re.sub(r'[^a-z0-9]', '', art.title.lower())[:40]
        if title_key in seen_titles:
            continue
        seen_titles.add(title_key)

        art.relevance_score = score_article(art, config)
        if art.relevance_score >= min_score:
            results.append(art)

    # Sort by relevance descending
    results.sort(key=lambda a: a.relevance_score, reverse=True)
    return results
