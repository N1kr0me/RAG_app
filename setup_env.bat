@echo off
echo Setting up RAG System environment...

REM Add Docker and Ollama to PATH
setx PATH "%PATH%;D:\Program\Docker;D:\Program\Ollama"

REM Set Ollama models directory
setx OLLAMA_MODELS "D:\Program\Ollama\models"

echo Environment variables set. Please restart your terminal to apply changes.
pause 