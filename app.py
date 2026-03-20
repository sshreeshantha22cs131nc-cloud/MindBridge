"""
app.py — MindBridge: Your Emotional Wellness Companion
=======================================================
Main Streamlit application file.
This is where everything comes together — UI, RAG, web search, LLM.

To run: streamlit run app.py
"""

import streamlit as st
import time

# ── Import our custom modules ──
from config.config import APP_TITLE, APP_SUBTITLE, APP_ICON
from models.llm import get_llm_response
from utils.rag_utils import process_uploaded_file, retrieve_relevant_chunks
from utils.web_search_utils import search_web, should_search_web
from utils.mood_tracker_utils import (
    detect_mood, is_crisis_message, get_mood_color,
    get_mood_affirmation, CRISIS_RESPONSE
)

# ─────────────────────────────────────────────
# PAGE CONFIGURATION — must be first Streamlit call
# ─────────────────────────────────────────────
st.set_page_config(
    page_title=f"{APP_ICON} {APP_TITLE}",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Beautiful calming design
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Import Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

    /* ── Global Styles ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Background ── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    /* ── Main Title ── */
    .main-title {
        font-family: 'DM Serif Display', serif;
        font-size: 3rem;
        background: linear-gradient(90deg, #a8edea, #fed6e3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }

    .main-subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 1rem;
        font-weight: 300;
        margin-bottom: 1.5rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* ── Chat Messages ── */
    .user-bubble {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.95rem;
        line-height: 1.5;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .bot-bubble {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #e2e8f0;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 85%;
        font-size: 0.95rem;
        line-height: 1.6;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    /* ── Mood Badge ── */
    .mood-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 6px;
        opacity: 0.85;
    }

    /* ── Source Tag ── */
    .source-tag {
        display: inline-block;
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 2px 8px;
        font-size: 0.7rem;
        color: #a0aec0;
        margin-top: 6px;
        margin-right: 4px;
    }

    /* ── Sidebar ── */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.9) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* ── Sidebar Text ── */
    .sidebar-header {
        font-family: 'DM Serif Display', serif;
        font-size: 1.3rem;
        color: #a8edea;
        margin-bottom: 0.5rem;
    }

    /* ── Input Box ── */
    .stTextInput input, .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        color: white !important;
        border-radius: 12px !important;
    }

    /* ── Buttons ── */
    .stButton button {
        background: linear-gradient(135deg, #a8edea, #fed6e3) !important;
        color: #1a1a2e !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 8px 24px !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(168, 237, 234, 0.3) !important;
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(255,255,255,0.07) !important;
    }

    /* ── Status indicators ── */
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #52B788;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    /* ── Metric Cards ── */
    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        margin: 4px 0;
    }
    .metric-number {
        font-size: 1.8rem;
        font-weight: 600;
        color: #a8edea;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ── Hide Streamlit branding ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# Session state persists data across reruns
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []          # Chat history

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None    # Uploaded document embeddings

if "mood_history" not in st.session_state:
    st.session_state.mood_history = []      # Track moods over time

if "message_count" not in st.session_state:
    st.session_state.message_count = 0

if "web_searches" not in st.session_state:
    st.session_state.web_searches = 0


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:

    # ── Logo & Branding ──
    st.markdown('<p class="sidebar-header">🧠 MindBridge</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#718096;font-size:0.8rem;">Emotional Wellness Companion</p>', unsafe_allow_html=True)
    st.divider()

    # ── Response Mode Toggle ──
    st.markdown("**⚙️ Response Mode**")
    response_mode = st.radio(
        label="Select how MindBridge responds:",
        options=["Concise", "Detailed"],
        index=1,
        help="Concise: Short 2-3 sentence replies. Detailed: In-depth responses with techniques."
    )
    st.caption("💡 Use **Concise** for quick support. Use **Detailed** for deeper understanding.")
    st.divider()

    # ── Web Search Toggle ──
    st.markdown("**🌐 Live Web Search**")
    enable_web_search = st.toggle(
        "Enable web search",
        value=True,
        help="Searches the web for latest mental health resources, helplines, and articles."
    )
    if enable_web_search:
        st.caption('<span class="status-dot"></span>Web search is active', unsafe_allow_html=True)
    st.divider()

    # ── Document Upload (RAG) ──
    st.markdown("**📄 Knowledge Base (RAG)**")
    st.caption("Upload a mental health guide, CBT worksheet, or wellness document.")

    uploaded_file = st.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt"],
        help="Your document will be processed and MindBridge will use it to answer questions."
    )

    if uploaded_file:
        with st.spinner("📚 Processing your document..."):
            vector_store = process_uploaded_file(uploaded_file)

            if "error" in vector_store and vector_store["error"]:
                st.error(f"❌ {vector_store['error']}")
            else:
                st.session_state.vector_store = vector_store
                st.success(f"✅ **{uploaded_file.name}** loaded!")
                st.caption(f"📊 {vector_store.get('total_chunks', 0)} knowledge chunks created")

    if st.session_state.vector_store:
        st.info(f"📖 Active: **{st.session_state.vector_store.get('filename', 'Document')}**")

    st.divider()

    # ── Session Stats ──
    st.markdown("**📊 Session Stats**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{st.session_state.message_count}</div>
            <div class="metric-label">Messages</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{st.session_state.web_searches}</div>
            <div class="metric-label">Searches</div>
        </div>""", unsafe_allow_html=True)

    # ── Mood History ──
    if st.session_state.mood_history:
        st.markdown("**🎭 Recent Moods**")
        recent_moods = st.session_state.mood_history[-5:]
        for mood in reversed(recent_moods):
            st.caption(mood)

    st.divider()

    # ── Clear Chat ──
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.session_state.mood_history = []
        st.session_state.message_count = 0
        st.session_state.web_searches = 0
        st.rerun()

    # ── Emergency Resources ──
    with st.expander("🆘 Emergency Resources"):
        st.markdown("""
        **India Helplines (Free & 24/7)**
        - **iCall:** 9152987821
        - **Vandrevala:** 1860-2662-345
        - **AASRA:** 9820466627
        - **Snehi:** 044-24640050
        """)


# ─────────────────────────────────────────────
# MAIN CHAT AREA
# ─────────────────────────────────────────────

# ── Header ──
st.markdown('<h1 class="main-title">MindBridge</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Your Safe Space to Talk · Understand · Heal</p>', unsafe_allow_html=True)

# ── Welcome message (shown when chat is empty) ──
if not st.session_state.messages:
    st.markdown("""
    <div style="
        background: rgba(168, 237, 234, 0.05);
        border: 1px solid rgba(168, 237, 234, 0.15);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin: 20px 0;
    ">
        <p style="font-size:2rem; margin:0;">🌙</p>
        <p style="color:#a8edea; font-size:1.1rem; margin:8px 0; font-family:'DM Serif Display',serif;">
            Welcome. You're in a safe space.
        </p>
        <p style="color:#718096; font-size:0.9rem; margin:0; line-height:1.6;">
            MindBridge is here to listen, support, and guide you.<br>
            Share what's on your mind — there's no judgment here.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick start prompts
    st.markdown('<p style="color:#4a5568; text-align:center; font-size:0.85rem; margin:16px 0 8px;">Try asking...</p>', unsafe_allow_html=True)
    cols = st.columns(3)
    prompts = [
        "😰 I'm feeling overwhelmed with stress",
        "😴 I can't sleep because of anxiety",
        "💭 How do I deal with negative thoughts?"
    ]
    for col, prompt in zip(cols, prompts):
        with col:
            if st.button(prompt, use_container_width=True):
                st.session_state.prefill = prompt
                st.rerun()

# ── Display Chat History ──
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display:flex; justify-content:flex-end; margin:8px 0;">
                <div class="user-bubble">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)
        else:
            # Build source tags
            source_tags = ""
            if msg.get("used_rag"):
                source_tags += '<span class="source-tag">📄 From Document</span>'
            if msg.get("used_web"):
                source_tags += '<span class="source-tag">🌐 Web Search</span>'

            mood_badge = ""
            if msg.get("mood") and msg["mood"] != "😐 Neutral":
                color = get_mood_color(msg["mood"])
                mood_badge = f'<div><span class="mood-badge" style="background:{color}22; color:{color}; border:1px solid {color}44;">{msg["mood"]} detected</span></div>'

            # Render bot label
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px; margin-top:8px;">
                <span style="font-size:1.2rem;">🧠</span>
                <span style="color:#718096; font-size:0.75rem;">MindBridge</span>
            </div>""", unsafe_allow_html=True)

            # Render message content safely
            st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

            # Render source + mood badges
            if source_tags or mood_badge:
                st.markdown(source_tags + mood_badge, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CHAT INPUT & RESPONSE LOGIC
# ─────────────────────────────────────────────
prefill_value = st.session_state.pop("prefill", "") if "prefill" in st.session_state else ""

user_input = st.chat_input(
    placeholder="Share what's on your mind... 💬",
)

# Also handle quick-start prompt clicks
if not user_input and prefill_value:
    user_input = prefill_value

if user_input and user_input.strip():
    # ── Add user message to history ──
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.message_count += 1

    # ── Detect mood ──
    detected_mood = detect_mood(user_input)
    if detected_mood not in st.session_state.mood_history:
        st.session_state.mood_history.append(detected_mood)

    # ── Check for crisis ──
    if is_crisis_message(user_input):
        st.session_state.messages.append({
            "role": "assistant",
            "content": CRISIS_RESPONSE,
            "mood": detected_mood,
            "used_rag": False,
            "used_web": False
        })
        st.rerun()

    # ── Build context from RAG and/or Web Search ──
    context = ""
    used_rag = False
    used_web = False

    with st.spinner("🧠 MindBridge is thinking..."):

        # Step 1: Try RAG (document retrieval)
        if st.session_state.vector_store and st.session_state.vector_store.get("chunks"):
            rag_context = retrieve_relevant_chunks(user_input, st.session_state.vector_store)
            if rag_context:
                context += f"[From your uploaded document]\n{rag_context}\n\n"
                used_rag = True

        # Step 2: Try web search if enabled and relevant
        if enable_web_search and should_search_web(user_input):
            time.sleep(0.3)  # Small delay to avoid rate limits
            web_context = search_web(f"mental health {user_input} India")
            if web_context and "⚠️" not in web_context:
                context += f"[From live web search]\n{web_context}"
                used_web = True
                st.session_state.web_searches += 1

        # Step 3: Build chat history for LLM memory
        chat_history = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[:-1]  # Exclude the current message
        ]

        # Step 4: Get LLM response
        bot_response = get_llm_response(
            user_message=user_input,
            context=context,
            mode=response_mode,
            chat_history=chat_history
        )

    # ── Add mood affirmation if mood detected ──
    affirmation = get_mood_affirmation(detected_mood)
    if detected_mood != "😐 Neutral" and affirmation not in bot_response:
        bot_response = f"*{affirmation}*\n\n{bot_response}"

    # ── Save assistant response ──
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response,
        "mood": detected_mood,
        "used_rag": used_rag,
        "used_web": used_web
    })

    st.rerun()
