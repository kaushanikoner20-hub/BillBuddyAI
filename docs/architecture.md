# Architecture

## Stage 1 (current)

```
Browser (React + Vite, localhost:5173)
        |  fetch  GET /api/health
        v
FastAPI backend (127.0.0.1:8000)
```

The frontend calls the backend through `frontend/src/services/api.js`. The backend allows the Vite address through CORS (`CORS_ORIGINS` in `backend/.env`).

## Planned flow (not built yet)

```
Upload -> OCR (Tesseract / PyMuPDF) -> Gemma via Ollama -> Review -> SQLite
```

## Backend layout

- `main.py`: creates the FastAPI app and routes
- `config.py`: reads settings from environment variables
- `services/`: OCR and Ollama code (added when needed)
- `models/`: data shapes (added when needed)
- `database/`: SQLite code (added when needed)
- `tests/`: pytest tests
