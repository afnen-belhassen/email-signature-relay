import os
from pathlib import Path
import smtplib
from aiosmtpd.controller import Controller

from app.email_processor import process_raw_email, extract_html_body


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

NEXT_SMTP_HOST = os.getenv("NEXT_SMTP_HOST", "127.0.0.1")
NEXT_SMTP_PORT = int(os.getenv("NEXT_SMTP_PORT", "1026"))


def forward_email(mail_from: str, rcpt_tos: list[str], raw_email: bytes):
    """
    Sends the processed email to the next SMTP server.
    In our POC, the next SMTP server is the local smtp_sink.py.
    Later, this could be Microsoft 365.
    """

    with smtplib.SMTP(NEXT_SMTP_HOST, NEXT_SMTP_PORT) as smtp:
        smtp.sendmail(mail_from, rcpt_tos, raw_email)


class SignatureRelayHandler:
    async def handle_DATA(self, server, session, envelope):
        """
        This function is called every time the SMTP relay receives an email.
        """

        print("New email received by signature relay")
        print(f"From: {envelope.mail_from}")
        print(f"To: {envelope.rcpt_tos}")

        raw_email = envelope.content

        try:
            processed_email = process_raw_email(raw_email)

            signed_email_path = OUTPUT_DIR / "signed_email_before_forwarding.eml"
            with open(signed_email_path, "wb") as file:
                file.write(processed_email)

            html_result = extract_html_body(processed_email)

            if html_result:
                preview_path = OUTPUT_DIR / "relay_preview.html"
                with open(preview_path, "w", encoding="utf-8") as file:
                    file.write(html_result)

                print(f"Relay HTML preview saved to: {preview_path}")

            print(f"Signed email saved to: {signed_email_path}")

            forward_email(
                mail_from=envelope.mail_from,
                rcpt_tos=envelope.rcpt_tos,
                raw_email=processed_email
            )

            print("Signed email forwarded to next SMTP server")

            return "250 Message processed and forwarded successfully"

        except Exception as error:
            print(f"Error while processing email: {error}")
            return "550 Error while processing email"


if __name__ == "__main__":
    controller = Controller(
        SignatureRelayHandler(),
        hostname="127.0.0.1",
        port=1025
    )

    controller.start()

    print("SMTP signature relay is running on 127.0.0.1:1025")
    print("Press Ctrl+C to stop the server")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        controller.stop()
        print("SMTP relay stopped")
