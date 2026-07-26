from pathlib import Path
from aiosmtpd.controller import Controller

from email_processor import process_raw_email, extract_html_body


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


class SignatureRelayHandler:
    async def handle_DATA(self, server, session, envelope):
        """
        This function is called every time the SMTP relay receives an email.
        """

        print("New email received")
        print(f"From: {envelope.mail_from}")
        print(f"To: {envelope.rcpt_tos}")

        raw_email = envelope.content

        try:
            processed_email = process_raw_email(raw_email)

            signed_email_path = OUTPUT_DIR / "signed_email.eml"
            with open(signed_email_path, "wb") as file:
                file.write(processed_email)

            html_result = extract_html_body(processed_email)

            if html_result:
                preview_path = OUTPUT_DIR / "preview.html"
                with open(preview_path, "w", encoding="utf-8") as file:
                    file.write(html_result)

                print(f"HTML preview saved to: {preview_path}")

            print(f"Signed email saved to: {signed_email_path}")

            return "250 Message processed successfully"

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