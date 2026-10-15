# TODO

Checked items are done. Unchecked items are planned only.

## Stage 1: Foundation
- [x] Project structure and .gitignore
- [x] FastAPI backend with `GET /api/health` and CORS for Vite
- [x] React + Vite starter that calls the health endpoint
- [x] Configurable Ollama address and Gemma model name
- [x] Initial documentation and CI workflow file
- [x] Backend health tests written
- [x] Verify setup on your own machine (backend tests, frontend build, health check)
- [x] Confirm the license (MIT) and add LICENSE
- [x] Create the GitHub repository and make the first commit

## Stage 2: Upload and validation
- [ ] Upload endpoint for JPG, JPEG, PNG, PDF
- [ ] File type and size validation
- [ ] Frontend upload component

## Stage 3: OCR
- [ ] Image text extraction with Tesseract
- [ ] PDF page rendering with PyMuPDF, then OCR
- [ ] Clear errors when Tesseract is missing

## Stage 4: AI extraction
- [ ] Ollama client service
- [ ] Prompt and JSON schema for expense fields
- [ ] Validation of the model's output

## Stage 5: Review and save
- [ ] SQLite database and expense model
- [ ] Review and correction screen
- [ ] Save expenses

## Stage 6: Manage expenses
- [ ] List, search, and filter
- [ ] Edit and delete

## Stage 7: Summaries and export
- [ ] Expense summaries
- [ ] CSV export

## Stage 8: Polish and release
- [ ] Screenshots and demo guide
- [ ] Error handling and accessibility pass
- [ ] First tagged release


