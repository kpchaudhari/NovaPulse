"""
NovaPulse — AI Summarizer
Uses Google Gemini 2.0 Flash (free tier) to generate professional
bullet-point summaries for each article category.
"""

import json
import logging
import requests
from config import GEMINI_API_KEY, MAX_ARTICLES_PER_CATEGORY
from categories import CATEGORIES

logger = logging.getLogger(__name__)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# ─── Prompt Template ─────────────────────────────────────────────────────────

SUMMARY_PROMPT = """You are an expert AI news analyst writing a WhatsApp-friendly news digest.

I will give you a list of article titles and their RSS descriptions from the "{category}" category.

For each article, write a concise, punchy 1-2 line bullet-point summary that:
- Captures the KEY facts (who, what, numbers, impact)
- Is written in professional news style (no fluff, no opinions)
- Can be understood without clicking the link
- Uses plain text (no markdown, no HTML, no bold/italic)

Respond ONLY with a valid JSON array of objects, one per article, in this exact format:
[
  {{"index": 0, "summary": "Your 1-2 line summary here"}},
  {{"index": 1, "summary": "Your 1-2 line summary here"}}
]

Do NOT include anything outside the JSON array. No explanation, no preamble.

Here are the articles:

{articles}"""


def _build_article_text(articles: list[dict]) -> str:
    """Format articles for the prompt."""
    lines = []
    for i, a in enumerate(articles[:MAX_ARTICLES_PER_CATEGORY]):
        title = a.get("title", "No title")
        summary = a.get("summary", "")
        source = a.get("source", "")
        lines.append(f"[{i}] Title: {title}\n    Description: {summary}\n    Source: {source}")
    return "\n\n".join(lines)


def summarize_category(cat_key: str, articles: list[dict]) -> list[dict]:
    """
    Summarize a list of articles for a given category using Gemini.
    Returns the articles list with a new 'ai_summary' field added to each.
    Falls back gracefully if Gemini fails.
    """
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set — skipping AI summaries.")
        return articles

    capped = articles[:MAX_ARTICLES_PER_CATEGORY]
    if not capped:
        return articles

    cat_title = CATEGORIES.get(cat_key, {}).get("title", cat_key)
    article_text = _build_article_text(capped)
    prompt = SUMMARY_PROMPT.format(category=cat_title, articles=article_text)

    import time
    max_retries = 3

    for attempt in range(max_retries):
        try:
            resp = requests.post(
                GEMINI_URL,
                headers={
                    "Content-Type": "application/json",
                    "X-goog-api-key": GEMINI_API_KEY,
                },
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": 1024,
                    },
                },
                timeout=30,
            )

            if resp.status_code == 429:
                wait_time = 10 * (2 ** attempt)  # 10s, 20s, 40s
                logger.warning(f"  Gemini rate limited for [{cat_key}], retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue

            resp.raise_for_status()
            data = resp.json()

            # Extract the text response
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            
            # Clean up: strip markdown code fences if present
            cleaned = raw_text.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]  # remove first line
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()

            summaries = json.loads(cleaned)

            # Attach summaries to articles
            summary_map = {s["index"]: s["summary"] for s in summaries}
            for i, article in enumerate(capped):
                article["ai_summary"] = summary_map.get(i, "")

            logger.info(f"  Gemini summarized {len(summaries)} articles for [{cat_key}]")
            return capped

        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"  Gemini attempt {attempt + 1} failed for [{cat_key}]: {e}")
                time.sleep(5)
            else:
                logger.warning(f"  Gemini summarization failed for [{cat_key}] after {max_retries} attempts: {e}")

    # Graceful fallback: return articles without summaries
    return capped


def summarize_all(categorised: dict[str, list[dict]]) -> dict[str, list[dict]]:
    """
    Summarize all categories. Returns the same dict but with
    'ai_summary' field added to each article where possible.
    """
    result = {}
    for cat_key, articles in categorised.items():
        if articles:
            result[cat_key] = summarize_category(cat_key, articles)
        else:
            result[cat_key] = articles
    return result
