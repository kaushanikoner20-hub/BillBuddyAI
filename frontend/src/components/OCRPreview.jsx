import { useState } from "react";

// The extracted text, shown on a receipt-paper strip.
// status is one of: "idle", "loading", "success", "error".
function OCRPreview({ status, result, error }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(result.extracted_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  }

  const hasText = status === "success" && result && result.extracted_text.trim() !== "";

  let body;
  if (status === "loading") {
    body = (
      <div className="skeleton" aria-label="Reading your receipt">
        <span /><span /><span /><span />
      </div>
    );
  } else if (status === "error") {
    body = <p className="hint">{error}</p>;
  } else if (status === "success" && result) {
    body = hasText ? (
      <pre>{result.extracted_text}</pre>
    ) : (
      <p className="hint">{result.message}</p>
    );
  } else {
    body = (
      <p className="hint">
        Choose a receipt and select Read receipt. The text it contains will
        print here.
      </p>
    );
  }

  return (
    <section className="receipt-wrap" aria-live="polite">
      <div className="receipt">
        <div className="receipt-head">
          <span>
            {status === "success" && result
              ? `Pages read: ${result.page_count}`
              : "Extracted text"}
          </span>
          {hasText && (
            <button onClick={handleCopy}>{copied ? "Copied" : "Copy text"}</button>
          )}
        </div>
        {body}
      </div>
    </section>
  );
}

export default OCRPreview;