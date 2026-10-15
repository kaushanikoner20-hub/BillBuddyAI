import io

import pytest
from fastapi.testclient import TestClient
from PIL import Image

import config
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def temp_upload_dir(tmp_path, monkeypatch):
    """Save test uploads in a temporary folder, never in the real uploads folder."""
    monkeypatch.setattr(config, "UPLOAD_DIR", tmp_path)
    return tmp_path


def make_image_bytes(image_format):
    buffer = io.BytesIO()
    Image.new("RGB", (10, 10), "white").save(buffer, format=image_format)
    return buffer.getvalue()


def upload(filename, data):
    return client.post("/api/receipts/upload", files={"file": (filename, data)})


def test_upload_png(temp_upload_dir):
    response = upload("receipt.png", make_image_bytes("PNG"))
    assert response.status_code == 201
    body = response.json()
    assert body["file_type"] == "png"
    assert (temp_upload_dir / f"{body['id']}.png").exists()


def test_upload_jpeg():
    response = upload("receipt.jpeg", make_image_bytes("JPEG"))
    assert response.status_code == 201
    assert response.json()["file_type"] == "jpeg"


def test_upload_pdf():
    response = upload("invoice.pdf", b"%PDF-1.4\n%%EOF")
    assert response.status_code == 201
    assert response.json()["file_type"] == "pdf"


def test_rejects_wrong_extension():
    response = upload("notes.txt", b"hello")
    assert response.status_code == 400


def test_rejects_fake_image():
    response = upload("fake.png", b"this is plain text, not a PNG")
    assert response.status_code == 400


def test_rejects_extension_that_does_not_match_contents():
    response = upload("receipt.jpg", make_image_bytes("PNG"))
    assert response.status_code == 400


def test_rejects_empty_file():
    response = upload("empty.png", b"")
    assert response.status_code == 400


def test_rejects_file_that_is_too_large(monkeypatch):
    monkeypatch.setattr(config, "MAX_UPLOAD_BYTES", 100)
    response = upload("big.png", make_image_bytes("PNG") + b"0" * 200)
    assert response.status_code == 413


def test_unsafe_file_name_is_not_used_for_saving(temp_upload_dir):
    response = upload("../../evil.png", make_image_bytes("PNG"))
    assert response.status_code == 201
    assert response.json()["original_filename"] == "evil.png"
    saved_files = list(temp_upload_dir.iterdir())
    assert len(saved_files) == 1
    assert saved_files[0].name != "evil.png"