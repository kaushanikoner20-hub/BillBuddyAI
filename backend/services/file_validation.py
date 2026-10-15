"""Checks that an uploaded file really is a JPG, PNG, or PDF.

We do not trust the file name alone. We also look at the first bytes of the
file (its "magic bytes"), because those show what the file really is.
"""

from pathlib import Path

# File extension -> file kind
ALLOWED_EXTENSIONS = {
    ".jpg": "jpeg",
    ".jpeg": "jpeg",
    ".png": "png",
    ".pdf": "pdf",
}

# File kind -> the bytes every file of that kind starts with
SIGNATURES = {
    "jpeg": b"\xff\xd8\xff",
    "png": b"\x89PNG\r\n\x1a\n",
    "pdf": b"%PDF-",
}


class FileValidationError(Exception):
    """Raised when an uploaded file is not acceptable."""

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code


def validate_upload(filename, data, max_bytes):
    """Return the file kind ("jpeg", "png" or "pdf") or raise FileValidationError."""
    extension = Path(filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise FileValidationError("Only JPG, JPEG, PNG, and PDF files are allowed.")

    if len(data) == 0:
        raise FileValidationError("The file is empty.")

    if len(data) > max_bytes:
        max_mb = max_bytes // (1024 * 1024)
        raise FileValidationError(
            f"The file is too large. The limit is {max_mb} MB.", status_code=413
        )

    expected_kind = ALLOWED_EXTENSIONS[extension]
    if not data.startswith(SIGNATURES[expected_kind]):
        raise FileValidationError(
            "The file contents do not match its extension. "
            "It may be damaged or not a real receipt file."
        )

    return expected_kind