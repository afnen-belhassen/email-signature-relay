from backend.graph_service import get_user_by_email as get_graph_user_by_email
import json 
from pathlib import Path

USERS_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "users.json"
)
def get_all_users() -> list[dict]:
    if not USERS_FILE.exists():
        return []

    with open(
        USERS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        users = json.load(file)

    return list(users.values())

def _map_graph_user(graph_user: dict) -> dict:
    business_phones = graph_user.get("businessPhones") or []

    phone = ""
    if business_phones:
        phone = business_phones[0]
    elif graph_user.get("mobilePhone"):
        phone = graph_user["mobilePhone"]

    return {
        "display_name": graph_user.get("displayName") or "",
        "job_title": graph_user.get("jobTitle") or "",
        "department": graph_user.get("department") or "",
        "phone": phone,
        "email": (
            graph_user.get("mail")
            or graph_user.get("userPrincipalName")
            or ""
        ),
        "office_location": graph_user.get("officeLocation") or "",
    }


def get_user_by_email(email: str):
    graph_user = get_graph_user_by_email(email)

    if not graph_user:
        return None

    return _map_graph_user(graph_user)