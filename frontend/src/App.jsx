import HealthStatus from "./components/HealthStatus.jsx";
import ReceiptUpload from "./components/ReceiptUpload.jsx";
import "./App.css";

function App() {
  return (
    <main className="app">
      <h1>BillBuddy AI</h1>
      <p className="tagline">
        A local, open-source receipt and invoice organizer for freelancers and
        small businesses.
      </p>
      <HealthStatus />
      <ReceiptUpload />
      <p className="note">
        Stage 2: uploading works. Text extraction (OCR) and AI extraction are
        planned for later stages.
      </p>
    </main>
  );
}

export default App;