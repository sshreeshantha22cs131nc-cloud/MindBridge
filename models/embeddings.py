"""
models/embeddings.py — Embedding Model Handler for MindBridge RAG
------------------------------------------------------------------
This file loads the sentence-transformer embedding model.
Embeddings convert text into numbers (vectors) so we can find
similar chunks of text using math (cosine similarity).

Think of it like this:
- "I feel sad" and "I am feeling depressed" → similar vectors → retrieved together
- "I feel sad" and "pizza recipe" → very different vectors → not related
"""

from sentence_transformers import SentenceTransformer
from config.config import EMBEDDING_MODEL

# ─────────────────────────────────────────────
# Load the embedding model ONCE globally
# (Loading models is slow, so we do it once and reuse)
# ─────────────────────────────────────────────
_embedding_model = None


def get_embedding_model() -> SentenceTransformer:
    """
    Returns the embedding model, loading it if not already loaded.
    This pattern is called 'lazy loading' — load only when needed.
    """
    global _embedding_model

    try:
        if _embedding_model is None:
            print(f"[INFO] Loading embedding model: {EMBEDDING_MODEL}")
            _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
            print("[INFO] Embedding model loaded successfully.")
        return _embedding_model

    except Exception as e:
        print(f"[ERROR] Failed to load embedding model: {e}")
        return None


def embed_texts(texts: list) -> list:
    """
    Converts a list of text strings into embedding vectors.

    Parameters:
    - texts: List of strings to embed

    Returns:
    - List of numpy arrays (one vector per text)
    """
    try:
        model = get_embedding_model()
        if model is None:
            return []
        embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings

    except Exception as e:
        print(f"[ERROR] Failed to embed texts: {e}")
        return []


def embed_query(query: str):
    """
    Converts a single query string into an embedding vector.

    Parameters:
    - query: The user's question

    Returns:
    - numpy array
    """
    try:
        model = get_embedding_model()
        if model is None:
            return None
        return model.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]

    except Exception as e:
        print(f"[ERROR] Failed to embed query: {e}")
        return None
