import { useCallback, useEffect, useState } from "react";
import { getUsers } from "../api/client";
import ApiError from "../components/ApiError";

export default function Directory() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadUsers = useCallback(async () => {
    setError(null);

    try {
      const usersData = await getUsers();
      setData(usersData);
    } catch (err) {
      setError(err.message ?? "Unable to reach the backend API.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

  const sourceLabel =
    data?.source === "local" ? "Local data (users.json)" : "Microsoft Graph";

  return (
    <>
      <header className="topbar">
        <div>
          <h1>Directory</h1>
          <p>Browse users from local data or Microsoft Graph.</p>
        </div>

        <div className="topbar-actions">
          <button
            type="button"
            className="btn-secondary"
            onClick={loadUsers}
            disabled={loading && !data}
          >
            Refresh
          </button>
        </div>
      </header>

      <ApiError error={error} />

      <div className="panel">
        <div className="panel-header panel-header--row">
          <div>
            <h2>Users</h2>
            <p className="panel-subtitle">
              {loading && !data
                ? "Loading users..."
                : `${data?.count ?? 0} user(s) · ${sourceLabel}`}
            </p>
          </div>
          {data?.source === "local" && (
            <span className="source-badge">Local</span>
          )}
        </div>

        {loading && !data ? (
          <div className="panel-loading">
            <div className="skeleton skeleton-row" />
            <div className="skeleton skeleton-row" />
            <div className="skeleton skeleton-row" />
          </div>
        ) : data?.users?.length ? (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Job title</th>
                  <th>Department</th>
                  <th>Phone</th>
                </tr>
              </thead>
              <tbody>
                {data.users.map((user) => (
                  <tr key={user.email}>
                    <td>{user.display_name}</td>
                    <td>{user.email}</td>
                    <td>{user.job_title || "—"}</td>
                    <td>{user.department || "—"}</td>
                    <td>{user.phone || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <p>No users found.</p>
            <span>Add entries to data/users.json to populate the directory.</span>
          </div>
        )}
      </div>
    </>
  );
}
