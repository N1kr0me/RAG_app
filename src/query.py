from pathlib import Path
from typing import List
from langchain.vectorstores.chroma import Chroma
from langchain.schema.document import Document
from .embeddings import get_embedding_function, load_config

class RAGQuery:
    def __init__(self):
        self.config = load_config()
        self.vector_store_path = Path(self.config["vector_store"]["path"])
        self.db = Chroma(
            persist_directory=str(self.vector_store_path),
            embedding_function=get_embedding_function()
        )
        
    def query(self, query_text: str, k: int = 4) -> List[Document]:
        """
        Query the vector store for relevant documents.
        
        Args:
            query_text: The query text
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        if not self.vector_store_path.exists():
            raise FileNotFoundError("Vector store not found. Please process documents first.")
            
        return self.db.similarity_search(query_text, k=k)
    
    def get_relevant_context(self, query_text: str, k: int = 4) -> str:
        """
        Get relevant context from documents for a query.
        
        Args:
            query_text: The query text
            k: Number of documents to retrieve
            
        Returns:
            Combined context from relevant documents
        """
        docs = self.query(query_text, k=k)
        return "\n\n".join(doc.page_content for doc in docs) 