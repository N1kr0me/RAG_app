from typing import List, Dict, Any
from pathlib import Path
from .embeddings import load_vector_store, load_config

class QueryEngine:
    def __init__(self):
        self.config = load_config()
        self.vector_store = load_vector_store(
            persist_directory=self.config["vector_store"]["path"]
        )

    def query(self, query_text: str, k: int = 4) -> List[Dict[str, Any]]:
        """
        Query the vector store for relevant documents.
        
        Args:
            query_text: The query text
            k: Number of results to return
            
        Returns:
            List of dictionaries containing document chunks and their metadata
        """
        results = self.vector_store.similarity_search_with_score(
            query_text,
            k=k
        )
        
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            })
            
        return formatted_results

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
        return "\n\n".join(doc["content"] for doc in docs) 