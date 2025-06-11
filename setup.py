from setuptools import setup, find_packages

setup(
    name="rag_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "python-multipart>=0.0.6",
        "requests>=2.31.0",
        "pydantic>=2.6.0",
        "langchain>=0.1.0",
        "langchain-community>=0.0.10",
        "langchain-text-splitters>=0.0.1",
        "chromadb>=0.4.22",
        "pypdf>=3.17.1",
        "openai>=1.12.0",
        "httpx>=0.26.0"
    ],
    python_requires=">=3.11",
) 