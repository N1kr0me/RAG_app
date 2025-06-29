# RAG Chatbot Backend

This project is a Retrieval-Augmented Generation (RAG) chatbot backend that uses OpenAI's API (gpt-3.5-turbo or gpt-4o) to answer questions based on your documents (PDFs, text, etc.).

## Features
- Ingests and indexes your documents for semantic search
- Uses OpenAI API for chat completions
- REST API endpoints for chat and document processing
- Ready to integrate with any frontend (including WordPress via widget)

## Requirements
- Python 3.11+
- OpenAI API key (set as `OPENAI_API_KEY` environment variable)

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.mcp.txt
   ```
3. **Set your OpenAI API key**
   ```bash
   set OPENAI_API_KEY=sk-...   # Windows
   export OPENAI_API_KEY=sk-... # Linux/Mac
   ```
4. **Prepare your documents**
   - Place PDFs and other supported files in the `data/documents/` directory.
5. **Process documents**
   ```bash
   python -m src.cli process
   ```
6. **Start the server**
   ```bash
   python -m src.mcp_server
   ```

## API Endpoints
- `POST /query` — Query the chatbot with a question
- `POST /process` — Re-process all documents
- `GET /health` — Health check

## Notes
- The backend no longer uses Llama/Ollama or Docker. All completions are via OpenAI API.
- You can change the model by setting the `OPENAI_MODEL` environment variable (default: `gpt-3.5-turbo`).

## Integrating with WordPress
- Use a JavaScript widget or iframe to connect your WordPress frontend to this backend's `/query` endpoint.

## License
MIT
