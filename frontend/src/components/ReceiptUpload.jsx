import { useEffect, useState } from "react";
import { extractReceiptText } from "../services/api.js";
import OCRPreview from "./OCRPreview.jsx";

const ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".pdf"];
const MAX_SIZE_MB = 10; // The backend enforces the real limit.

// Returns an error message, or "" if the file looks fine.
function checkFile(file) {
  const name = file.name.toLowerCase();
  if (!ALLOWED_EXTENSIONS.some((ext) => name.endsWith(ext))) {
    return "Choose a JPG, JPEG, PNG, or PDF file.";
  }
  if (file.size > MAX_SIZE_MB * 1024 * 1024) {
    return `That file is larger than ${MAX_SIZE_MB} MB. Choose a smaller one.`;
  }
  return "";
}

function formatSize(bytes) {
  if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function ReceiptUpload() {
  const [file, setFile] = useState(null);
  const [fileError, setFileError] = useState("");
  const [previewUrl, setPreviewUrl] = useState("");
  const [dragging, setDragging] = useState(false);
  const [status, setStatus] = useState("idle"); // idle, loading, success, error
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [inputKey, setInputKey] = useState(0); // changing this clears the file input

  const loading = status === "loading";
  const isPdf = file && file.name.toLowerCase().endsWith(".pdf");

  // Show a small thumbnail for images, and free it when the file changes.
  useEffect(() => {
    if (!file || isPdf) {
      setPreviewUrl("");
      return undefined;
    }
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file, isPdf]);

  function chooseFile(chosen) {
    setFile(chosen);
    setFileError(chosen ? checkFile(chosen) : "");
    setStatus("idle");
    setResult(null);
    setError("");
  }

  function handleDrop(event) {
    event.preventDefault();
    setDragging(false);
    if (!loading && event.dataTransfer.files[0]) {
      chooseFile(event.dataTransfer.files[0]);
    }
  }

  async function handleExtract() {
    if (!file || fileError || loading) return; // blocks double submits
    setStatus("loading");
    setResult(null);
    setError("");
    try {
      setResult(await extractReceiptText(file));
      setStatus("success");
    } catch (err) {
      setError(err.message);
      setStatus("error");
    }
  }

  function handleReset() {
    chooseFile(null);
    setInputKey((key) => key + 1);
  }

  return (
    <div className="workspace">
      <section className="card">
        <h2>Your receipt</h2>

        {!file ? (
          <label
            className={`dropzone${dragging ? " dragging" : ""}`}
            onDragOver={(event) => { event.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={handleDrop}
          >
            <strong>Drop a receipt here</strong>
            <span>or click to choose a file</span>
            <span>JPG, PNG or PDF, up to {MAX_SIZE_MB} MB</span>
            <input
              type="file"
              accept=".jpg,.jpeg,.png,.pdf"
              onChange={(event) => chooseFile(event.target.files[0] || null)}
              key={inputKey}
            />
          </label>
        ) : (
          <div className="preview">
            {previewUrl ? (
              <img className="thumb" src={previewUrl} alt="Selected receipt" />
            ) : (
              <div className="thumb">PDF</div>
            )}
            <div className="file-meta">
              <strong>{file.name}</strong>
              <span>{formatSize(file.size)}</span>
            </div>
          </div>
        )}

        {fileError && <p className="msg bad">{fileError}</p>}
        {status === "error" && <p className="msg bad">{error}</p>}
        {status === "success" && result && <p className="msg ok">{result.message}</p>}
        {loading && <div className="progress" role="progressbar" aria-label="Reading receipt" />}

        <div className="actions">
          <button className="btn" onClick={handleExtract} disabled={!file || fileError !== "" || loading}>
            {loading ? "Reading..." : "Read receipt"}
          </button>
          {file && (
            <button className="btn quiet" onClick={handleReset} disabled={loading}>
              Choose another
            </button>
          )}
        </div>
      </section>

      <OCRPreview status={status} result={result} error={error} />
    </div>
  );
}

export default ReceiptUpload;