import json
from pathlib import Path


def get_user_by_email(email: str):

    users_file = Path(__file__).resolve().parent.parent / "data" / "users.json"

    with open(users_file, "r", encoding="utf-8") as file:
        users = json.load(file)

    return users.get(email)