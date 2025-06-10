from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from typing import List, Optional
from .query import QueryEngine
from .document_processor import DocumentProcessor

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
query_engine = QueryEngine()
document_processor = DocumentProcessor()

class QueryRequest(BaseModel):
    query: str
    chat_history: Optional[List[dict]] = None

class ProcessRequest(BaseModel):
    reset: bool = False

@app.post("/query")
async def query(request: QueryRequest):
    try:
        # Get relevant documents
        results = query_engine.query(request.query)
        
        # Prepare context for Ollama
        context = "\n\n".join([r["content"] for r in results])
        
        # Prepare messages for Ollama
        messages = []
        if request.chat_history:
            messages.extend(request.chat_history)
        
        messages.append({
            "role": "system",
            "content": f"Use the following context to answer the question. If you cannot find the answer in the context, say so.\n\nContext:\n{context}"
        })
        messages.append({
            "role": "user",
            "content": request.query
        })
        
        # Call Ollama API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://{os.getenv('OLLAMA_HOST', 'localhost')}:{os.getenv('OLLAMA_PORT', '11434')}/api/chat",
                json={
                    "model": "phi:2.7b",
                    "messages": messages,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Error calling Ollama API")
            
            ollama_response = response.json()
            
        return {
            "answer": ollama_response["message"]["content"],
            "sources": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process")
async def process_documents(request: ProcessRequest):
    try:
        # Process documents
        chunks = document_processor.process_directory()
        
        if not chunks:
            return {"message": "No documents found or processed"}
        
        # Create vector store
        from .embeddings import create_vector_store, load_config
        config = load_config()
        create_vector_store(chunks, config["vector_store"]["path"])
        
        return {
            "message": f"Successfully processed {len(chunks)} chunks",
            "chunks": len(chunks)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 