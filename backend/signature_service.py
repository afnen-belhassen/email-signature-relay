import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from backend.user_service import get_all_users, get_user_by_email

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
CONFIG_FILE = Path(__file__).resolve().parent.parent / "data" / "signatures.json"


def _load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def _save_config(config: dict) -> None:
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=2)
        file.write("\n")


def _template_path(template_id: str) -> Path:
    return TEMPLATES_DIR / f"{template_id}.html"


def _is_active(template_id: str, config: dict) -> bool:
    return config.get(template_id, {}).get("active", True)


def get_signature_templates() -> list[dict]:
    config = _load_config()
    templates = []

    for template_path in sorted(TEMPLATES_DIR.glob("*.html")):
        template_id = template_path.stem
        templates.append(
            {
                "id": template_id,
                "name": template_id.replace("_", " ").title(),
                "filename": template_path.name,
                "active": _is_active(template_id, config),
            }
        )

    return templates


def get_signature_template(template_id: str) -> dict | None:
    template_path = _template_path(template_id)

    if not template_path.exists():
        return None

    config = _load_config()

    return {
        "id": template_id,
        "name": template_id.replace("_", " ").title(),
        "filename": template_path.name,
        "active": _is_active(template_id, config),
        "html": template_path.read_text(encoding="utf-8"),
    }


def render_signature_preview(template_id: str, email: str | None = None) -> dict:
    template_path = _template_path(template_id)

    if not template_path.exists():
        raise ValueError(f"Template not found: {template_id}")

    if email:
        user = get_user_by_email(email)
        if not user:
            raise ValueError(f"No user found for email: {email}")
    else:
        users = get_all_users()
        if not users:
            raise ValueError("No users available for preview")
        user = users[0]

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template(template_path.name)
    html = template.render(user)

    return {
        "html": html,
        "preview_user": user,
    }


def set_template_active(template_id: str, active: bool) -> dict:
    if not _template_path(template_id).exists():
        raise ValueError(f"Template not found: {template_id}")

    config = _load_config()
    config.setdefault(template_id, {})["active"] = active
    _save_config(config)

    return get_signature_template(template_id)
