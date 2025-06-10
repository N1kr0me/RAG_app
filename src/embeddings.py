import os
from pathlib import Path
import json
from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def load_config() -> Dict[str, Any]:
    """Load configuration from config.json."""
    config_path = Path("config/config.json")
    if not config_path.exists():
        raise FileNotFoundError("config.json not found. Please create it from config.template.json")
    
    with open(config_path) as f:
        return json.load(f)

def get_embedding_function():
    """Get OpenAI embedding function."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY not set. Using mock embeddings for development.")
        # Return a mock embedding function for development
        return MockEmbeddings()
    
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=api_key
    )

class MockEmbeddings:
    """Mock embeddings for development when API key is not available."""
    def __init__(self):
        self.dimension = 1536  # Same as text-embedding-3-small
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate mock embeddings for documents."""
        return [[0.0] * self.dimension for _ in texts]
        
    def embed_query(self, text: str) -> List[float]:
        """Generate mock embedding for a query."""
        return [0.0] * self.dimension

def create_vector_store(texts: List[str], persist_directory: str):
    """Create and persist a vector store from texts."""
    embedding_function = get_embedding_function()
    
    # Create and persist the vector store
    vector_store = Chroma.from_texts(
        texts=texts,
        embedding=embedding_function,
        persist_directory=persist_directory
    )
    
    vector_store.persist()
    return vector_store

def load_vector_store(persist_directory: str):
    """Load an existing vector store."""
    embedding_function = get_embedding_function()
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function
    ) 