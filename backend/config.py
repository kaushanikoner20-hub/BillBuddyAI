"""Central place for backend settings.

Values come from environment variables or a local backend/.env file.
If nothing is set, the safe defaults below are used.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load backend/.env if it exists (it is ignored by Git).
load_dotenv(Path(__file__).parent / ".env")

APP_NAME = "BillBuddy AI"
APP_VERSION = "0.1.0"

# Ollama settings (used from Stage 4).
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")

# Optional path to tesseract.exe (used from Stage 3).
TESSERACT_CMD = os.getenv("TESSERACT_CMD", "")

# Which frontend addresses may call this backend.
_default_origins = "http://localhost:5173,http://127.0.0.1:5173"
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", _default_origins).split(",")
    if origin.strip()
]
