"""
models/llm.py — LLM Model Handler for MindBridge
--------------------------------------------------
This file manages all communication with the Groq LLM API.
It builds the right prompt based on response mode and context.
"""

from groq import Groq
from config.config import GROQ_API_KEY, GROQ_MODEL, MAX_TOKENS_CONCISE, MAX_TOKENS_DETAILED, TEMPERATURE


# ─────────────────────────────────────────────
# Initialize Groq client once (reused across calls)
# ─────────────────────────────────────────────
try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"[ERROR] Failed to initialize Groq client: {e}")
    client = None


# ─────────────────────────────────────────────
# SYSTEM PROMPT — defines MindBridge's personality
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """
You are MindBridge, a warm, empathetic, and non-judgmental emotional wellness companion.
Your purpose is to provide emotional support, mental health information, and coping strategies.

Guidelines:
- Always respond with compassion and kindness
- Never diagnose or prescribe medication
- Always encourage professional help for serious issues
- Use simple, clear language that anyone can understand
- If someone seems in crisis, always provide emergency resources (iCall: 9152987821, Vandrevala Foundation: 1860-2662-345)
- Draw from the provided context (documents/web search) when available
- Be culturally sensitive — many users are from India

You are NOT a replacement for professional therapy. You are a supportive first step.
"""


def get_llm_response(user_message: str, context: str = "", mode: str = "Detailed", chat_history: list = []) -> str:
    """
    Gets a response from Groq LLM.

    Parameters:
    - user_message: What the user typed
    - context: Retrieved text from RAG or web search (can be empty)
    - mode: "Concise" or "Detailed"
    - chat_history: List of previous messages for memory

    Returns:
    - LLM response as a string
    """

    # Validate client
    if client is None:
        return "⚠️ I'm having trouble connecting right now. Please check your API key in config/config.py."

    try:
        # ── Build the mode instruction ──
        if mode == "Concise":
            mode_instruction = "Give a SHORT, focused response in 2-3 sentences maximum. Be warm but brief."
            max_tokens = MAX_TOKENS_CONCISE
        else:
            mode_instruction = "Give a DETAILED, thorough response with explanation, techniques, and encouragement."
            max_tokens = MAX_TOKENS_DETAILED

        # ── Build context block (from RAG or web search) ──
        context_block = ""
        if context and context.strip():
            context_block = f"""
Relevant information retrieved for this query:
---
{context}
---
Use the above information to support your response where relevant.
"""

        # ── Combine into full system prompt ──
        full_system = SYSTEM_PROMPT + f"\n\nResponse Style: {mode_instruction}" + context_block

        # ── Build message history ──
        # Start with system message
        messages = [{"role": "system", "content": full_system}]

        # Add previous chat history (last 6 exchanges for memory)
        for msg in chat_history[-6:]:
            messages.append(msg)

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # ── Call Groq API ──
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=TEMPERATURE,
        )

        # Extract and return the text
        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Something went wrong while generating a response: {str(e)}"
