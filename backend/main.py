"""BillBuddy AI backend.

Run from the backend folder with:
    uvicorn main:app --reload --port 8000
"""

from pathlib import PurePath

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import config
from services.file_validation import FileValidationError, validate_upload
from services.storage import save_receipt

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


@app.post("/api/receipts/upload", status_code=201)
async def upload_receipt(file: UploadFile = File(...)):
    """Accept one receipt (JPG, JPEG, PNG or PDF), check it, and save it."""
    # Read at most one byte more than the limit, so huge files cannot fill memory.
    data = await file.read(config.MAX_UPLOAD_BYTES + 1)

    try:
        kind = validate_upload(file.filename, data, config.MAX_UPLOAD_BYTES)
    except FileValidationError as error:
        raise HTTPException(status_code=error.status_code, detail=str(error))

    saved = save_receipt(data, kind)

    return {
        "id": saved["id"],
        "original_filename": PurePath(file.filename).name,
        "file_type": kind,
        "size_bytes": len(data),
        "message": "Receipt uploaded. Text extraction is not built yet.",
    }