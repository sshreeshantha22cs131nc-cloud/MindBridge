# 🧠 MindBridge — Your Emotional Wellness Companion

> *"You don't have to face it alone."*

MindBridge is an intelligent mental health chatbot built with Streamlit and powered by Groq's LLaMA3 model. It combines RAG (document-based knowledge retrieval), live web search, and real-time mood detection to provide empathetic, contextual emotional support.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **LLM (Groq/LLaMA3)** | Fast, free AI responses with memory |
| 📄 **RAG Integration** | Upload mental health PDFs — chatbot learns from them |
| 🌐 **Live Web Search** | Finds real-time helplines, resources, articles |
| 🎭 **Mood Detection** | Detects emotional tone and responds accordingly |
| ⚡ **Response Modes** | Switch between Concise and Detailed replies |
| 🆘 **Crisis Detection** | Immediately surfaces emergency helplines |
| 💅 **Beautiful UI** | Calming dark design with smooth animations |

---

## 🚀 Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/mindbridge.git
cd mindbridge
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API keys
Open `config/config.py` and replace:
- `"your_groq_api_key_here"` → your key from https://console.groq.com
- `"your_serper_api_key_here"` → your key from https://serper.dev

### 5. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
mindbridge/
├── config/
│   └── config.py          ← API keys & settings
├── models/
│   ├── llm.py             ← Groq LLM handler
│   └── embeddings.py      ← RAG embedding model
├── utils/
│   ├── rag_utils.py       ← Document processing & retrieval
│   ├── web_search_utils.py← Live web search
│   └── mood_tracker_utils.py ← Mood detection
├── app.py                 ← Main Streamlit app
├── requirements.txt
└── README.md
```

---

## 🌐 Live Demo
[View on Streamlit Cloud](YOUR_DEPLOYMENT_LINK_HERE)

---

## ⚠️ Disclaimer
MindBridge is NOT a substitute for professional therapy or medical advice. If you are in crisis, please contact a mental health professional immediately.

**India Helplines:**
- iCall (TISS): 9152987821
- Vandrevala Foundation: 1860-2662-345
- AASRA: 9820466627

