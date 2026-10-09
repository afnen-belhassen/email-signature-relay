import os
import base64
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

def get_all_users():
    token = get_access_token()

    url = "https://graph.microsoft.com/v1.0/users"

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

    if response.status_code == 403:
        raise RuntimeError(
            "Microsoft Graph refused access. "
            "Check User.Read.All and admin consent."
        )

    response.raise_for_status()

    return response.json().get("value", [])

def send_mail(
    sender_email: str,
    recipient_email: str,
    subject: str,
    html_body: str
):
    token = get_access_token()

    url = (
        "https://graph.microsoft.com/v1.0/"
        f"users/{sender_email}/sendMail"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": html_body,
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": recipient_email
                    }
                }
            ],
        },
        "saveToSentItems": True,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=10,
    )

    if response.status_code == 403:
        raise RuntimeError(
            "Microsoft Graph refused access. "
            "Check Mail.Send and admin consent."
        )

    response.raise_for_status()

    return response.status_code
def send_mime_mail(sender_email: str, raw_email: bytes):
    """
    Sends a complete MIME email through Microsoft Graph.

    raw_email is the already processed email containing:
    - original sender
    - original recipients
    - subject
    - HTML/plain-text body
    - injected signature
    - MIME headers
    """

    token = get_access_token()

    url = (
        "https://graph.microsoft.com/v1.0/"
        f"users/{sender_email}/sendMail"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "text/plain",
    }

    encoded_email = base64.b64encode(raw_email).decode("ascii")

    response = requests.post(
        url,
        headers=headers,
        data=encoded_email,
        timeout=20,
    )

    if response.status_code == 403:
        raise RuntimeError(
            "Microsoft Graph refused access. "
            "Check Mail.Send and admin consent."
        )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Microsoft Graph sendMail failed: "
            f"{response.status_code} - {response.text}"
        )

    return response.status_code
