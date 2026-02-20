# ⚡ NovaPulse

> **The AI intelligence signal for the modern digital creator.**
> Automatically aggregates, categorizes, and distributes AI news to your Telegram channel — every 6 hours, zero cost.

Built for **Auro & Eevio** distribution channels.

---

## 📡 Categories Covered

| # | Category | What it covers |
|---|---|---|
| 💰 | Business & Funding | VC rounds, acquisitions, investments, IPOs |
| 🛠️ | Developer Tools | APIs, SDKs, open-source, LLM frameworks |
| 🔬 | Research & Science | Papers, breakthroughs, benchmarks |
| 📱 | Products & Apps | Consumer AI launches, app updates |
| 🎨 | Creators & Entertainment | AI art, music, video, gaming |
| ⚖️ | Policy & Regulation | Laws, ethics, government AI policy |
| 🎓 | Career & Education | Jobs, courses, upskilling, AI in the workplace |
| 🖥️ | Hardware & Infrastructure | GPUs, chips, data centers, cloud |

---

## 🚀 Setup Guide (One-Time)

### Step 1 — Create a Telegram Bot

1. Open Telegram → search **@BotFather**
2. Send `/newbot` → give it a name (e.g. `NovaPulseBot`)
3. Copy the **Bot Token** (looks like `123456:ABCdefGHI...`)

### Step 2 — Create Your Telegram Channel

1. Create a new Telegram channel (e.g. `@NovaPulseAI`)
2. Add your bot as an **Administrator** of the channel
3. Note the channel username (`@NovaPulseAI`) or numeric ID

### Step 3 — Get a NewsAPI Key (optional but recommended)

1. Sign up free at [newsapi.org](https://newsapi.org)
2. Copy your API key from the dashboard
3. Free tier gives you **100 requests/day** — enough for 4 runs/day

### Step 4 — Fork this repo on GitHub

1. Push this project to a new GitHub repo
2. Go to **Settings → Secrets and variables → Actions → New repository secret**
3. Add these secrets:

| Secret name | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather |
| `TELEGRAM_CHANNEL_ID` | `@YourChannelUsername` |
| `NEWS_API_KEY` | Your NewsAPI key (optional) |

### Step 5 — Enable GitHub Actions

1. Go to the **Actions** tab in your repo
2. Click **Enable Actions** if prompted
3. The bot will now run automatically **4× per day** (every 6 hours)

---

## 🧪 Test Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill in your secrets
cp .env.example .env
# Edit .env with your Telegram token, channel, etc.

# 3. Dry run (prints messages, does NOT send to Telegram)
DRY_RUN=true python news_bot.py

# 4. Real run
python news_bot.py
```

---

## 🏃 Manual Trigger (GitHub)

1. Go to **Actions → NovaPulse — AI Digest Bot**
2. Click **Run workflow**
3. Choose `dry_run: true` to preview, or `false` to actually post

---

## 📁 Project Structure

```
NovaPulse/
├── .github/workflows/run_bot.yml  ← Auto-scheduler (every 6h)
├── categories.py                  ← 8 categories + keywords + RSS feeds
├── classifier.py                  ← Keyword-based article classifier
├── config.py                      ← Environment variable config loader
├── fetcher.py                     ← RSS + NewsAPI article fetcher
├── formatter.py                   ← Telegram HTML message builder
├── news_bot.py                    ← 🚀 Main entry point
├── telegram_bot.py                ← Telegram Bot API sender
├── .env.example                   ← Secret template
└── requirements.txt
```

---

## 💡 Extending NovaPulse

**Add more RSS feeds**: Edit `categories.py` → add URLs to any category's `rss_feeds` list or `GLOBAL_RSS_FEEDS`.

**Add a new category**: Add a new entry to the `CATEGORIES` dict in `categories.py` and include it in `CATEGORY_ORDER`.

**Change frequency**: Edit `.github/workflows/run_bot.yml` → update the `cron` expression.

**WhatsApp**: Use [Callmebot](https://www.callmebot.com/blog/free-api-whatsapp-messages/) for personal WhatsApp pings (free, personal use only).

---

## 📊 Architecture

```
[RSS Feeds]  ──┐
               ├──► fetcher.py ──► classifier.py ──► formatter.py ──► telegram_bot.py ──► 📢 Channel
[NewsAPI]    ──┘
                                        ↕
                              GitHub Actions (runs every 6h)
                              seen_urls.json (deduplication)
```

---

*Made with ⚡ by NovaPulse — for Auro & Eevio*
