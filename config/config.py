"""
config.py — All API keys and settings for MindBridge
------------------------------------------------------
IMPORTANT: Never share this file publicly or push it to GitHub as-is.
When uploading to GitHub, replace actual keys with os.environ.get() calls.
"""

import os

# ─────────────────────────────────────────────
# GROQ API KEY — get yours free at https://console.groq.com
# ─────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "")

# ─────────────────────────────────────────────
# SERPER API KEY — free web search API at https://serper.dev
# Used for live web search feature
# ─────────────────────────────────────────────

#SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "")

# ─────────────────────────────────────────────
# LLM SETTINGS
# ─────────────────────────────────────────────
GROQ_MODEL = "llama-3.3-70b-versatile"         # Fast, free Groq model
MAX_TOKENS_CONCISE = 300               # Short replies
MAX_TOKENS_DETAILED = 1024             # Long, in-depth replies
TEMPERATURE = 0.7                      # Controls creativity (0=robotic, 1=creative)

# ─────────────────────────────────────────────
# RAG (Document Retrieval) SETTINGS
# ─────────────────────────────────────────────
CHUNK_SIZE = 500          # How many characters per document chunk
CHUNK_OVERLAP = 50        # Overlap between chunks to avoid losing context
TOP_K_RESULTS = 3         # How many chunks to retrieve per query
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Free, lightweight embedding model

# ─────────────────────────────────────────────
# APP SETTINGS
# ─────────────────────────────────────────────
APP_TITLE = "MindBridge"
APP_SUBTITLE = "Your Emotional Wellness Companion"
APP_ICON = "🧠"
