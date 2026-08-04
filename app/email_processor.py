from email import policy
from email.parser import BytesParser
from email.message import EmailMessage
from email.utils import parseaddr

from signature_engine import generate_signature
from email_injector import inject_signature


def process_raw_email(raw_email: bytes) -> bytes:
    """
    Takes a raw email, detects the sender, injects the correct signature,
    and returns the modified email.
    """

    message = BytesParser(policy=policy.default).parsebytes(raw_email)

    if message.get("X-Signature-Processed", "").lower() == "true":
        print("Email already processed. Skipping signature injection.")
        return message.as_bytes(policy=policy.SMTP)

    sender_header = message.get("From")
    sender_email = parseaddr(sender_header)[1]

    signature = generate_signature(sender_email)

    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/html":
                html_body = part.get_content()
                updated_html = inject_signature(html_body, signature)
                part.set_content(updated_html, subtype="html")
                break
    else:
        if message.get_content_type() == "text/html":
            html_body = message.get_content()
            updated_html = inject_signature(html_body, signature)
            message.set_content(updated_html, subtype="html")

    message["X-Signature-Processed"] = "true"

    return message.as_bytes(policy=policy.SMTP)


def extract_html_body(raw_email: bytes) -> str:
    """
    Extracts the HTML body from a raw email.
    Used to generate preview.html.
    """

    message = BytesParser(policy=policy.default).parsebytes(raw_email)

    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/html":
                return part.get_content()

    if message.get_content_type() == "text/html":
        return message.get_content()

    return ""


if __name__ == "__main__":
    test_email = EmailMessage()

    test_email["From"] = "Afnen Belhassen <afnen.belhassen@esprit.tn>"
    test_email["To"] = "client@example.com"
    test_email["Subject"] = "Test signature injection"

    test_email.set_content("This is the plain text version.")

    test_email.add_alternative("""
    <html>
      <body>
        <p>Hello,</p>
        <p>Please find attached the document.</p>
        <p>Best regards,</p>
      </body>
    </html>
    """, subtype="html")

    processed_email = process_raw_email(test_email.as_bytes())

    html_result = extract_html_body(processed_email)

    if html_result:
        with open("preview.html", "w", encoding="utf-8") as file:
            file.write(html_result)

        print("HTML preview generated: preview.html")
    else:
        print("No HTML body found.")