import os
from pathlib import Path

from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def is_graph_configured():
    return all([
        TENANT_ID,
        CLIENT_ID,
        CLIENT_SECRET
    ])