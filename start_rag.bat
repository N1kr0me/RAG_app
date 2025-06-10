@echo off
echo Starting RAG System...

REM Set Ollama path
set PATH=%PATH%;D:\Program\ollama

REM Start Ollama service
start "Ollama Service" D:\Program\ollama\ollama.exe serve

REM Wait for Ollama to start
timeout /t 5

REM Pull the model if not already pulled
D:\Program\ollama\ollama.exe pull phi:2.7b

REM Start the MCP server
python -m src.mcp_server

pause 