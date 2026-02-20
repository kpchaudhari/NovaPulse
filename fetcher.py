"""
NovaPulse — News Fetcher
Pulls articles from RSS feeds and (optionally) NewsAPI.
Returns a flat list of normalised article dicts.
"""

import feedparser
import requests
import logging
from datetime import datetime, timezone, timedelta
from config import NEWS_API_KEY
from categories import GLOBAL_RSS_FEEDS, CATEGORIES

logger = logging.getLogger(__name__)

# ─── Helpers ─────────────────────────────────────────────────────────────────

def _parse_date(entry) -> datetime:
    """Best-effort publish-date extraction from a feedparser entry."""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        return datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc)


def _is_recent(pub_date: datetime, hours: int = 12) -> bool:
    """Only keep articles published within the last N hours."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    return pub_date >= cutoff


def _normalise(entry, source_url: str) -> dict:
    """Turn a feedparser entry into a standard article dict."""
    return {
        "title": getattr(entry, "title", "No title").strip(),
        "url": getattr(entry, "link", ""),
        "summary": getattr(entry, "summary", "")[:300].strip(),
        "published": _parse_date(entry),
        "source": source_url,
    }


# ─── RSS Fetcher ─────────────────────────────────────────────────────────────

def fetch_rss(feed_url: str, hours: int = 12) -> list[dict]:
    """Fetch and parse a single RSS feed, returning recent articles."""
    articles = []
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            article = _normalise(entry, feed_url)
            if article["url"] and _is_recent(article["published"], hours):
                articles.append(article)
    except Exception as e:
        logger.warning(f"RSS fetch failed for {feed_url}: {e}")
    return articles


def fetch_all_rss(hours: int = 12) -> list[dict]:
    """Fetch from global feeds + every category-specific feed."""
    all_feeds = set(GLOBAL_RSS_FEEDS)
    for cat in CATEGORIES.values():
        all_feeds.update(cat.get("rss_feeds", []))

    articles = []
    for feed_url in all_feeds:
        fetched = fetch_rss(feed_url, hours)
        logger.info(f"  RSS [{len(fetched):>2}] {feed_url}")
        articles.extend(fetched)

    # Deduplicate by URL
    seen = set()
    unique = []
    for a in articles:
        if a["url"] not in seen:
            seen.add(a["url"])
            unique.append(a)

    logger.info(f"RSS total: {len(unique)} unique articles in last {hours}h")
    return unique


# ─── NewsAPI Fetcher (optional) ──────────────────────────────────────────────

def fetch_newsapi(hours: int = 12) -> list[dict]:
    """
    Fetch from NewsAPI free tier (100 req/day).
    Returns [] gracefully if key is missing or quota exceeded.
    """
    if not NEWS_API_KEY:
        logger.info("NewsAPI key not set — skipping NewsAPI fetch.")
        return []

    from_dt = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
    params = {
        "q": "artificial intelligence OR AI OR machine learning OR LLM OR generative AI",
        "language": "en",
        "sortBy": "publishedAt",
        "from": from_dt,
        "pageSize": 100,
        "apiKey": NEWS_API_KEY,
    }
    try:
        resp = requests.get("https://newsapi.org/v2/everything", params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        articles = []
        for item in data.get("articles", []):
            if item.get("url") and item.get("title"):
                articles.append({
                    "title": item["title"].strip(),
                    "url": item["url"],
                    "summary": (item.get("description") or "")[:300].strip(),
                    "published": datetime.fromisoformat(
                        item["publishedAt"].replace("Z", "+00:00")
                    ),
                    "source": item.get("source", {}).get("name", "NewsAPI"),
                })
        logger.info(f"NewsAPI: {len(articles)} articles")
        return articles
    except Exception as e:
        logger.warning(f"NewsAPI fetch failed: {e}")
        return []


# ─── Main Entry ──────────────────────────────────────────────────────────────

def fetch_all_articles(hours: int = 12) -> list[dict]:
    """Aggregate articles from all sources."""
    articles = fetch_all_rss(hours) + fetch_newsapi(hours)
    # Final dedup by URL
    seen = set()
    unique = []
    for a in articles:
        if a["url"] not in seen and a["url"]:
            seen.add(a["url"])
            unique.append(a)
    return sorted(unique, key=lambda x: x["published"], reverse=True)
