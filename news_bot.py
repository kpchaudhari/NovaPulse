"""
NovaPulse — Main Orchestrator
Run this script to fetch, classify, format, and post the AI digest.

Usage:
    python news_bot.py               # Normal run → posts to Telegram
    DRY_RUN=true python news_bot.py  # Print messages, do not send
"""

import json
import logging
import os
import sys
from pathlib import Path

from config import SEEN_URLS_FILE, MAX_SEEN_URLS
from fetcher import fetch_all_articles
from classifier import classify_all
from summarizer import summarize_all, summarize_top_stories
from formatter import format_full_digest, format_top_stories, format_summary_line
from telegram_bot import send_messages, send_message

# ─── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ─── Deduplication ───────────────────────────────────────────────────────────

def load_seen_urls() -> set[str]:
    p = Path(SEEN_URLS_FILE)
    if p.exists():
        with open(p) as f:
            return set(json.load(f))
    return set()


def save_seen_urls(seen: set[str]) -> None:
    # Keep only the last MAX_SEEN_URLS to avoid the file growing forever
    trimmed = list(seen)[-MAX_SEEN_URLS:]
    with open(SEEN_URLS_FILE, "w") as f:
        json.dump(trimmed, f)


def filter_seen(articles: list[dict], seen: set[str]) -> list[dict]:
    return [a for a in articles if a["url"] not in seen]


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    logger.info("⚡ NovaPulse is starting...")

    # 1. Load dedup state
    seen_urls = load_seen_urls()
    logger.info(f"Seen URLs loaded: {len(seen_urls)}")

    # 2. Fetch
    logger.info("Fetching articles from all sources...")
    all_articles = fetch_all_articles(hours=12)
    logger.info(f"Total fetched: {len(all_articles)}")

    # 3. Filter already-seen articles
    target_category = os.getenv("CATEGORY", "all").lower()
    is_manual = os.getenv("EVENT_NAME") == "workflow_dispatch"
    
    # If it's a manual on-demand request from Telegram, always give them the news (bypass cache)
    if is_manual:
        fresh = all_articles
        logger.info(f"Manual trigger detected, bypassing deduplication: {len(fresh)} articles")
    else:
        fresh = filter_seen(all_articles, seen_urls)
        logger.info(f"Automated run: Fresh articles (not seen before): {len(fresh)}")

    if not fresh:
        logger.info("Nothing new to post. Exiting.")
        sys.exit(0)

    # 4. Branch: "All Categories" (Top 10) vs specific category
    if target_category == "all":
        # ── Top 10 Mode: single consolidated message ──
        logger.info("All Categories mode: generating Top 10 AI Stories...")
        top_stories = summarize_top_stories(fresh)

        if not top_stories:
            logger.info("No AI-relevant stories found.")
            if is_manual:
                send_message("🔍 <b>BuzzWordAI</b>\n\nNo AI-relevant news found right now.\nTry again later! 🧠")
            sys.exit(0)

        messages = format_top_stories(top_stories)

    else:
        # ── Specific Category Mode: category-based digest ──
        categorised = classify_all(fresh)

        if target_category in categorised:
            logger.info(f"Filtering digest for category: {target_category}")
            categorised = {target_category: categorised[target_category]}
        else:
            logger.warning(f"Requested category '{target_category}' not found or invalid.")
            categorised = {}

        logger.info(f"Digest: {format_summary_line(categorised)}")

        if not any(categorised.values()):
            logger.info("No matching articles found for the given criteria.")
            if is_manual:
                send_message(f"🔍 <b>BuzzWordAI</b>\n\nNo fresh AI news found for <b>{target_category}</b> right now.\nTry another category! 🧠")
            sys.exit(0)

        logger.info("Generating AI summaries via Gemini...")
        categorised = summarize_all(categorised)

        if not any(categorised.values()):
            logger.info("All articles filtered as non-AI by Gemini.")
            if is_manual:
                send_message("🔍 <b>BuzzWordAI</b>\n\nNo AI-relevant news found right now.\nTry another category! 🧠")
            sys.exit(0)

        messages = format_full_digest(categorised)

    # 5. Send
    sent = send_messages(messages)
    logger.info(f"Messages sent: {sent}/{len(messages)}")

    # 6. Save seen URLs
    if not is_manual:
        new_urls = {a["url"] for a in fresh}
        seen_urls.update(new_urls)
        save_seen_urls(seen_urls)
        logger.info(f"Saved {len(new_urls)} new URLs to seen list.")
    else:
        logger.info("Bypassed saving seen URLs for manual request.")

    logger.info("✅ NovaPulse run complete.")


if __name__ == "__main__":
    main()
