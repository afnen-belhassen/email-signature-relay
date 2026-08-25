from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def get_signature_templates() -> list[dict]:
    templates = []

    for template_path in sorted(TEMPLATES_DIR.glob("*.html")):
        templates.append(
            {
                "id": template_path.stem,
                "name": template_path.stem.replace("_", " ").title(),
                "filename": template_path.name,
                "active": True,
            }
        )

    return templates
