import { useCallback, useEffect, useState } from "react";
import { getSettingsData } from "../api/client";
import ApiError from "../components/ApiError";
import StatusBadge from "../components/StatusBadge";

export default function Settings() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadSettings = useCallback(async () => {
    setError(null);

    try {
      const settingsData = await getSettingsData();
      setData(settingsData);
    } catch (err) {
      setError(err.message ?? "Unable to reach the backend API.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadSettings();
  }, [loadSettings]);

  const graphConfigured = data?.graph?.configured;
  const relayRunning = data?.relay?.running;

  return (
    <>
      <header className="topbar">
        <div>
          <h1>Settings</h1>
          <p>Monitor backend, Graph, and relay configuration.</p>
        </div>

        <div className="topbar-actions">
          <button
            type="button"
            className="btn-secondary"
            onClick={loadSettings}
            disabled={loading && !data}
          >
            Refresh
          </button>
        </div>
      </header>

      <ApiError error={error} />

      <section className="content-grid">
        <div className="panel">
          <div className="panel-header">
            <h2>Service status</h2>
          </div>

          {loading && !data ? (
            <div className="panel-loading">
              <div className="skeleton skeleton-row" />
              <div className="skeleton skeleton-row" />
              <div className="skeleton skeleton-row" />
            </div>
          ) : (
            <>
              <div className="status-row">
                <span>Backend API</span>
                <StatusBadge status={data?.health?.status ?? "offline"} />
              </div>

              <div className="status-row">
                <span>SMTP Relay</span>
                <StatusBadge status={relayRunning ? "online" : "offline"} />
              </div>

              <div className="status-row">
                <span>Microsoft Graph</span>
                <StatusBadge
                  status={graphConfigured ? "connected" : "not_configured"}
                />
              </div>
            </>
          )}
        </div>

        <div className="panel">
          <div className="panel-header">
            <h2>General configuration</h2>
          </div>

          {loading && !data ? (
            <div className="panel-loading">
              <div className="skeleton skeleton-row" />
              <div className="skeleton skeleton-row" />
              <div className="skeleton skeleton-row" />
            </div>
          ) : (
            <>
              <div className="config-row">
                <span>User directory source</span>
                <strong>Local (users.json)</strong>
              </div>

              <div className="config-row">
                <span>SMTP relay host</span>
                <strong>{data?.relay?.host ?? "—"}</strong>
              </div>

              <div className="config-row">
                <span>SMTP relay port</span>
                <strong>{data?.relay?.port ?? "—"}</strong>
              </div>

              <div className="config-row">
                <span>Microsoft Graph credentials</span>
                <strong>
                  {graphConfigured ? "Configured in .env" : "Not configured"}
                </strong>
              </div>

              <p className="config-note">
                Secrets such as CLIENT_SECRET are never displayed in the UI.
                Configure them in the backend <code>.env</code> file.
              </p>
            </>
          )}
        </div>
      </section>
    </>
  );
}
