from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from graph_service import is_graph_configured
from log_service import get_logs, get_processed_email_count_today
from relay_service import get_relay_status
from signature_service import get_signature_templates
from user_service import get_all_users, get_user_by_email

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Email Signature Relay API is running", "status": "online"}


@app.get("/health")
def health():
    return {"status": "online"}


@app.get("/users")
def list_users():
    users = get_all_users()
    return {
        "users": users,
        "count": len(users),
        "source": "local",
    }


@app.get("/users/{email}")
def get_user(email: str):
    user = get_user_by_email(email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.get("/relay/status")
def relay_status():
    return get_relay_status()


@app.get("/graph/status")
def graph_status():
    configured = is_graph_configured()
    return {
        "configured": configured,
        "status": "connected" if configured else "not_configured",
    }


@app.get("/signatures")
def list_signatures():
    templates = get_signature_templates()
    active_count = sum(1 for template in templates if template["active"])

    return {
        "templates": templates,
        "count": len(templates),
        "active_count": active_count,
    }


@app.get("/logs")
def list_logs(limit: int = 10):
    logs = get_logs(limit=limit)
    return {
        "logs": logs,
        "count": len(logs),
        "processed_today": get_processed_email_count_today(),
    }
