import "./App.css";

function App() {
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <h2>SignFlow</h2>
          <span>Email Signatures</span>
        </div>

        <nav>
          <button className="nav-item active">Dashboard</button>
          <button className="nav-item">Signatures</button>
          <button className="nav-item">Assignments</button>
          <button className="nav-item">Directory</button>
          <button className="nav-item">Logs</button>
          <button className="nav-item">Settings</button>
        </nav>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <h1>Dashboard</h1>
            <p>Manage your organization's email signatures.</p>
          </div>

          <div className="user">
            <div className="avatar">AB</div>

            <div>
              <strong>Administrator</strong>
              <p>admin@company.com</p>
            </div>
          </div>
        </header>

        <section className="stats">
          <div className="stat-card">
            <p>Relay status</p>
            <h2>Online</h2>
            <span className="success">● Running</span>
          </div>

          <div className="stat-card">
            <p>Directory users</p>
            <h2>1</h2>
            <span>Local data</span>
          </div>

          <div className="stat-card">
            <p>Signature templates</p>
            <h2>1</h2>
            <span>Active template</span>
          </div>

          <div className="stat-card">
            <p>Processed emails</p>
            <h2>0</h2>
            <span>Today</span>
          </div>
        </section>

        <section className="content-grid">
          <div className="panel">
            <div className="panel-header">
              <h2>System status</h2>
            </div>

            <div className="status-row">
              <span>SMTP Relay</span>
              <span className="status-online">Connected</span>
            </div>

            <div className="status-row">
              <span>Microsoft Graph</span>
              <span className="status-pending">Not configured</span>
            </div>

            <div className="status-row">
              <span>Microsoft 365</span>
              <span className="status-pending">Not configured</span>
            </div>
          </div>

          <div className="panel">
            <div className="panel-header">
              <h2>Recent activity</h2>
            </div>

            <div className="empty-state">
              <p>No email activity yet.</p>
              <span>Processed emails will appear here.</span>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;