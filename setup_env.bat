@echo off
echo Setting up RAG System environment...

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