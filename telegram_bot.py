"""
NovaPulse — Telegram Sender
Sends messages to a Telegram channel via Bot API.
"""

import time
import logging
import requests
from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHANNEL_ID,
    DRY_RUN,
    SEND_DELAY_SECONDS,
)

logger = logging.getLogger(__name__)

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_message(text: str) -> bool:
    """Send a single HTML message to the configured channel."""
    if DRY_RUN:
        print("=" * 60)
        print(text)
        print("=" * 60)
        return True

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
        logger.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL_ID not set!")
        return False

    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        resp = requests.post(f"{TELEGRAM_API}/sendMessage", json=payload, timeout=15)
        data = resp.json()
        if not data.get("ok"):
            logger.error(f"Telegram API error: {data.get('description')}")
            return False
        return True
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False


def send_messages(messages: list[str]) -> int:
    """Send a list of messages with a delay. Returns count of successes."""
    sent = 0
    for i, msg in enumerate(messages):
        if not msg.strip():
            continue
        success = send_message(msg)
        if success:
            sent += 1
        if i < len(messages) - 1:
            time.sleep(SEND_DELAY_SECONDS)
    return sent
