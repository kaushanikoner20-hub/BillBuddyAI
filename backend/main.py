"""BillBuddy AI backend.

Run from the backend folder with:
    uvicorn main:app --reload --port 8000
"""

import logging
from pathlib import PurePath

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware

import config
from services.file_validation import FileValidationError, validate_upload
from services.ocr_service import OcrError, TesseractNotFoundError, extract_text
from services.storage import save_receipt

logger = logging.getLogger("billbuddy")

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
        "message": "Receipt uploaded.",
    }


@app.post("/api/receipts/ocr")
async def ocr_receipt(file: UploadFile = File(...)):
    """Read the text from one receipt. The file is NOT saved."""
    data = await file.read(config.MAX_UPLOAD_BYTES + 1)

    try:
        kind = validate_upload(file.filename, data, config.MAX_UPLOAD_BYTES)
    except FileValidationError as error:
        raise HTTPException(status_code=error.status_code, detail=str(error))

    try:
        # OCR is slow, so run it in a worker thread and keep the server responsive.
        result = await run_in_threadpool(extract_text, data, kind)
    except TesseractNotFoundError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except OcrError as error:
        raise HTTPException(status_code=422, detail=str(error))
    except Exception as error:
        # Log only the error type, never the receipt or file paths.
        logger.error("Unexpected OCR failure: %s", type(error).__name__)
        raise HTTPException(
            status_code=500, detail="Something went wrong while reading the document."
        )

    text = result["text"]
    message = "Text extracted successfully."
    if not text:
        message = "No text was detected. Try a clearer or higher-resolution image."
    if result["total_pages"] > result["page_count"]:
        message += (
            f" Only the first {result['page_count']} of "
            f"{result['total_pages']} pages were read."
        )

    return {
        "success": True,
        "filename": PurePath(file.filename).name,
        "extracted_text": text,
        "page_count": result["page_count"],
        "message": message,
    }