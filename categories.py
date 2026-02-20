"""
NovaPulse — Category Definitions
Each category has:
  - emoji, title, description
  - keywords: used to classify articles
  - rss_feeds:  AI-specific RSS sources per category
"""

CATEGORIES = {
    "business": {
        "emoji": "💰",
        "title": "Business & Funding",
        "subtitle": "AI deals, investments & economy",
        "keywords": [
            "funding", "investment", "acquisition", "acqui-hire", "startup",
            "venture capital", "series a", "series b", "series c", "ipo",
            "valuation", "revenue", "profit", "merger", "partnership",
            "raises", "round", "billion", "million", "investor",
            "enterprise ai", "saas", "b2b", "growth", "market cap",
        ],
        "rss_feeds": [
            "https://techcrunch.com/category/artificial-intelligence/feed/",
            "https://venturebeat.com/category/ai/feed/",
        ],
    },

    "developer_tools": {
        "emoji": "🛠️",
        "title": "Developer Tools",
        "subtitle": "APIs, SDKs, frameworks & open‑source drops",
        "keywords": [
            "api", "sdk", "open source", "github", "library", "framework",
            "model release", "weights", "fine-tuning", "rag", "llm",
            "langchain", "llamaindex", "hugging face", "transformer",
            "inference", "deployment", "docker", "kubernetes", "mlops",
            "benchmark", "eval", "code generation", "copilot", "cursor",
            "developer", "devtools", "cli", "plugin", "extension",
        ],
        "rss_feeds": [
            "https://huggingface.co/blog/feed.xml",
            "https://simonwillison.net/atom/everything/",
            "https://lilianweng.github.io/index.xml",
        ],
    },

    "research": {
        "emoji": "🔬",
        "title": "Research & Science",
        "subtitle": "Breakthroughs, papers & benchmarks",
        "keywords": [
            "research", "paper", "arxiv", "study", "published", "dataset",
            "breakthrough", "state of the art", "sota", "benchmark",
            "model architecture", "diffusion", "transformer", "attention",
            "multimodal", "reasoning", "alignment", "safety", "interpretability",
            "reinforcement learning", "reward model", "rlhf", "rlaif",
            "neuroscience", "cognitive", "deep learning", "neural network",
        ],
        "rss_feeds": [
            "https://deepmind.google/blog/rss.xml",
            "https://openai.com/blog/rss.xml",
            "https://blog.research.google/feeds/posts/default?alt=rss",
            "https://ai.meta.com/blog/rss/",
        ],
    },

    "creators": {
        "emoji": "🎨",
        "title": "Creators & Entertainment",
        "subtitle": "AI art, music, video, gaming & media",
        "keywords": [
            "ai art", "ai music", "ai video", "ai image", "generative art",
            "midjourney", "stable diffusion", "dalle", "sora", "runway",
            "text to image", "text to video", "text to music", "deepfake",
            "avatar", "virtual influencer", "gaming", "game ai",
            "creator economy", "content creation",
            "voiceover", "dubbing", "animation", "vfx",
        ],
        "rss_feeds": [
            "https://stability.ai/blog/feed",
        ],
    },

    "products": {
        "emoji": "📱",
        "title": "Products & Apps",
        "subtitle": "Consumer AI launches, updates & features",
        "keywords": [
            "launches", "release", "update", "new feature", "product",
            "app", "chatbot", "assistant", "chatgpt", "gemini", "claude",
            "perplexity", "copilot", "grok", "siri", "alexa",
            "wearable", "smart", "subscription", "pricing", "free tier",
            "beta", "waitlist", "general availability", "ga", "v2", "v3",
        ],
        "rss_feeds": [
            "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
            "https://9to5google.com/guides/google-ai/feed/",
        ],
    },

    "policy": {
        "emoji": "⚖️",
        "title": "Policy & Regulation",
        "subtitle": "Laws, ethics, governance & global AI policy",
        "keywords": [
            "regulation", "policy", "law", "government", "eu ai act",
            "executive order", "senate", "congress", "parliament",
            "gdpr", "privacy", "ban", "restriction", "compliance",
            "copyright", "ip", "intellectual property", "bias", "fairness",
            "ethics", "responsible ai", "safety", "risks", "threats",
            "fcc", "ftc", "nist", "un", "nato",
        ],
        "rss_feeds": [
            "https://www.wired.com/feed/category/artificial-intelligence/latest/rss",
        ],
    },

    "career": {
        "emoji": "🎓",
        "title": "Career & Education",
        "subtitle": "Jobs, courses, skills & AI in the workplace",
        "keywords": [
            "job", "hiring", "layoff", "workforce", "skills", "upskill",
            "course", "certification", "degree", "bootcamp", "learn ai",
            "prompt engineering", "career", "salary", "remote",
            "ai replaces", "automation jobs", "reskilling", "training",
            "university", "mooc", "coursera", "udemy", "openai academy",
        ],
        "rss_feeds": [],
    },

    "hardware": {
        "emoji": "🖥️",
        "title": "Hardware & Infrastructure",
        "subtitle": "Chips, GPUs, cloud & compute power",
        "keywords": [
            "gpu", "chip", "semiconductor", "nvidia", "amd", "intel",
            "tpu", "npu", "wafer", "fabrication", "tsmc",
            "data center", "cloud", "aws", "azure", "gcp", "supercomputer",
            "energy", "power", "cooling", "infrastructure", "cluster",
            "h100", "a100", "b200", "blackwell", "groq", "cerebras",
        ],
        "rss_feeds": [
            "https://semianalysis.com/feed/",
        ],
    },
}

# ─── Global AI-Focused RSS Feeds ────────────────────────────────────────────
# These are crawled for ALL categories (Gemini filters out non-AI articles)
GLOBAL_RSS_FEEDS = [
    # 🏆 Google News AI — free crawler, aggregates top AI news from the entire internet
    "https://news.google.com/rss/search?q=artificial+intelligence+OR+machine+learning+OR+LLM+OR+generative+AI&hl=en-US&gl=US&ceid=US:en",

    # 📰 Top AI-specific publications
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/ai/feed/",
    "https://www.artificialintelligence-news.com/feed/",
    "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    "https://arstechnica.com/tag/ai/feed/",

    # 🔬 AI Research Lab Blogs
    "https://openai.com/blog/rss.xml",
    "https://deepmind.google/blog/rss.xml",
    "https://blog.research.google/feeds/posts/default?alt=rss",
    "https://ai.meta.com/blog/rss/",
    "https://www.anthropic.com/rss",
    "https://huggingface.co/blog/feed.xml",

    # 📧 AI Newsletters (RSS)
    "https://simonwillison.net/atom/everything/",
    "https://www.marktechpost.com/feed/",
    "https://the-decoder.com/feed/",
]

# Category display order for messages
CATEGORY_ORDER = [
    "business", "developer_tools", "research", "products",
    "creators", "policy", "career", "hardware"
]
