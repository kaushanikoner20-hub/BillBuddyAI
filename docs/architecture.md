# Architecture

## Current (Stage 2)

```
Browser (React + Vite, localhost:5173)
   |  GET  /api/health
   |  POST /api/receipts/upload   (multipart form, field name "file")
   v
FastAPI backend (127.0.0.1:8000)
   -> services/file_validation.py  (extension, size, real file contents)
   -> services/storage.py          (saves under a random name)
   -> backend/uploads/             (ignored by Git, holds private receipts)
```

The frontend calls the backend through `frontend/src/services/api.js`. The backend allows the Vite address through CORS (`CORS_ORIGINS` in `backend/.env`).

### Upload rules

- Allowed types: JPG, JPEG, PNG, PDF. The extension must match the file's real contents.
- Size limit: `MAX_UPLOAD_MB` (default 10).
- Files are saved as `<random id>.<ext>`. The name the user sent is never used as a path.
- Uploaded receipts are private financial data. Keep `UPLOAD_DIR` outside any cloud-synced folder if you can.

Responses: `201` saved, `400` wrong type, empty, or damaged file, `413` too large.

## Planned flow (not built yet)

```
Upload (done) -> OCR (Tesseract / PyMuPDF) -> Gemma via Ollama -> Review -> SQLite
```

## Backend layout

- `main.py`: creates the FastAPI app and routes
- `config.py`: reads settings from environment variables
- `services/`: file validation and storage now; OCR and Ollama code later
- `models/`: data shapes (added when needed)
- `database/`: SQLite code (added when needed)
- `tests/`: pytest tests