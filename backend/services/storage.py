"""Saves uploaded receipts to disk."""

import uuid

import config

FILE_EXTENSIONS = {"jpeg": ".jpg", "png": ".png", "pdf": ".pdf"}


def save_receipt(data, kind):
    """Save the file under a random name and return its id and stored name.

    We never use the name the user sent as a path. That keeps tricks like
    "../../something.png" from writing files outside the uploads folder.
    """
    upload_dir = config.UPLOAD_DIR
    upload_dir.mkdir(parents=True, exist_ok=True)

    receipt_id = uuid.uuid4().hex
    stored_name = receipt_id + FILE_EXTENSIONS[kind]
    (upload_dir / stored_name).write_bytes(data)

    return {"id": receipt_id, "stored_name": stored_name}