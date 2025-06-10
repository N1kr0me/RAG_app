# RAG System with Ollama Integration

A Retrieval-Augmented Generation (RAG) system built with OpenAI embeddings, LangChain, and Ollama for lightweight deployment.

## Features

- PDF document processing and chunking
- OpenAI embeddings for semantic search (optional)
- Chroma vector store for efficient retrieval
- Ollama integration with phi:2.7b model
- Docker support for easy deployment
- GitHub Actions workflow for CI/CD
- Frontend deployment to GitHub Pages

## Setup

### Local Development

1. Clone the repository:
```batch
git clone <repository-url>
cd rag-system
```

2. Create and activate a virtual environment:
```batch
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```batch
pip install -r requirements.mcp.txt
```

4. Set up configuration:
```batch
copy config\config.template.json config\config.json
```

5. (Optional) Set your OpenAI API key for production use:
```batch
set OPENAI_API_KEY=your-api-key-here
```
Note: The system will work without an API key in development mode using mock embeddings.

### Docker Setup

1. Install Docker Desktop
2. Build and run the containers:
```batch
docker-compose up --build
```

## Usage

### CLI Interface

1. Place your PDF documents in the `data/documents` directory.

2. Process the documents:
```batch
python -m src.cli process
```

3. Query the system:
```batch
python -m src.cli query "your question here" --chat
```

### API Endpoints

The MCP server provides the following endpoints:

- `POST /query`: Query the system with chat history
  ```json
  {
    "query": "your question",
    "chat_history": [
      {"role": "user", "content": "previous question"},
      {"role": "assistant", "content": "previous answer"}
    ]
  }
  ```

- `POST /process`: Process documents
  ```json
  {
    "reset": false
  }
  ```

## Project Structure

```
.
├── config/
│   ├── config.json
│   └── config.template.json
├── data/
│   ├── documents/     # PDF storage
│   └── vector_store/  # Vector database
├── src/
│   ├── cli.py
│   ├── document_processor.py
│   ├── embeddings.py
│   ├── mcp_server.py
│   └── query.py
├── frontend/          # GitHub Pages frontend
├── docker-compose.yml
├── Dockerfile.mcp
├── requirements.mcp.txt
└── .github/workflows/
    └── deploy.yml
```

## Deployment

The system is configured for deployment using GitHub Actions:

1. Backend: GitHub Actions (free tier)
   - Processes documents
   - Runs MCP server
   - Integrates with Ollama

2. Frontend: GitHub Pages (free)
   - Static site hosting
   - Automatic deployment on push

3. Storage: GitHub LFS (1GB free)
   - Document storage
   - Vector store persistence

## Development Notes

- Uses Ollama's phi:2.7b model for lightweight deployment
- Docker setup optimized for local development
- Windows-specific implementation
- All paths use Windows backslash (\) format
- Development mode available without OpenAI API key

## License

MIT License - see LICENSE file for details
