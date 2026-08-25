import { useCallback, useEffect, useState } from "react";
import {
  getSignature,
  getSignaturePreview,
  getSignatures,
  getUsers,
  updateSignature,
} from "../api/client";
import ApiError from "../components/ApiError";

export default function Signatures() {
  const [templates, setTemplates] = useState([]);
  const [users, setUsers] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [templateDetail, setTemplateDetail] = useState(null);
  const [preview, setPreview] = useState(null);
  const [previewEmail, setPreviewEmail] = useState("");
  const [view, setView] = useState("preview");
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadTemplates = useCallback(async () => {
    setError(null);

    try {
      const [signaturesData, usersData] = await Promise.all([
        getSignatures(),
        getUsers(),
      ]);

      setTemplates(signaturesData.templates ?? []);
      setUsers(usersData.users ?? []);
      setSelectedId(
        (current) => current ?? signaturesData.templates?.[0]?.id ?? null,
      );
    } catch (err) {
      setError(err.message ?? "Unable to reach the backend API.");
    } finally {
      setLoading(false);
    }
  }, []);

  const loadTemplateDetail = useCallback(async (templateId, email) => {
    if (!templateId) {
      return;
    }

    setDetailLoading(true);

    try {
      const [detail, previewData] = await Promise.all([
        getSignature(templateId),
        getSignaturePreview(templateId, email || undefined),
      ]);

      setTemplateDetail(detail);
      setPreview(previewData);
    } catch (err) {
      setError(err.message ?? "Unable to load template details.");
    } finally {
      setDetailLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTemplates();
  }, [loadTemplates]);

  useEffect(() => {
    if (selectedId) {
      loadTemplateDetail(selectedId, previewEmail);
    }
  }, [selectedId, previewEmail, loadTemplateDetail]);

  const handleToggleActive = async () => {
    if (!templateDetail) {
      return;
    }

    setSaving(true);
    setError(null);

    try {
      const updated = await updateSignature(templateDetail.id, {
        active: !templateDetail.active,
      });

      setTemplateDetail(updated);
      setTemplates((current) =>
        current.map((template) =>
          template.id === updated.id
            ? { ...template, active: updated.active }
            : template,
        ),
      );
    } catch (err) {
      setError(err.message ?? "Unable to update template status.");
    } finally {
      setSaving(false);
    }
  };

  const selectedTemplate = templates.find((template) => template.id === selectedId);

  return (
    <>
      <header className="topbar">
        <div>
          <h1>Signatures</h1>
          <p>Create and manage HTML signature templates.</p>
        </div>

        <div className="topbar-actions">
          <button
            type="button"
            className="btn-secondary"
            onClick={loadTemplates}
            disabled={loading}
          >
            Refresh
          </button>
        </div>
      </header>

      <ApiError error={error} />

      <section className="signatures-layout">
        <div className="panel signatures-list-panel">
          <div className="panel-header">
            <h2>Templates</h2>
            <p className="panel-subtitle">
              {loading ? "Loading..." : `${templates.length} template(s)`}
            </p>
          </div>

          {loading ? (
            <div className="panel-loading">
              <div className="skeleton skeleton-row" />
              <div className="skeleton skeleton-row" />
            </div>
          ) : templates.length ? (
            <ul className="template-list">
              {templates.map((template) => (
                <li key={template.id}>
                  <button
                    type="button"
                    className={`template-item${
                      selectedId === template.id ? " template-item--active" : ""
                    }`}
                    onClick={() => setSelectedId(template.id)}
                  >
                    <div>
                      <strong>{template.name}</strong>
                      <span>{template.filename}</span>
                    </div>
                    <span
                      className={
                        template.active ? "status-online" : "status-pending"
                      }
                    >
                      {template.active ? "Active" : "Inactive"}
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <div className="empty-state">
              <p>No templates found.</p>
              <span>Add HTML files to the templates/ folder.</span>
            </div>
          )}
        </div>

        <div className="panel signatures-detail-panel">
          {!selectedTemplate ? (
            <div className="empty-state">
              <p>Select a template to preview.</p>
            </div>
          ) : (
            <>
              <div className="panel-header panel-header--row">
                <div>
                  <h2>{selectedTemplate.name}</h2>
                  <p className="panel-subtitle">{selectedTemplate.filename}</p>
                </div>

                <button
                  type="button"
                  className={`btn-secondary${
                    templateDetail?.active ? " btn-secondary--active" : ""
                  }`}
                  onClick={handleToggleActive}
                  disabled={detailLoading || saving || !templateDetail}
                >
                  {templateDetail?.active ? "Set inactive" : "Set active"}
                </button>
              </div>

              <div className="preview-controls">
                <label htmlFor="preview-user">Preview as</label>
                <select
                  id="preview-user"
                  value={previewEmail}
                  onChange={(event) => setPreviewEmail(event.target.value)}
                  disabled={detailLoading || !users.length}
                >
                  <option value="">First user</option>
                  {users.map((user) => (
                    <option key={user.email} value={user.email}>
                      {user.display_name} ({user.email})
                    </option>
                  ))}
                </select>
              </div>

              <div className="view-tabs">
                <button
                  type="button"
                  className={`view-tab${view === "preview" ? " view-tab--active" : ""}`}
                  onClick={() => setView("preview")}
                >
                  Preview
                </button>
                <button
                  type="button"
                  className={`view-tab${view === "source" ? " view-tab--active" : ""}`}
                  onClick={() => setView("source")}
                >
                  HTML source
                </button>
              </div>

              {detailLoading ? (
                <div className="panel-loading">
                  <div className="skeleton skeleton-row" />
                  <div className="skeleton skeleton-row" />
                  <div className="skeleton skeleton-row" />
                </div>
              ) : view === "preview" ? (
                <div className="preview-frame-wrap">
                  <iframe
                    title={`Preview ${selectedTemplate.name}`}
                    className="preview-frame"
                    srcDoc={preview?.html ?? ""}
                    sandbox=""
                  />
                </div>
              ) : (
                <pre className="source-code">
                  <code>{templateDetail?.html ?? ""}</code>
                </pre>
              )}

              {preview?.preview_user && (
                <p className="preview-note">
                  Preview rendered with data from{" "}
                  <strong>{preview.preview_user.display_name}</strong>.
                </p>
              )}
            </>
          )}
        </div>
      </section>
    </>
  );
}
