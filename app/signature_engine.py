import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "users.json"
TEMPLATE_DIR = BASE_DIR / "templates"


def load_users():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_signature(sender_email: str) -> str:
    users = load_users()

    if sender_email not in users:
        raise ValueError(f"No user found for email: {sender_email}")

    user_data = users[sender_email]

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("signature.html")

    return template.render(user_data)


if __name__ == "__main__":
    sender = "afnen.belhassen@esprit.tn"
    signature = generate_signature(sender)

    print("Generated signature:")
    print(signature)