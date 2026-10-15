"""BillBuddy AI backend (Stage 1: foundation only).

Run from the backend folder with:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config

app = FastAPI(title=config.APP_NAME, version=config.APP_VERSION)

# Allow the Vite development server to call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    """Tell the caller that the backend is running."""
    return {
        "status": "ok",
        "app": config.APP_NAME,
        "version": config.APP_VERSION,
    }
