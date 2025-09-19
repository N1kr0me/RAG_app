# Customizable RAG Chatbot (Portfolio-Preset Included)

A modern, customizable Retrieval-Augmented Generation (RAG) chatbot that can answer questions based on your own documents. This repository includes a ready-made portfolio preset wired to answer questions about Nikhil, plus a clean structure to adapt for any use case.

## 🚀 Quick Start

### Frontend (Local Development)
```bash
# Start the local server
python server.py

# Open in browser
http://localhost:3000
# Default page served: frontend/pages/index.html
```

### Backend (Deployed on Render)
- URL: https://personal-chatbot-assistant.onrender.com
- Status: Live and running

## 📁 Project Structure

```
RAG_app/
├── frontend/                 # Web UI
│   ├── pages/               # Full-page experiences
│   │   └── index.html       # ChatGPT-like full chat (best UX)
│   └── embeds/              # Embeddable widgets
│       └── portfolio-full-chat.html  # Full chat experience with minimize support
├── src/                     # Backend Python code
│   ├── mcp_server.py        # FastAPI server (OpenAI + RAG)
│   ├── query.py             # Query processing
│   ├── embeddings.py        # Vector embeddings / Chroma
│   └── document_processor.py
├── data/                    # Knowledge base
│   └── documents/           # PDF files to ingest
├── config/                  # Configuration
│   └── config.json          # App settings
├── server.py                # Local dev static server (serves frontend/pages)
├── render.yaml              # Render deployment config
└── requirements.txt         # Python dependencies
```

## 🧩 What You Get

- Full ChatGPT-like chat UI (pages/index.html)
- Embeddable full-chat widget (embeds/portfolio-full-chat.html)
- Butler-style polite assistant, focused on answering about the provided documents
- Chat memory of the last 5 exchanges (per session)
- Automatic document processing on startup (server)

## 🛠️ Configure For Your Own Use

1. Replace documents:
   - Drop your PDFs into `data/documents/`
2. Redeploy or restart backend:
   - On Render, manual deploy
   - Or run locally via uvicorn if you prefer
3. Update system persona (optional):
   - Edit `src/mcp_server.py` system prompt to change assistant persona/purpose

## 🌐 Using The Frontend

- Full-page experience (recommended):
  - Open `http://localhost:3000` (serves `frontend/pages/index.html`)
- Embed in your website:
  - Use `frontend/embeds/portfolio-full-chat.html` and paste into your site

## 🔌 API Endpoints

- `GET /health` - Health check
- `POST /query` - Ask questions `{ query, chat_history? }`
- `POST /process` - Manually (re)process documents

## ⚙️ Tech

- FastAPI + Uvicorn backend
- OpenAI chat + LangChain embeddings (ChromaDB)
- Static HTML/CSS/JS frontend (no build step)

## 🔒 Environment

- Set `OPENAI_API_KEY` in Render (or your environment)
- Optional: `OPENAI_MODEL` (default: `gpt-3.5-turbo`)

## 📦 Install
```bash
pip install -r requirements.txt
```

## 📝 License
MIT
