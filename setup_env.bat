@echo off
REM Setup environment variables for RAG Chatbot (OpenAI API)

REM Set your OpenAI API key here
set OPENAI_API_KEY=sk-...

REM Optionally set the model (default is gpt-3.5-turbo)
REM set OPENAI_MODEL=gpt-3.5-turbo

echo Environment variables set for OpenAI API.

REM Create and activate virtual environment
python -m venv venv
call .\venv\Scripts\activate

REM Install dependencies
pip install -e .

REM Add Docker and Ollama to PATH
setx PATH "%PATH%;D:\Program\Docker;D:\Program\Ollama"

REM Set Ollama models directory
setx OLLAMA_MODELS "D:\Program\Ollama\models"

echo Environment setup complete. Please restart your terminal to apply changes.
pause 