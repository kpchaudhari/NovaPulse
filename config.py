"""
NovaPulse Configuration
Load settings from environment variables (set via .env or GitHub Secrets).
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ─── Telegram ────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")  # e.g. @YourChannel or -100xxxxxxx

# ─── NewsAPI ─────────────────────────────────────────────────────────────────
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")  # https://newsapi.org (free: 100 req/day)

# ─── Bot Behaviour ───────────────────────────────────────────────────────────
MAX_ARTICLES_PER_CATEGORY = int(os.getenv("MAX_ARTICLES_PER_CATEGORY", "5"))
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"   # Print instead of send
SEND_DELAY_SECONDS = float(os.getenv("SEND_DELAY_SECONDS", "2"))  # Delay between messages

# ─── Deduplication ───────────────────────────────────────────────────────────
SEEN_URLS_FILE = "seen_urls.json"
MAX_SEEN_URLS = 500  # Keep last N URLs in memory to avoid re-posting
