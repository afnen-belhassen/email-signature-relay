from pathlib import Path
from aiosmtpd.controller import Controller
from app.email_processor import extract_html_body


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


class SmtpSinkHandler:
    async def handle_DATA(self, server, session, envelope):
        """
        This server simulates the final SMTP destination.
        It receives the signed email after the relay has processed it.
        """

        print("Final SMTP server received an email")
        print(f"From: {envelope.mail_from}")
        print(f"To: {envelope.rcpt_tos}")

        final_email = envelope.content

        final_email_path = OUTPUT_DIR / "final_received_email.eml"
        with open(final_email_path, "wb") as file:
            file.write(final_email)

        html_result = extract_html_body(final_email)

        if html_result:
            preview_path = OUTPUT_DIR / "final_preview.html"
            with open(preview_path, "w", encoding="utf-8") as file:
                file.write(html_result)

            print(f"Final HTML preview saved to: {preview_path}")

        print(f"Final email saved to: {final_email_path}")

        return "250 Final email received successfully"


if __name__ == "__main__":
    controller = Controller(
        SmtpSinkHandler(),
        hostname="127.0.0.1",
        port=1026
    )

    controller.start()

    print("Final SMTP sink is running on 127.0.0.1:1026")
    print("Press Ctrl+C to stop the server")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        controller.stop()
        print("SMTP sink stopped")