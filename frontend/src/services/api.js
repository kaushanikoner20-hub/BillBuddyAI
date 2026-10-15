// All calls to the backend live in this folder, so pages stay simple.
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function getHealth() {
  const response = await fetch(`${API_URL}/api/health`);
  if (!response.ok) {
    throw new Error(`Backend answered with status ${response.status}`);
  }
  return response.json();
}

export async function uploadReceipt(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/api/receipts/upload`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || `Upload failed (status ${response.status})`);
  }
  return data;
}