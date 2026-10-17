"""Reads text from receipt images and PDFs with Tesseract OCR.

The uploaded file is handled in memory. (pytesseract briefly writes a temporary
copy of each image to the system temp folder and deletes it right after.)
"""

import io
from pathlib import Path

import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageOps

import config

MAX_PDF_PAGES = 5
PDF_RENDER_DPI = 200  # Sharp enough for OCR without using too much memory.
MAX_IMAGE_PIXELS = 40_000_000
OCR_TIMEOUT_SECONDS = 60
DEFAULT_WINDOWS_TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")

TESSERACT_MISSING_MESSAGE = (
    "Tesseract OCR was not found. Install it from "
    "https://github.com/UB-Mannheim/tesseract/wiki and restart the backend. "
    "If it is installed in a custom folder, set TESSERACT_CMD in backend/.env "
    "to the full path of tesseract.exe."
)


class OcrError(Exception):
    """The document could not be read. The message is safe to show to the user."""


class TesseractNotFoundError(OcrError):
    """Tesseract is not installed or not configured."""


def _configure_tesseract():
    """Point pytesseract at tesseract.exe (checked on each run, not at startup)."""
    if config.TESSERACT_CMD:
        pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD
    elif DEFAULT_WINDOWS_TESSERACT.exists():
        pytesseract.pytesseract.tesseract_cmd = str(DEFAULT_WINDOWS_TESSERACT)


def run_tesseract(image):
    """Run Tesseract on one Pillow image and return the raw text."""
    _configure_tesseract()
    try:
        return pytesseract.image_to_string(image, timeout=OCR_TIMEOUT_SECONDS)
    except pytesseract.TesseractNotFoundError:
        raise TesseractNotFoundError(TESSERACT_MISSING_MESSAGE) from None
    except (pytesseract.TesseractError, RuntimeError, OSError):
        raise OcrError(
            "Tesseract could not read this document. Try a clearer image."
        ) from None


def _prepare_image(image):
    """Fix rotation and transparency so Tesseract gets a plain RGB image."""
    image = ImageOps.exif_transpose(image)
    if image.mode in ("RGBA", "LA") or "transparency" in image.info:
        rgba = image.convert("RGBA")
        background = Image.new("RGB", rgba.size, "white")
        background.paste(rgba, mask=rgba.split()[3])
        return background
    return image.convert("RGB")


def extract_text_from_image(data):
    """OCR a JPG or PNG given as bytes. Returns the text."""
    try:
        with Image.open(io.BytesIO(data)) as image:
            if image.width * image.height > MAX_IMAGE_PIXELS:
                raise OcrError("The image is too large. Please use a smaller image.")
            prepared = _prepare_image(image)
        with prepared:
            return run_tesseract(prepared).strip()
    except OcrError:
        raise
    except (OSError, ValueError, SyntaxError, Image.DecompressionBombError):
        raise OcrError(
            "The file could not be read as an image. It may be damaged."
        ) from None


def _choose_dpi(page):
    """Use 200 dpi, but go lower for pages that would be huge at that size."""
    width_in = page.rect.width / 72
    height_in = page.rect.height / 72
    pixels = (width_in * PDF_RENDER_DPI) * (height_in * PDF_RENDER_DPI)
    if pixels <= MAX_IMAGE_PIXELS:
        return PDF_RENDER_DPI
    return max(50, int(PDF_RENDER_DPI * (MAX_IMAGE_PIXELS / pixels) ** 0.5))


def _ocr_pdf_page(page):
    """Render one PDF page to an image and OCR it."""
    try:
        pixmap = page.get_pixmap(dpi=_choose_dpi(page))
        image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
    except Exception:
        raise OcrError("A page of this PDF could not be rendered.") from None
    with image:
        return run_tesseract(image).strip()


def extract_text_from_pdf(data):
    """OCR up to MAX_PDF_PAGES pages of a PDF given as bytes."""
    try:
        document = fitz.open(stream=data, filetype="pdf")
    except Exception:
        raise OcrError("This PDF could not be opened. It may be damaged.") from None

    try:
        if document.needs_pass:
            raise OcrError(
                "This PDF is password protected. Remove the password and try again."
            )
        total_pages = document.page_count
        if total_pages == 0:
            raise OcrError("This PDF has no pages.")

        pages_to_read = min(total_pages, MAX_PDF_PAGES)
        page_texts = [_ocr_pdf_page(document[number]) for number in range(pages_to_read)]
    finally:
        document.close()

    return {
        "text": "\n\n".join(text for text in page_texts if text),
        "page_count": pages_to_read,
        "total_pages": total_pages,
    }


def extract_text(data, kind):
    """OCR a receipt. kind is "jpeg", "png" or "pdf".

    Returns {"text": ..., "page_count": pages read, "total_pages": pages in file}.
    """
    if kind == "pdf":
        return extract_text_from_pdf(data)
    return {
        "text": extract_text_from_image(data),
        "page_count": 1,
        "total_pages": 1,
    }