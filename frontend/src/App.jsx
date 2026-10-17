import HealthStatus from "./components/HealthStatus.jsx";
import ReceiptUpload from "./components/ReceiptUpload.jsx";
import "./App.css";

function App() {
  return (
    <div className="shell">
      <header className="topbar">
        <div className="brand">
          <svg viewBox="0 0 64 64" aria-hidden="true">
            <rect width="64" height="64" rx="14" fill="var(--accent)" />
            <path d="M20 14h24v36l-4-3-4 3-4-3-4 3-4-3-4 3z" fill="var(--accent-ink)" />
            <path d="M26 24h12M26 31h12M26 38h7" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" />
          </svg>
          BillBuddy AI
        </div>
        <HealthStatus />
      </header>

      <main>
        <div className="intro">
          <h1>Read your receipts without sending them anywhere</h1>
          <p>
            Add a receipt or invoice and BillBuddy reads the text on this
            computer. Nothing is uploaded to a cloud service.
          </p>
        </div>

        <ReceiptUpload />

        <p className="footnote">
          Pulling out vendor, date and total with AI comes next. Saving expenses
          comes after that.
        </p>
      </main>
    </div>
  );
}

export default App;