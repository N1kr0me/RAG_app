import argparse
from pathlib import Path
from .document_processor import DocumentProcessor
from .embeddings import create_vector_store, load_config
from .query import QueryEngine

def process_documents():
    """Process documents and create vector store."""
    config = load_config()
    processor = DocumentProcessor()
    
    # Process documents
    documents_path = Path(config["documents"]["path"])
    if not documents_path.exists():
        print(f"Creating documents directory: {documents_path}")
        documents_path.mkdir(parents=True, exist_ok=True)
        print("Please add PDF files to the documents directory and run this command again.")
        return
    
    print("Processing documents...")
    chunks = processor.process_directory(documents_path)
    
    if not chunks:
        print("No documents found or processed. Please add PDF files to the documents directory.")
        return
    
    print(f"Created {len(chunks)} chunks from documents")
    
    # Create vector store
    vector_store_path = Path(config["vector_store"]["path"])
    vector_store_path.mkdir(parents=True, exist_ok=True)
    
    print("Creating vector store...")
    create_vector_store(chunks, str(vector_store_path))
    print("Vector store created successfully!")

def query_documents(query_text: str):
    """Query the vector store."""
    try:
        engine = QueryEngine()
        results = engine.query(query_text)
        
        print("\nRelevant documents found:")
        for i, result in enumerate(results, 1):
            print(f"\n--- Result {i} (Score: {result['score']:.4f}) ---")
            print(result["content"])
            print("---")
            
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("Please process documents first using: python -m src.cli process")

def main():
    parser = argparse.ArgumentParser(description="RAG System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Process command
    process_parser = subparsers.add_parser("process", help="Process documents")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query the system")
    query_parser.add_argument("text", help="Query text")
    
    args = parser.parse_args()
    
    if args.command == "process":
        process_documents()
    elif args.command == "query":
        query_documents(args.text)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 