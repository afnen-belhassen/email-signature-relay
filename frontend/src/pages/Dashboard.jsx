import { useCallback, useEffect, useState } from "react";
import { getDashboardData } from "../api/client";
import ApiError from "../components/ApiError";
import StatusBadge from "../components/StatusBadge";function StatCard({ label, value, detail, variant }) {  return (
    <div className="stat-card stat-card--loading">
      <div className="skeleton skeleton-text skeleton-text--sm" />
      <div className="skeleton skeleton-text skeleton-text--lg" />
      <div className="skeleton skeleton-text skeleton-text--sm" />
    </div>
  );
}

function StatusBadge({ status }) {
  const labels = {
    online: "Connected",
    offline: "Offline",
    connected: "Connected",
    not_configured: "Not configured",
  };

  const className =
    status === "online" || status === "connected"
      ? "status-online"
      : status === "offline"
        ? "status-offline"
        : "status-pending";

  return <span className={className}>{labels[status] ?? status}</span>;
}

function formatActivityTime(timestamp) {
  return new Date(timestamp).toLocaleString();
}

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadDashboard = useCallback(async () => {
    setError(null);

    try {
      const dashboardData = await getDashboardData();
      setData(dashboardData);
    } catch (err) {
      setError(err.message ?? "Unable to reach the backend API.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDashboard();
    const interval = setInterval(loadDashboard, 30000);
    return () => clearInterval(interval);
  }, [loadDashboard]);

  const relayRunning = data?.relay?.running;
  const graphConfigured = data?.graph?.configured;

  return (
    <>
      <header className="topbar">
        <div>
          <h1>Dashboard</h1>
          <p>Manage your organization's email signatures.</p>
        </div>

        <div className="topbar-actions">
          <button
            type="button"
            className="btn-secondary"
            onClick={loadDashboard}
            disabled={loading && !data}
          >
            Refresh
          </button>

          <div className="user">
            <div className="avatar">AB</div>
            <div>
              <strong>Administrator</strong>
              <p>admin@company.com</p>
            </div>
          </div>
        </div>
      </header>

      {error && (
        <div className="alert alert-error">
          <strong>Backend unavailable.</strong> Start FastAPI with{" "}
          <code>uvicorn main:app --reload</code> from the <code>backend/</code>{" "}
          folder. ({error})
        </div>
      )}

      <section className="stats">
        {loading && !data ? (
          <>
            <StatCardSkeleton />
            <StatCardSkeleton />
            <StatCardSkeleton />
            <StatCardSkeleton />
          </>
        ) : (
          <>
            <StatCard
              label="Relay status"
              value={relayRunning ? "Online" : "Offline"}
              detail={relayRunning ? "● Running" : "● Stopped"}
              variant={relayRunning ? "success" : "danger"}
            />
            <StatCard
              label="Directory users"
              value={data?.users?.count ?? 0}
              detail={
                data?.users?.source === "local" ? "Local data" : "Microsoft Graph"
              }
            />
            <StatCard
              label="Signature templates"
              value={data?.signatures?.count ?? 0}
              detail={`${data?.signatures?.active_count ?? 0} active`}
            />
            <StatCard
              label="Processed emails"
              value={data?.logs?.processed_today ?? 0}
              detail="Today"
            />
          </>
        )}
      </section>

      <section className="content-grid">
        <div className="panel">
          <div className="panel-header">
            <h2>System status</h2>
          </div>

          {loading && !data ? (
            <div className="panel-loading">
              <div className="skeleton skeleton-row" />
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
                <StatusBadge
                  status={relayRunning ? "online" : "offline"}
                />
              </div>

              <div className="status-row">
                <span>Microsoft Graph</span>
                <StatusBadge
                  status={graphConfigured ? "connected" : "not_configured"}
                />
              </div>

              <div className="status-row">
                <span>Microsoft 365</span>
                <StatusBadge
                  status={graphConfigured ? "connected" : "not_configured"}
                />
              </div>
            </>
          )}
        </div>

        <div className="panel">
          <div className="panel-header">
            <h2>Recent activity</h2>
          </div>

          {loading && !data ? (
            <div className="panel-loading">
              <div className="skeleton skeleton-row" />
              <div className="skeleton skeleton-row" />
              <div className="skeleton skeleton-row" />
            </div>
          ) : data?.logs?.logs?.length ? (
            <ul className="activity-list">
              {data.logs.logs.map((entry) => (
                <li key={entry.id} className="activity-item">
                  <div>
                    <strong>{entry.user ?? entry.email}</strong>
                    <p>{entry.signature ?? "Signature applied"}</p>
                  </div>
                  <div className="activity-meta">
                    <span
                      className={
                        entry.success === false ? "status-offline" : "status-online"
                      }
                    >
                      {entry.success === false ? "Error" : "Success"}
                    </span>
                    <time>{formatActivityTime(entry.timestamp)}</time>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <div className="empty-state">
              <p>No email activity yet.</p>
              <span>Processed emails will appear here.</span>
            </div>
          )}
        </div>
      </section>
    </>
  );
}
