import argparse
from .document_processor import DocumentProcessor
from .query import RAGQuery

def main():
    parser = argparse.ArgumentParser(description="RAG System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Process documents command
    process_parser = subparsers.add_parser("process", help="Process documents")
    process_parser.add_argument("--reset", action="store_true", help="Reset the vector store")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query the RAG system")
    query_parser.add_argument("text", help="Query text")
    query_parser.add_argument("--k", type=int, default=4, help="Number of documents to retrieve")
    
    args = parser.parse_args()
    
    if args.command == "process":
        processor = DocumentProcessor()
        processor.process_documents(reset=args.reset)
    elif args.command == "query":
        rag = RAGQuery()
        try:
            context = rag.get_relevant_context(args.text, k=args.k)
            print("\nRelevant context:")
            print("-" * 80)
            print(context)
            print("-" * 80)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print("Please process documents first using: python -m src.cli process")
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 