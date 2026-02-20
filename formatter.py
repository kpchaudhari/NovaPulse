"""
NovaPulse — Message Formatter
Produces Telegram HTML-formatted messages for each category digest.
Designed for a premium, WhatsApp-friendly visual experience.
"""

from datetime import datetime, timezone
from categories import CATEGORIES, CATEGORY_ORDER
from config import MAX_ARTICLES_PER_CATEGORY


# ─── Header / Footer ──────────────────────────────────────────────────────────

HEADER_TEMPLATE = """🧠 <b>BuzzWordAI</b> — Your Daily AI Pulse
📅 <i>{date} • {time} IST</i>
━━━━━━━━━━━━━━━━━━━━━━

Here's what's happening in the world of AI 👇"""

FOOTER = """━━━━━━━━━━━━━━━━━━━━━━
💡 <i>Curated by AI, powered by</i> <b>BuzzWordAI</b>
📢 Share with your tech crew! ⚡"""


def _now_ist() -> tuple[str, str]:
    """Return current date and time in IST as strings."""
    from datetime import timedelta
    ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    return ist.strftime("%d %b %Y"), ist.strftime("%I:%M %p")


def format_header() -> str:
    date, time = _now_ist()
    return HEADER_TEMPLATE.format(date=date, time=time)


# ─── Category Block ───────────────────────────────────────────────────────────

def format_category_block(cat_key: str, articles: list[dict]) -> str:
    """Format a single category into a visually rich Telegram HTML block."""
    cat = CATEGORIES[cat_key]
    emoji = cat["emoji"]
    title = cat["title"]

    lines = [
        f"{emoji} <b>{title}</b>",
        "",
    ]

    for idx, article in enumerate(articles[:MAX_ARTICLES_PER_CATEGORY]):
        url = article["url"]
        ai_summary = article.get("ai_summary", "")

        if ai_summary:
            # AI summary: clean text + separate link
            summary_escaped = ai_summary.replace("<", "&lt;").replace(">", "&gt;")
            lines.append(f"▸ {summary_escaped}")
            lines.append(f'   🔗 <a href="{url}">Read more</a>')
        else:
            # Fallback: plain title + separate link (same visual style)
            t = article["title"].replace("<", "&lt;").replace(">", "&gt;")
            lines.append(f"▸ {t}")
            lines.append(f'   🔗 <a href="{url}">Read more</a>')

        # Add spacing between articles
        lines.append("")

    return "\n".join(lines)


# ─── Full Digest ──────────────────────────────────────────────────────────────

def format_full_digest(categorised: dict[str, list[dict]]) -> list[str]:
    """
    Build a list of Telegram messages.
    Telegram has a 4096-char limit per message, so we split by category.
    Returns [header_msg, cat1_msg, cat2_msg, ..., footer_msg]
    """
    messages = [format_header()]

    for cat_key in CATEGORY_ORDER:
        articles = categorised.get(cat_key, [])
        if not articles:
            continue
        block = format_category_block(cat_key, articles)
        # Telegram limit safety: chunk if > 4000 chars
        if len(block) > 4000:
            block = block[:3997] + "…"
        messages.append(block)

    messages.append(FOOTER)
    return messages


def format_summary_line(categorised: dict[str, list[dict]]) -> str:
    """One-liner summary of how many articles per category (for logs)."""
    parts = []
    for k in CATEGORY_ORDER:
        n = len(categorised.get(k, []))
        if n:
            cat = CATEGORIES[k]
            parts.append(f"{cat['emoji']} {n}")
    return "  ".join(parts) if parts else "No articles found"


# ─── Top Stories (single message) ────────────────────────────────────────────

def format_top_stories(articles: list[dict]) -> list[str]:
    """
    Format a flat list of ranked articles into a SINGLE Telegram message.
    Used for "All Categories" mode — one consolidated Top 10 message.
    """
    date, time = _now_ist()

    lines = [
        f"🧠 <b>BuzzWordAI — Top AI Stories</b>",
        f"📅 <i>{date} • {time} IST</i>",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]

    for idx, article in enumerate(articles[:10], 1):
        url = article["url"]
        ai_summary = article.get("ai_summary", "")

        if ai_summary:
            summary_escaped = ai_summary.replace("<", "&lt;").replace(">", "&gt;")
            lines.append(f"<b>{idx}.</b> {summary_escaped}")
            lines.append(f'   🔗 <a href="{url}">Read more</a>')
        else:
            t = article["title"].replace("<", "&lt;").replace(">", "&gt;")
            lines.append(f"<b>{idx}.</b> {t}")
            lines.append(f'   🔗 <a href="{url}">Read more</a>')

        lines.append("")

    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    lines.append('💡 <i>Curated by AI, powered by</i> <b>BuzzWordAI</b>')
    lines.append("📢 Share with your tech crew! ⚡")

    msg = "\n".join(lines)

    # If single message exceeds Telegram limit, split into 2
    if len(msg) > 4000:
        return [msg[:3997] + "…"]
    return [msg]
