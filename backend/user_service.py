import json
from pathlib import Path

USERS_FILE = Path(__file__).resolve().parent.parent / "data" / "users.json"


def _load_users() -> dict:
    with open(USERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_user_by_email(email: str):
    return _load_users().get(email)


def get_all_users() -> list[dict]:
    users = _load_users()
    return list(users.values())