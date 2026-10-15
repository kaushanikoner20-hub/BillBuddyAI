# AI Model Notes

This document explains how BillBuddy AI **plans** to use AI. None of this is implemented in Stage 1.

## Planned pipeline

1. **Tesseract OCR** reads text from a receipt image (or from PDF pages rendered to images by PyMuPDF).
2. **Gemma**, running locally through **Ollama**, receives that text and returns structured fields such as vendor, date, total, tax, currency, and category.
3. The user **reviews and corrects** the fields before anything is saved.

## Why local inference

- Receipts and invoices contain private financial details.
- Running the model on your own computer means document text is not sent to a cloud AI service.
- No API keys or paid services are required.

## Configuration

Settings live in `backend/.env` (copy from `backend/.env.example`):

- `OLLAMA_BASE_URL`: where Ollama listens (default `http://localhost:11434`)
- `OLLAMA_MODEL`: the Gemma model tag (default `gemma3:4b`)

Newer Gemma versions may exist in the Ollama library. Check https://ollama.com/library and change `OLLAMA_MODEL` if you prefer another size or version.

## Current limitations

- Stage 1 contains no OCR or AI code.
- OCR can misread blurry, rotated, or low-contrast receipts.
- Language models can make mistakes or invent values. Extracted fields must always be reviewed by a person.
- Small local models are less accurate than large cloud models and need enough RAM to run.
- Handwritten receipts are not a goal for the first versions.
