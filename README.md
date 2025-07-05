# Nikhil's AI Assistant

A modern AI-powered chatbot that can answer questions about Nikhil based on his CV and other documents.

## 🚀 Quick Start

### Frontend (Local Development)
```bash
# Start the local server
python server.py

# Open in browser
http://localhost:3000
```

### Backend (Deployed on Render)
- **URL**: https://personal-chatbot-assistant.onrender.com
- **Status**: Live and running
- **Auto-deploy**: Enabled via GitHub

## 📁 Project Structure

```
RAG_app/
├── frontend/           # Web interface
│   ├── index.html     # Main AI Assistant UI
│   └── README.md      # Frontend documentation
├── src/               # Backend Python code
│   ├── mcp_server.py  # FastAPI server
│   ├── query.py       # Query processing
│   ├── embeddings.py  # Vector embeddings
│   └── document_processor.py
├── data/              # Knowledge base
│   └── documents/     # PDF files (CV, etc.)
├── config/            # Configuration
│   └── config.json    # App settings
├── server.py          # Local development server
├── render.yaml        # Render deployment config
└── requirements.txt   # Python dependencies
```

## 🔧 Setup

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
# Add your OpenAI API key to Render environment variables
```

### Adding Documents
1. Place PDF files in `data/documents/`
2. Deploy to Render (auto-deploys on push)
3. Process documents via `/process` endpoint

## 🌐 Deployment

- **Frontend**: Local development (or deploy to any static hosting)
- **Backend**: Render.com (auto-deploys from GitHub)
- **Database**: ChromaDB (vector store)

## 📝 Features

- Modern chat interface
- Real-time AI responses
- Document-based knowledge base
- Responsive design
- CORS enabled for cross-origin requests

## 🔗 API Endpoints

- `GET /health` - Health check
- `POST /query` - Ask questions
- `POST /process` - Process documents

## 📄 License

MIT License - see LICENSE file for details
