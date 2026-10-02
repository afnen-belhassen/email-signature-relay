from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from backend.user_service import get_user_by_email


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"


def generate_signature(sender_email: str) -> str:
    user_data = get_user_by_email(sender_email)

    if not user_data:
        raise ValueError(
            f"No user found for email: {sender_email}"
        )

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR)
    )

    template = env.get_template("signature.html")

    return template.render(user_data)


if __name__ == "__main__":
    sender = "afnen.belhassen@intern-insomea.com"

    signature = generate_signature(sender)

    print("Generated signature:")
    print(signature)