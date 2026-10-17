import { useEffect, useState } from "react";
import { getHealth } from "../services/api.js";

// Small status pill that shows whether the backend is reachable.
function HealthStatus() {
  const [state, setState] = useState({ status: "loading" });

  useEffect(() => {
    getHealth()
      .then((data) => setState({ status: "ok", data }))
      .catch(() => setState({ status: "error" }));
  }, []);

  if (state.status === "loading") {
    return <span className="pill"><i />Checking backend</span>;
  }

  if (state.status === "error") {
    return (
      <span className="pill pill-bad" title="Start it with: uvicorn main:app --reload --port 8000">
        <i />Backend offline
      </span>
    );
  }

  return (
    <span className="pill pill-ok">
      <i />Backend connected, v{state.data.version}
    </span>
  );
}

export default HealthStatus;