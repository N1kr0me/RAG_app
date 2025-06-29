@echo off

echo Starting RAG Chatbot Server (OpenAI API)...
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.mcp.txt
)

echo.
echo Make sure you have set your OPENAI_API_KEY environment variable!
echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

REM Start the FastAPI server
python -m src.mcp_server 