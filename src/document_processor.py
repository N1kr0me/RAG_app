import json
from pathlib import Path
from typing import List
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.vectorstores.chroma import Chroma
from .embeddings import get_embedding_function, load_config

class DocumentProcessor:
    def __init__(self):
        self.config = load_config()
        self.documents_path = Path(self.config["documents"]["path"])
        self.vector_store_path = Path(self.config["vector_store"]["path"])
        
    def load_documents(self) -> List[Document]:
        """Load documents from the configured documents directory."""
        if not self.documents_path.exists():
            raise FileNotFoundError(f"Documents directory not found: {self.documents_path}")
            
        document_loader = PyPDFDirectoryLoader(str(self.documents_path))
        return document_loader.load()
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        return text_splitter.split_documents(documents)
    
    def process_documents(self, reset: bool = False):
        """Process documents and add them to the vector store."""
        if reset and self.vector_store_path.exists():
            import shutil
            shutil.rmtree(self.vector_store_path)
            
        documents = self.load_documents()
        chunks = self.split_documents(documents)
        self._add_to_vector_store(chunks)
        
    def _add_to_vector_store(self, chunks: List[Document]):
        """Add document chunks to the vector store."""
        db = Chroma(
            persist_directory=str(self.vector_store_path),
            embedding_function=get_embedding_function()
        )
        
        chunks_with_ids = self._calculate_chunk_ids(chunks)
        
        existing_items = db.get(include=[])
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")
        
        new_chunks = [
            chunk for chunk in chunks_with_ids
            if chunk.metadata["id"] not in existing_ids
        ]
        
        if new_chunks:
            print(f"👉 Adding new documents: {len(new_chunks)}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
            db.persist()
        else:
            print("✅ No new documents to add")
            
    def _calculate_chunk_ids(self, chunks: List[Document]) -> List[Document]:
        """Calculate unique IDs for document chunks."""
        last_page_id = None
        current_chunk_index = 0
        
        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"
            
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0
                
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id
            
            chunk.metadata["id"] = chunk_id
            
        return chunks 