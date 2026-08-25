const LABELS = {
  online: "Connected",
  offline: "Offline",
  connected: "Connected",
  not_configured: "Not configured",
};

export default function StatusBadge({ status }) {
  const className =
    status === "online" || status === "connected"
      ? "status-online"
      : status === "offline"
        ? "status-offline"
        : "status-pending";

  return <span className={className}>{LABELS[status] ?? status}</span>;
}
