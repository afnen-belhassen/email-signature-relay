Email Signature Relay

A proof-of-concept platform for centralized email signature management.

The project currently provides a local SMTP relay that receives an email, identifies the sender, generates an HTML signature from user data, injects the signature into the message, and forwards the modified email to a local SMTP sink for validation.

A React-based administration dashboard is also being developed to manage signatures, assignments, directory information, logs, and system status.

Project Goal

The final goal is to build a centralized email signature management solution for Microsoft 365.

Target flow:

Microsoft 365 / Exchange Online→ SMTP Relay→ Sender identification→ Microsoft Graph user lookup→ Signature generation→ Signature injection→ Email forwarding

The current POC uses local mock data instead of Microsoft Graph and a local SMTP sink instead of the final Microsoft 365 mail flow.

Current Features

Local SMTP relay

HTML email processing

Sender identification

Dynamic signature generation with Jinja2

HTML signature injection

Local user data stored in JSON

Local SMTP sink for end-to-end testing

Saved .eml and HTML preview files

Unit tests with pytest

React administration dashboard prototype

Project Structure

email-signature-relay/
│
├── app/
│   ├── __init__.py
│   ├── email_injector.py
│   ├── email_processor.py
│   ├── send_test_email.py
│   ├── signature_engine.py
│   ├── smtp_relay.py
│   └── smtp_sink.py
│
├── data/
│   └── users.json
│
├── templates/
│   └── signature.html
│
├── tests/
│   ├── conftest.py
│   └── test_email_injector.py
│
├── frontend/
│   └── React administration interface
│
├── output/
│   └── Generated email previews and test files
│
├── requirements.txt
└── README.md

Main Python Files

send_test_email.py

Creates and sends a test email to the local SMTP relay.

smtp_relay.py

Receives the email, triggers the signature-processing workflow, and forwards the modified message.

email_processor.py

Parses the received email, identifies the sender, and coordinates the signature-generation and injection process.

signature_engine.py

Loads user information and generates an HTML signature using the Jinja2 template.

email_injector.py

Injects the generated signature into the HTML content of the email.

smtp_sink.py

Acts as a fake final SMTP server during local testing and saves the final signed email.

Current Local Flow

send_test_email.py
        ↓
SMTP Relay - 127.0.0.1:1025
        ↓
email_processor.py
        ↓
signature_engine.py
        ↓
users.json + signature.html
        ↓
email_injector.py
        ↓
SMTP Sink - 127.0.0.1:1026
        ↓
final_received_email.eml

Installation

1. Clone the repository

git clone <repository-url>
cd email-signature-relay

2. Create a virtual environment

Windows:

python -m venv .venv
.venv\Scripts\activate

3. Install Python dependencies

pip install -r requirements.txt

Run the Local SMTP POC

Open three terminals from the project root.

Terminal 1 - Start the SMTP sink

python app\smtp_sink.py

The sink listens on:

127.0.0.1:1026

Terminal 2 - Start the SMTP relay

python app\smtp_relay.py

The relay listens on:

127.0.0.1:1025

Terminal 3 - Send a test email

python app\send_test_email.py

The processed email is saved in the output/ folder.

To open the final HTML preview on Windows:

Start-Process .\output\final_preview.html

Run the Tests

pytest

The tests currently focus on the signature-injection logic, including correct HTML insertion and prevention of duplicate signature injection.

Frontend

The administration interface is built with:

React

Vite

To run it:

cd frontend
npm install
npm run dev

The development server is available locally, usually at:

http://localhost:5173

The current dashboard is a UI prototype. Some values such as relay status, Microsoft Graph status, directory user count, and processed email count are currently mocked and are not yet connected to the Python backend.

Planned Backend API

The React dashboard will communicate with the Python backend through FastAPI.

Target architecture:

React Dashboard
      ↓
    FastAPI
      ↓
Python services
   ├── SMTP Relay
   ├── Signature Engine
   ├── Logs
   ├── Assignments
   └── Microsoft Graph

FastAPI will expose endpoints such as:

GET /api/relay/status
GET /api/users
GET /api/signatures
GET /api/logs
POST /api/assignments

Microsoft Graph Integration

The current POC reads employee information from:

data/users.json

The target implementation will replace this local source with Microsoft Graph.

Planned flow:

Sender email
    ↓
graph_client.py
    ↓
Microsoft Entra ID authentication
    ↓
Microsoft Graph
    ↓
Employee profile
    ↓
signature_engine.py

Expected user fields include:

display name

email

job title

department

business phone

mobile phone

office location

For an app-only POC, the application is expected to use an Entra App Registration with a Tenant ID, Client ID, development credential, and appropriate Microsoft Graph application permissions granted by an administrator.

Secrets must never be committed to GitHub.

Future Improvements

Microsoft Graph integration

FastAPI backend for the admin dashboard

Multiple signature templates

Signature assignment rules by department, group, or user

Microsoft 365 / Exchange Online mail-flow integration

Anti-loop protection

Centralized logs and monitoring

Authentication for the admin platform

Docker containerization

CI/CD with GitHub Actions

Production-ready secret management

Improved error handling and fallback behavior

Current POC vs Target Production System

Current POC:

Test Email
→ Local SMTP Relay
→ Local JSON User Data
→ Signature Injection
→ Local SMTP Sink

Target system:

Microsoft 365
→ SMTP Relay
→ Microsoft Graph
→ Signature Rules
→ Signature Injection
→ Microsoft 365 / Recipient

Security Notes

Do not commit .env files.

Do not commit Microsoft Entra client secrets.

Use environment variables for credentials.

Prefer certificates or another stronger credential mechanism for production.

Request only the Microsoft Graph permissions required by the application.

Use test accounts or an isolated test tenant whenever production directory access is not available.

Status

The local SMTP signature-processing POC is implemented.

The React administration dashboard is under development.

Microsoft Graph, FastAPI, and Microsoft 365 production mail-flow integration are planned as the next major steps.