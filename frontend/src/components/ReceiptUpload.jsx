import { useState } from "react";
import { uploadReceipt } from "../services/api.js";

const ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".pdf"];
const MAX_SIZE_MB = 10; // The backend enforces the real limit.

// Returns an error message, or "" if the file looks fine.
function checkFile(file) {
  const name = file.name.toLowerCase();
  if (!ALLOWED_EXTENSIONS.some((ext) => name.endsWith(ext))) {
    return "Please choose a JPG, JPEG, PNG, or PDF file.";
  }
  if (file.size > MAX_SIZE_MB * 1024 * 1024) {
    return `That file is larger than ${MAX_SIZE_MB} MB.`;
  }
  return "";
}

function ReceiptUpload() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [uploading, setUploading] = useState(false);

  function handleChoose(event) {
    const chosen = event.target.files[0] || null;
    setResult(null);
    setFile(chosen);
    setError(chosen ? checkFile(chosen) : "");
  }

  async function handleUpload() {
    setUploading(true);
    setError("");
    try {
      setResult(await uploadReceipt(file));
      setFile(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  }

  return (
    <section className="upload">
      <h2>Upload a receipt</h2>
      <input
        type="file"
        accept=".jpg,.jpeg,.png,.pdf"
        onChange={handleChoose}
        key={result ? result.id : "empty"}
      />
      <button onClick={handleUpload} disabled={!file || error !== "" || uploading}>
        {uploading ? "Uploading..." : "Upload"}
      </button>

      {error && <p className="status status-error">{error}</p>}
      {result && (
        <p className="status status-ok">
          Uploaded {result.original_filename} ({result.file_type},{" "}
          {Math.round(result.size_bytes / 1024)} KB). {result.message}
        </p>
      )}
    </section>
  );
}

export default ReceiptUpload;
