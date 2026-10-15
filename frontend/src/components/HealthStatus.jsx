import { useEffect, useState } from "react";
import { getHealth } from "../services/api.js";

// Shows whether the backend is reachable.
function HealthStatus() {
  const [state, setState] = useState({ status: "loading" });

  useEffect(() => {
    getHealth()
      .then((data) => setState({ status: "ok", data }))
      .catch(() => setState({ status: "error" }));
  }, []);

  if (state.status === "loading") {
    return <p className="status">Checking backend...</p>;
  }

  if (state.status === "error") {
    return (
      <p className="status status-error">
        Backend not reachable. Start it with: uvicorn main:app --reload --port 8000
      </p>
    );
  }

  return (
    <p className="status status-ok">
      Backend connected: {state.data.app} v{state.data.version}
    </p>
  );
}

export default HealthStatus;
