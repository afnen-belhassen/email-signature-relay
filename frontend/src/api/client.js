const API_BASE = "/api";

async function fetchJson(path) {
  const response = await fetch(`${API_BASE}${path}`);

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export function getHealth() {
  return fetchJson("/health");
}

export function getRelayStatus() {
  return fetchJson("/relay/status");
}

export function getGraphStatus() {
  return fetchJson("/graph/status");
}

export function getUsers() {
  return fetchJson("/users");
}

export function getSignatures() {
  return fetchJson("/signatures");
}

export function getSignature(templateId) {
  return fetchJson(`/signatures/${templateId}`);
}

export function getSignaturePreview(templateId, email) {
  const query = email ? `?email=${encodeURIComponent(email)}` : "";
  return fetchJson(`/signatures/${templateId}/preview${query}`);
}

export async function updateSignature(templateId, data) {
  const response = await fetch(`${API_BASE}/signatures/${templateId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export function getLogs(limit = 5) {
  return fetchJson(`/logs?limit=${limit}`);
}

export async function getSettingsData() {
  const [health, relay, graph] = await Promise.all([
    getHealth(),
    getRelayStatus(),
    getGraphStatus(),
  ]);

  return { health, relay, graph };
}

export async function getDashboardData() {
  const [health, relay, graph, users, signatures, logs] = await Promise.all([
    getHealth(),
    getRelayStatus(),
    getGraphStatus(),
    getUsers(),
    getSignatures(),
    getLogs(),
  ]);

  return { health, relay, graph, users, signatures, logs };
}
