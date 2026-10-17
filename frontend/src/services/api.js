// All calls to the backend live in this folder, so pages stay simple.
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function getHealth() {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  if (!response.ok) {
    throw new Error(`Backend answered with status ${response.status}`);
  }
  return response.json();
}

// Sends one receipt to the backend and returns the OCR result.
export async function extractReceiptText(file) {
  const formData = new FormData();
  formData.append("file", file);

  let response;
  try {
    // Do not set Content-Type here: the browser adds it, including the boundary.
    response = await fetch(`${API_BASE_URL}/api/receipts/ocr`, {
      method: "POST",
      body: formData,
    });
  } catch {
    throw new Error(
      `Could not reach the backend at ${API_BASE_URL}. Is it running?`
    );
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = data && typeof data.detail === "string" ? data.detail : "";
    throw new Error(
      detail || `The server could not process the file (status ${response.status}).`
    );
  }

  if (!data || typeof data.extracted_text !== "string") {
    throw new Error("The server sent a response the app could not understand.");
  }
  return data;
}