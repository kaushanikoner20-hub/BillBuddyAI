# Architecture

## Current (Stage 3)

```
Browser (React + Vite, localhost:5173)
   |  GET  /api/health
   |  POST /api/receipts/ocr      (multipart form, field name "file")
   v
FastAPI backend (127.0.0.1:8000)
   -> services/file_validation.py  (extension, size, real file contents)
   -> services/ocr_service.py      (Pillow / PyMuPDF -> Tesseract)
   <- JSON: success, filename, extracted_text, page_count, message
```

The OCR endpoint works in memory and **does not save the receipt**. pytesseract briefly writes a temporary image to the system temp folder and deletes it right after reading it.

The older `POST /api/receipts/upload` endpoint (Stage 2) still exists and saves files to `backend/uploads/` (ignored by Git). The web page no longer uses it.

### How OCR works

- **Images (JPG, JPEG, PNG):** fix rotation, flatten transparency, then run Tesseract.
- **PDFs:** render each page to an image at 200 dpi (lower for very large pages), then run Tesseract. At most 5 pages are read, so scanned PDFs work too.
- Tesseract is looked up on each request: first `TESSERACT_CMD`, then `C:\Program Files\Tesseract-OCR\tesseract.exe`, then the PATH. If it is missing, the API answers `503` with install steps, and the server still runs.

### Rules and responses

- Allowed types: JPG, JPEG, PNG, PDF. The extension must match the file's real contents.
- Size limit: `MAX_UPLOAD_MB` (default 10), enforced by the backend.
- `200` text read (may be empty), `400` wrong type, empty, or fake file, `413` too large, `422` unreadable file, `503` Tesseract missing, `500` unexpected error (no details shown).

## Planned flow (not built yet)

```
OCR text (done) -> Gemma via Ollama -> Review -> SQLite
```

## Backend layout

- `main.py`: creates the FastAPI app and routes
- `config.py`: reads settings from environment variables
- `services/`: file validation, OCR, and storage now; Ollama code later
- `models/`: data shapes (added when needed)
- `database/`: SQLite code (added when needed)
- `tests/`: pytest tests