import os
from pathlib import Path

import msal
from dotenv import load_dotenv

import requests

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]


def is_graph_configured():
    return all([
        TENANT_ID,
        CLIENT_ID,
        CLIENT_SECRET
    ])


def get_access_token():
    if not is_graph_configured():
        raise RuntimeError(
            "Microsoft Graph is not configured. "
            "Check TENANT_ID, CLIENT_ID and CLIENT_SECRET in .env."
        )

    authority = f"https://login.microsoftonline.com/{TENANT_ID}"

    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(
        scopes=GRAPH_SCOPE
    )

    if "access_token" not in result:
        error = result.get("error", "unknown_error")
        description = result.get(
            "error_description",
            "No error description returned."
        )

        raise RuntimeError(
            f"Unable to get Microsoft Graph token: "
            f"{error} - {description}"
        )

    return result["access_token"]

def get_user_by_email(email):
    token = get_access_token()

    url = f"https://graph.microsoft.com/v1.0/users/{email}"

    params = {
        "$select": (
            "displayName,"
            "mail,"
            "userPrincipalName,"
            "jobTitle,"
            "department,"
            "businessPhones,"
            "mobilePhone,"
            "officeLocation"
        )
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    if response.status_code == 404:
        raise RuntimeError(
            f"User not found in Microsoft Graph: {email}"
        )

    if response.status_code == 403:
        raise RuntimeError(
            "Microsoft Graph refused access. "
            "Check User.Read.All and admin consent."
        )

    response.raise_for_status()
    return response.json()
