"""
NovaPulse — Classifier
Assigns each article to one or more categories using keyword matching.
"""

import re
from categories import CATEGORIES

# Pre-compile keyword patterns for performance
_PATTERNS: dict[str, re.Pattern] = {}
for _key, _cat in CATEGORIES.items():
    kws = [re.escape(k) for k in _cat["keywords"]]
    _PATTERNS[_key] = re.compile(r"\b(" + "|".join(kws) + r")\b", re.IGNORECASE)


def classify(article: dict) -> list[str]:
    """
    Return a list of category keys that match the article.
    Searches title + summary text.
    Falls back to 'products' if nothing matched (catch-all).
    """
    text = f"{article.get('title', '')} {article.get('summary', '')}"
    matched = [key for key, pat in _PATTERNS.items() if pat.search(text)]
    return matched if matched else ["products"]


def classify_all(articles: list[dict]) -> dict[str, list[dict]]:
    """
    Group a list of articles by category.
    Returns {category_key: [article, ...]}
    An article CAN appear in multiple categories.
    """
    buckets: dict[str, list[dict]] = {key: [] for key in CATEGORIES}
    for article in articles:
        for cat in classify(article):
            buckets[cat].append(article)
    return buckets
