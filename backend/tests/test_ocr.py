import io

import fitz  # PyMuPDF
import pytest
import pytesseract
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw, ImageFont

import config
import main
from services import ocr_service
from services.ocr_service import OcrError, TesseractNotFoundError

client = TestClient(main.app)


def tesseract_available():
    ocr_service._configure_tesseract()
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False


requires_tesseract = pytest.mark.skipif(
    not tesseract_available(), reason="Tesseract is not installed"
)


@pytest.fixture(autouse=True)
def temp_upload_dir(tmp_path, monkeypatch):
    """Use a temporary uploads folder so we can prove OCR saves nothing."""
    monkeypatch.setattr(config, "UPLOAD_DIR", tmp_path)
    return tmp_path


def png_bytes():
    buffer = io.BytesIO()
    Image.new("RGB", (10, 10), "white").save(buffer, format="PNG")
    return buffer.getvalue()


def post_ocr(filename, data):
    return client.post("/api/receipts/ocr", files={"file": (filename, data)})


def fake_ocr(text="TOTAL 12.50", page_count=1, total_pages=1):
    def _fake(data, kind):
        return {"text": text, "page_count": page_count, "total_pages": total_pages}

    return _fake


def raise_error(error):
    def _raise(data, kind):
        raise error

    return _raise


# ---------- endpoint tests (Tesseract is replaced by a stand-in) ----------


def test_ocr_rejects_unsupported_extension():
    assert post_ocr("notes.txt", b"hello").status_code == 400


def test_ocr_rejects_empty_file():
    assert post_ocr("empty.png", b"").status_code == 400


def test_ocr_rejects_oversized_file(monkeypatch):
    monkeypatch.setattr(config, "MAX_UPLOAD_BYTES", 100)
    assert post_ocr("big.png", png_bytes() + b"0" * 200).status_code == 413


def test_ocr_rejects_fake_image_before_running_ocr(monkeypatch):
    monkeypatch.setattr(main, "extract_text", raise_error(AssertionError("must not run")))
    assert post_ocr("fake.png", b"plain text pretending to be a PNG").status_code == 400


def test_ocr_success_for_png(monkeypatch):
    monkeypatch.setattr(main, "extract_text", fake_ocr("TOTAL 12.50"))
    response = post_ocr("receipt.png", png_bytes())
    body = response.json()
    assert response.status_code == 200
    assert body["success"] is True
    assert body["filename"] == "receipt.png"
    assert body["extracted_text"] == "TOTAL 12.50"
    assert body["page_count"] == 1


def test_ocr_reports_when_pdf_pages_were_skipped(monkeypatch):
    monkeypatch.setattr(main, "extract_text", fake_ocr("text", page_count=5, total_pages=8))
    response = post_ocr("invoice.pdf", b"%PDF-1.4\n%%EOF")
    assert response.status_code == 200
    assert "first 5 of 8" in response.json()["message"]


def test_ocr_reports_empty_result(monkeypatch):
    monkeypatch.setattr(main, "extract_text", fake_ocr(""))
    response = post_ocr("blank.png", png_bytes())
    assert response.status_code == 200
    assert "No text was detected" in response.json()["message"]


def test_ocr_missing_tesseract_gives_clear_error(monkeypatch):
    monkeypatch.setattr(
        main, "extract_text", raise_error(TesseractNotFoundError(ocr_service.TESSERACT_MISSING_MESSAGE))
    )
    response = post_ocr("receipt.png", png_bytes())
    assert response.status_code == 503
    assert "TESSERACT_CMD" in response.json()["detail"]


def test_ocr_failure_returns_understandable_error(monkeypatch):
    monkeypatch.setattr(main, "extract_text", raise_error(OcrError("This PDF has no pages.")))
    response = post_ocr("receipt.png", png_bytes())
    assert response.status_code == 422
    assert response.json()["detail"] == "This PDF has no pages."


def test_unexpected_error_does_not_leak_details(monkeypatch):
    monkeypatch.setattr(main, "extract_text", raise_error(RuntimeError(r"C:\secret\path.txt")))
    response = post_ocr("receipt.png", png_bytes())
    assert response.status_code == 500
    assert "secret" not in response.text


def test_ocr_does_not_save_the_receipt(monkeypatch, temp_upload_dir):
    monkeypatch.setattr(main, "extract_text", fake_ocr())
    post_ocr("receipt.png", png_bytes())
    assert list(temp_upload_dir.iterdir()) == []


def test_corrupt_image_with_valid_signature_is_rejected():
    response = post_ocr("broken.png", b"\x89PNG\r\n\x1a\n" + b"garbage")
    assert response.status_code == 422


def test_corrupt_pdf_with_valid_signature_is_rejected():
    response = post_ocr("broken.pdf", b"%PDF-1.4 garbage, not a real pdf")
    assert response.status_code == 422


# ---------- OCR service tests ----------


def make_pdf(page_texts):
    document = fitz.open()
    for text in page_texts:
        page = document.new_page()
        page.insert_text((72, 100), text, fontsize=36)
    data = document.tobytes()
    document.close()
    return data


def test_missing_tesseract_is_reported(monkeypatch):
    def not_found(*args, **kwargs):
        raise pytesseract.TesseractNotFoundError()

    monkeypatch.setattr(pytesseract, "image_to_string", not_found)
    with pytest.raises(TesseractNotFoundError):
        ocr_service.run_tesseract(Image.new("RGB", (5, 5)))


def test_pdf_reading_stops_at_five_pages(monkeypatch):
    monkeypatch.setattr(ocr_service, "run_tesseract", lambda image: "page text")
    result = ocr_service.extract_text(make_pdf(["page"] * 7), "pdf")
    assert result["page_count"] == 5
    assert result["total_pages"] == 7


def test_service_rejects_unreadable_image():
    with pytest.raises(OcrError):
        ocr_service.extract_text(b"not an image", "png")


# ---------- real OCR tests (only run when Tesseract is installed) ----------


@requires_tesseract
def test_real_ocr_reads_an_image():
    image = Image.new("RGB", (700, 160), "white")
    font = ImageFont.load_default(size=56)
    ImageDraw.Draw(image).text((20, 40), "HELLO 123", fill="black", font=font)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    result = ocr_service.extract_text(buffer.getvalue(), "png")
    assert "HELLO" in result["text"].upper()


@requires_tesseract
def test_real_ocr_reads_a_pdf():
    result = ocr_service.extract_text(make_pdf(["INVOICE TOTAL"]), "pdf")
    assert "INVOICE" in result["text"].upper()