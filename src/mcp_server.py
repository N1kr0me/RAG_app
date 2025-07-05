import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from .query import QueryEngine
from .document_processor import DocumentProcessor
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Chatbot Server", version="2.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
query_engine = QueryEngine()
document_processor = DocumentProcessor()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

def initialize_documents():
    """Process documents on startup"""
    try:
        logger.info("Starting automatic document processing on startup...")
        chunks = document_processor.process_directory(document_processor.documents_path)
        if chunks:
            from .embeddings import create_vector_store, load_config
            config = load_config()
            create_vector_store(chunks, config["vector_store"]["path"])
            logger.info(f"✅ Successfully processed {len(chunks)} chunks on startup")
        else:
            logger.warning("⚠️ No documents found to process on startup")
    except Exception as e:
        logger.error(f"❌ Document processing failed on startup: {e}")
        # Don't fail the entire service startup, just log the error

# Process documents when the service starts
@app.on_event("startup")
async def startup_event():
    """Run on service startup"""
    logger.info("🚀 RAG Chatbot Server starting up...")
    initialize_documents()
    logger.info("✅ RAG Chatbot Server ready!")

class QueryRequest(BaseModel):
    query: str
    chat_history: Optional[List[dict]] = None

class ProcessRequest(BaseModel):
    reset: bool = False

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "rag-chatbot-server"}

@app.get("/")
async def root():
    """Root endpoint with server information"""
    return {
        "message": "RAG Chatbot Server is running",
        "version": "2.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/query",
            "process": "/process"
        }
    }

@app.post("/query")
async def query(request: QueryRequest):
    """Query the RAG system with context from documents using OpenAI API"""
    try:
        logger.info(f"Processing query: {request.query[:50]}...")
        results = query_engine.query(request.query)
        logger.info(f"Found {len(results)} relevant document chunks")
        context = "\n\n".join([r["content"] for r in results])

        # Prepare messages for OpenAI with butler personality
        messages = []
        
        # Add chat history (last 5 exchanges for context)
        if request.chat_history:
            # Keep only the last 10 messages (5 exchanges)
            recent_history = request.chat_history[-10:] if len(request.chat_history) > 10 else request.chat_history
            messages.extend(recent_history)
        
        # Butler personality system prompt
        system_prompt = """You are a distinguished butler serving as Nikhil's personal assistant. You embody the following characteristics:

- **Respectful and Professional**: Always address users with courtesy and maintain a formal, yet warm tone
- **Precise and Concise**: Provide direct, accurate answers to questions asked
- **Context-Aware**: Remember previous conversation context and build upon it naturally
- **Character Consistency**: Never break character - always respond as a professional butler
- **Knowledgeable**: Draw from the provided context about Nikhil's background, skills, and experience
- **Expansive When Asked**: Only elaborate or provide additional details when specifically requested

When responding:
- Be direct and to the point initially
- Use respectful language ("sir", "madam", or simply polite phrasing)
- If asked to expand, provide comprehensive details
- Always maintain the butler's professional demeanor
- Reference specific information from the context when available

Context about Nikhil:"""

        messages.append({
            "role": "system",
            "content": f"{system_prompt}\n\n{context}"
        })
        messages.append({
            "role": "user",
            "content": request.query
        })

        # Call OpenAI using new API
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.3,  # Slightly higher for personality
            max_tokens=512
        )
        answer = response.choices[0].message.content
        logger.info("Successfully generated response from OpenAI")
        return {
            "answer": answer,
            "sources": results,
            "query": request.query,
            "context_length": len(context)
        }
    except Exception as e:
        logger.error(f"Query processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process")
async def process_documents(request: ProcessRequest):
    """Process documents in the data/documents directory"""
    try:
        logger.info("Starting document processing...")
        chunks = document_processor.process_directory(document_processor.documents_path)
        if not chunks:
            logger.warning("No documents found or processed")
            return {"message": "No documents found or processed", "chunks": 0}
        from .embeddings import create_vector_store, load_config
        config = load_config()
        create_vector_store(chunks, config["vector_store"]["path"])
        logger.info(f"Successfully processed {len(chunks)} chunks")
        return {
            "message": f"Successfully processed {len(chunks)} chunks",
            "chunks": len(chunks)
        }
    except Exception as e:
        logger.error(f"Document processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting RAG Chatbot Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000) 