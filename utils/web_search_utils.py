"""
utils/web_search_utils.py — Live Web Search for MindBridge
-----------------------------------------------------------
When the LLM doesn't have enough knowledge (or the user asks
about current events, latest resources, helplines, etc.),
we use the Serper API to do a real Google search.

Serper is a free Google Search API:
Sign up at https://serper.dev to get your free API key (2500 free searches/month)
"""

import requests
import json
from config.config import SERPER_API_KEY


# Serper API endpoint
SERPER_URL = "https://google.serper.dev/search"


def search_web(query: str, num_results: int = 4) -> str:
    """
    Performs a live web search using Serper API.

    Parameters:
    - query: The search query string
    - num_results: How many results to return (default 4)

    Returns:
    - Formatted string of search results
    """
    try:
        # ── Validate API key ──
        if not SERPER_API_KEY or SERPER_API_KEY == "your_serper_api_key_here":
            return "⚠️ Web search is not configured. Please add your Serper API key in the .env file."

        # ── Make the API request ──
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": num_results,
            "gl": "in",   # India-focused results
            "hl": "en"
        }

        response = requests.post(SERPER_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()  # Raises error if status code is 4xx/5xx

        data = response.json()

        # ── Parse and format results ──
        results_text = ""

        # Answer box (if Google shows a direct answer)
        if "answerBox" in data:
            answer = data["answerBox"].get("answer") or data["answerBox"].get("snippet", "")
            if answer:
                results_text += f"Quick Answer: {answer}\n\n"

        # Organic search results
        organic = data.get("organic", [])
        if not organic:
            return "No relevant search results found."

        for i, result in enumerate(organic[:num_results], 1):
            title = result.get("title", "No title")
            snippet = result.get("snippet", "No description available")
            link = result.get("link", "")
            results_text += f"{i}. {title}\n{snippet}\nSource: {link}\n\n"

        return results_text.strip() if results_text else "No useful results found."

    except requests.exceptions.Timeout:
        return "⚠️ Web search timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"⚠️ Web search failed: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected error during web search: {str(e)}"


def should_search_web(user_message: str) -> bool:
    """
    Decides if a web search would help answer this question.
    Looks for keywords that suggest current/external information is needed.

    Parameters:
    - user_message: The user's input

    Returns:
    - True if web search is recommended, False otherwise
    """
    try:
        # Keywords that suggest we need live/external information
        search_triggers = [
            "helpline", "hotline", "contact", "number", "call",
            "latest", "recent", "current", "2024", "2025",
            "hospital", "doctor", "clinic", "therapist", "psychiatrist",
            "app", "website", "resource", "where can i",
            "how to find", "recommend", "suggest", "near me",
            "india", "bangalore", "delhi", "mumbai",
            "medication", "medicine", "drug", "treatment center",
            "ngo", "organization", "support group"
        ]

        message_lower = user_message.lower()
        return any(trigger in message_lower for trigger in search_triggers)

    except Exception as e:
        print(f"[ERROR] Failed to evaluate search trigger: {e}")
        return False
