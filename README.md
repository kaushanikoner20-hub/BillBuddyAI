# BillBuddy AI

An open-source, **local-first** receipt and invoice organizer for freelancers and small businesses.
Upload a receipt, extract its text with OCR, and let an open-weight AI model turn it into structured expense data, all on your own computer.

> **Status: Stage 1 (project foundation).** The backend health check and a starter frontend exist.
> Everything under "Planned features" is **not built yet**. See [TODO.md](TODO.md).

## Planned features

- Upload JPG, JPEG, PNG, and PDF receipts
- Extract text with Tesseract OCR
- Organize the text into expense fields with Gemma running locally through Ollama
- Review and correct extracted fields
- Save expenses in SQLite
- Search, filter, edit, and delete expenses
- Expense summaries and CSV export

## Technology stack

| Part | Technology |
|------|------------|
| Frontend | React + Vite + JavaScript + CSS |
| Backend | Python + FastAPI |
| OCR | Tesseract with pytesseract and Pillow |
| PDF processing | PyMuPDF |
| AI | Gemma through Ollama (local) |
| Database | SQLite |
| Tests | pytest |

No paid APIs, API keys, or cloud AI services are needed.

## Prerequisites (Windows)

Needed now:
- [Python 3.11 or newer](https://www.python.org/downloads/) (tick "Add Python to PATH" in the installer)
- [Node.js LTS](https://nodejs.org/)
- [Git](https://git-scm.com/download/win)

Needed in later stages (not required to run Stage 1):
- [Tesseract OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
- [Ollama](https://ollama.com/download)

## Setup

Open two PowerShell terminals in the project folder.

**Terminal 1: backend**

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn main:app --reload --port 8000
```

If PowerShell blocks the activate script, run this once and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Terminal 2: frontend**

```powershell
cd frontend
npm install
npm run dev
```

## Check that it works

- Backend health: open http://127.0.0.1:8000/api/health. You should see `{"status":"ok", ...}`.
- API docs: http://127.0.0.1:8000/docs
- Frontend: open http://localhost:5173. You should see a green "Backend connected" message.

## Run the checks

```powershell
# Backend tests (venv active)
cd backend
python -m pytest

# Frontend build check
cd frontend
npm run build
```

## Project layout

```
backend/    FastAPI app (main.py), settings (config.py), tests/
frontend/   React + Vite app
docs/       Architecture notes
```

Folders such as `backend/services/`, `backend/models/`, and `backend/database/` are added when a stage needs them.

## Privacy

Receipts are sensitive. BillBuddy AI is designed to process them locally. See [SECURITY.md](SECURITY.md) and [AI_MODEL.md](AI_MODEL.md).

## License

Not chosen yet. MIT is recommended and is waiting for the maintainer's confirmation.
