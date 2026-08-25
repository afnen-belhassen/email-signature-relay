export default function ApiError({ error }) {
  if (!error) {
    return null;
  }

  return (
    <div className="alert alert-error">
      <strong>Backend unavailable.</strong> Start FastAPI with{" "}
      <code>uvicorn main:app --reload</code> from the <code>backend/</code>{" "}
      folder. ({error})
    </div>
  );
}
