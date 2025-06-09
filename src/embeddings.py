import json
import os
from pathlib import Path
from langchain_community.embeddings.openai import OpenAIEmbeddings

def load_config():
    config_path = Path(__file__).parent.parent / "config" / "config.json"
    with open(config_path) as f:
        return json.load(f)

def get_embedding_function():
    """Get the OpenAI embedding function."""
    config = load_config()
    api_key = os.getenv("OPENAI_API_KEY") or config["embedding"]["api_key"]
    
    return OpenAIEmbeddings(
        model=config["embedding"]["model"],
        openai_api_key=api_key
    ) 