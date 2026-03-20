"""
utils/mood_tracker_utils.py — Mood Detection & Tracking (Bonus Feature!)
-------------------------------------------------------------------------
This module detects the emotional tone of user messages
and tracks mood patterns across the conversation.

This is what makes MindBridge stand out — it's not just a chatbot,
it actually understands HOW you're feeling and adjusts accordingly.
"""

# ─────────────────────────────────────────────
# Simple keyword-based mood detection
# (No extra API needed — works offline!)
# ─────────────────────────────────────────────

MOOD_KEYWORDS = {
    "😢 Sad": [
        "sad", "unhappy", "miserable", "depressed", "crying", "cry",
        "tears", "heartbroken", "grief", "loss", "lonely", "alone",
        "hopeless", "worthless", "empty", "numb", "hurt"
    ],
    "😰 Anxious": [
        "anxious", "anxiety", "worried", "worry", "nervous", "panic",
        "panic attack", "fear", "scared", "terrified", "overwhelmed",
        "stress", "stressed", "tension", "tense", "dread", "uneasy"
    ],
    "😤 Angry": [
        "angry", "anger", "furious", "rage", "mad", "frustrated",
        "frustration", "irritated", "annoyed", "hatred", "hate",
        "resentment", "bitter", "fed up"
    ],
    "😊 Positive": [
        "happy", "good", "great", "better", "hopeful", "grateful",
        "thankful", "calm", "peaceful", "relaxed", "joy", "excited",
        "motivated", "confident", "proud", "relieved", "content"
    ],
    "😔 Exhausted": [
        "tired", "exhausted", "burnout", "burn out", "drained",
        "fatigue", "fatigued", "no energy", "can't sleep", "insomnia",
        "sleepless", "worn out"
    ],
    "🤔 Confused": [
        "confused", "lost", "don't know", "unsure", "uncertain",
        "stuck", "don't understand", "unclear", "mixed up"
    ]
}

# Crisis keywords — need immediate attention
CRISIS_KEYWORDS = [
    "suicide", "suicidal", "kill myself", "end my life", "want to die",
    "self harm", "self-harm", "cutting", "hurt myself", "no reason to live",
    "better off dead", "can't go on"
]

CRISIS_RESPONSE = """
🆘 **I'm genuinely concerned about you right now.**

Please reach out to these free, confidential helplines immediately:

🇮🇳 **India-specific:**
- **iCall (TISS):** 9152987821 — Mon–Sat, 8am–10pm
- **Vandrevala Foundation:** 1860-2662-345 — 24/7
- **AASRA:** 9820466627 — 24/7
- **iCall Chat:** icallhelpline.org

You are not alone. These trained counselors are here for you. 💙
"""


def detect_mood(message: str) -> str:
    """
    Detects the primary mood from a user's message.

    Parameters:
    - message: User's input text

    Returns:
    - Mood label string like "😢 Sad" or "😊 Positive"
    """
    try:
        message_lower = message.lower()
        mood_scores = {}

        for mood, keywords in MOOD_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                mood_scores[mood] = score

        if not mood_scores:
            return "😐 Neutral"

        # Return the mood with highest keyword matches
        return max(mood_scores, key=mood_scores.get)

    except Exception as e:
        print(f"[ERROR] Mood detection failed: {e}")
        return "😐 Neutral"


def is_crisis_message(message: str) -> bool:
    """
    Checks if a message contains crisis/emergency signals.

    Parameters:
    - message: User's input

    Returns:
    - True if crisis keywords detected
    """
    try:
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in CRISIS_KEYWORDS)
    except Exception as e:
        print(f"[ERROR] Crisis detection failed: {e}")
        return False


def get_mood_color(mood: str) -> str:
    """
    Returns a CSS color for a given mood (used in UI).
    """
    mood_colors = {
        "😢 Sad": "#6B9BD2",
        "😰 Anxious": "#F4A261",
        "😤 Angry": "#E76F51",
        "😊 Positive": "#52B788",
        "😔 Exhausted": "#9B8EA8",
        "🤔 Confused": "#E9C46A",
        "😐 Neutral": "#ADB5BD"
    }
    return mood_colors.get(mood, "#ADB5BD")


def get_mood_affirmation(mood: str) -> str:
    """
    Returns a short affirmation message based on detected mood.
    """
    affirmations = {
        "😢 Sad": "It's okay to feel sad. Your feelings are valid. 💙",
        "😰 Anxious": "Take a deep breath. You are safe in this moment. 🌸",
        "😤 Angry": "Your anger is telling you something important. Let's explore it. 🔥",
        "😊 Positive": "It's wonderful that you're feeling good! Let's keep that going. 🌟",
        "😔 Exhausted": "Rest is not giving up. Taking care of yourself is brave. 🌙",
        "🤔 Confused": "Feeling lost is okay. Let's work through this together. 🧭",
        "😐 Neutral": "I'm here to listen, whatever you'd like to talk about. 💬"
    }
    return affirmations.get(mood, "I'm here for you. 💙")
