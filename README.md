# 📜 Game of Thrones AI Chatbot

### A Fully Custom RAG + LLM Chatbot with Character Voices, Lore-Based Answers & Stunning Streamlit UI

<p align="center">
  <img src="assets/got_logo.jpg" width="40%">
</p>

This project is a **Game of Thrones conversational AI chatbot** powered by:

- **RAG (Retrieval-Augmented Generation)**
- **ChromaDB vector embeddings**
- **Local sentence-transformer embeddings**
- **OpenAI GPT for response generation**
- **Selectable character voices (Tyrion, Jon Snow, Arya, Daenerys, Cersei, Raven)**
- **Dark-theme, avatar-based Streamlit UI**

<!-- The chatbot answers **strictly using the Game of Thrones lore PDF you provide** and rejects out-of-universe questions. -->

---

# ⚔️ Features

### 🧙 Lore-Grounded RAG Responses

- Answers only from your GOT PDF
- Strict rules ensure lore consistency
- Rejects questions unrelated to GOT universe

### 🎭 Character Mode

Respond in the tone of:

- Tyrion Lannister
- Jon Snow
- Arya Stark
- Daenerys Targaryen
- Cersei Lannister
- Raven (neutral)

### 🎨 Stunning Streamlit UI

- Dark mode
- Avatar icons
- Left/right aligned chat bubbles
- GOT banner styling
- Clean headers & typography

### 🧠 Long-Term Memory Engine

Stores important conversation facts (configurable).

### ⚙️ Fast Vector Search (ChromaDB + Sentence Transformers)

- PDF → Text → Chunks → Embeddings
- Local vector store (not uploaded to GitHub)
- Real-time similarity search

---

# 📂 Project Structure

```
game-of-thrones-gpt/
│
├── assets/                     # Avatars, icons, banners, logo images
│   ├── got_banner.png
│   ├── got_logo.png
│   ├── tyrion.png
│   ├── jon.png
│   ├── arya.png
│   ├── daenerys.png
│   ├── cersei.png
│   └── raven.png
│
├── data/                       # Your GoT lore PDF (not included in GitHub)
│   └── got_lore.pdf
│
├── vector_store/               # Local Chroma vector database (ignored in Git)
│   └── chroma.sqlite3
│
├── got_env/                    # Optional local virtual environment (ignored)
│
├── chatbot_core.py             # Main logic: LLM + RAG + persona prompts
├── rag_engine.py               # PDF loading, chunking, embeddings, retrieval
├── memory_engine.py            # Conversational long-term memory handler
├── prompts.py                  # System prompts, strict rules, persona prompts
├── build_rag_index.py          # One-time script to build vector DB from PDF
├── ui.py                       # Beautiful Streamlit front-end (UI)
├── config.py                   # API keys, model name, paths (not pushed to GitHub)
│
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Excludes vector store, env, config, etc.
```

---

### 🚀 How It Works

1. Load your GoT lore PDF → The system breaks it into chunks
2. Each chunk is embedded using Sentence Transformers
3. ChromaDB stores the embeddings locally
4. When a question is asked:
   - The vector DB retrieves relevant chunks
   - These chunks are injected into the system prompt
5. GPT generates character-style, lore-accurate replies
6. Streamlit UI renders the chat with avatars & dark theme

---

### 🛠️ Installation

```
git clone https://github.com/NeelDevX/game-of-thrones-GPT.git
cd game-of-thrones-GPT
python3 -m venv got_env
source got_env/bin/activate
pip install -r requirements.txt
```

---

### 📘 Building Vector Store (Run Once)

```
python build_rag_index.py
```

---

### 🔑 Add your OpenAI API key in config.py:

```
OPENAI_API_KEY = "your_key_here"
MODEL_NAME = "gpt-4o-mini"
```
