import HealthStatus from "./components/HealthStatus.jsx";
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
      <p className="note">
        Stage 1 foundation only. Receipt upload, OCR, and AI extraction are
        planned for later stages.
      </p>
    </main>
  );
}

export default App;
