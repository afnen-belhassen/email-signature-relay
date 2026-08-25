import { useState } from "react";
import "./App.css";
import Dashboard from "./pages/Dashboard";
import Directory from "./pages/Directory";
import Settings from "./pages/Settings";
import Signatures from "./pages/Signatures";

const NAV_ITEMS = [
  { id: "dashboard", label: "Dashboard" },
  { id: "signatures", label: "Signatures" },
  { id: "assignments", label: "Assignments" },
  { id: "directory", label: "Directory" },
  { id: "logs", label: "Logs" },
  { id: "settings", label: "Settings" },
];

function PlaceholderPage({ title, description }) {
  return (
    <>
      <header className="topbar">
        <div>
          <h1>{title}</h1>
          <p>{description}</p>
        </div>
      </header>
      <div className="panel placeholder-panel">
        <p>This page is coming soon.</p>
      </div>
    </>
  );
}

function App() {
  const [activePage, setActivePage] = useState("dashboard");

  const renderPage = () => {
    switch (activePage) {
      case "dashboard":
        return <Dashboard />;
      case "signatures":
        return <Signatures />;
      case "assignments":
        return (
          <PlaceholderPage
            title="Assignments"
            description="Assign templates to users, groups, or departments."
          />
        );
      case "directory":
        return <Directory />;
      case "logs":
        return (
          <PlaceholderPage
            title="Logs"
            description="Review processed emails and injection results."
          />
        );
      case "settings":
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <h2>SignFlow</h2>
          <span>Email Signatures</span>
        </div>

        <nav>
          {NAV_ITEMS.map((item) => (
            <button
              key={item.id}
              type="button"
              className={`nav-item${activePage === item.id ? " active" : ""}`}
              onClick={() => setActivePage(item.id)}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </aside>

      <main className="main-content">{renderPage()}</main>
    </div>
  );
}

export default App;
