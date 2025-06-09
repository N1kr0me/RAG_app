# Personal RAG System

A Retrieval-Augmented Generation (RAG) system for your personal documents. This system allows you to create a knowledge base from your PDF documents (CV, projects, etc.) and query it using natural language.

## Setup

1. Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Set up your API key in one of two ways:
   - Set as environment variable:
     ```bash
     export OPENAI_API_KEY=your-api-key-here
     ```
   - Or add to `config/config.json`:
     ```json
     {
         "embedding": {
             "api_key": "your-api-key-here"
         }
     }
     ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your PDF documents in the `data/documents` directory
2. Process the documents:
   ```bash
   python -m src.cli process
   ```
3. Query the system:
   ```bash
   python -m src.cli query "What projects have you worked on?"
   ```

## Cost Estimation

The system uses OpenAI's `text-embedding-3-small` model, which costs:
- $0.00002 per 1K tokens for embeddings
- Typical usage for personal documents:
  - Initial processing: ~$0.01-0.05 per document
  - Queries: ~$0.0001-0.001 per query
- $10 monthly credit should be more than sufficient for personal use

## Configuration

The system is configured through `config/config.json`. You can modify:
- OpenAI API key
- Embedding model
- Vector store location
- Documents directory

## Project Structure

```
.
├── config/
│   └── config.json
├── data/
│   ├── documents/     # Place your PDFs here
│   └── vector_store/  # Vector store database
├── src/
│   ├── cli.py
│   ├── document_processor.py
│   ├── embeddings.py
│   └── query.py
└── requirements.txt
```
