from app.signature_engine import generate_signature


SIGNATURE_MARKER = "<!-- signature-injected-by-email-signature-relay -->"


def inject_signature(html_body: str, signature_html: str) -> str:
    """
    Injects the signature before the closing </body> tag.
    If the signature is already present, it does not add it again.
    """

    if SIGNATURE_MARKER in html_body:
        print("Signature marker already found. Skipping HTML injection.")
        return html_body

    signature_with_marker = SIGNATURE_MARKER + "\n" + signature_html

    if "</body>" in html_body:
        return html_body.replace("</body>", signature_with_marker + "\n</body>")

    return html_body + signature_with_marker


if __name__ == "__main__":
    sender = "afnen.belhassen@esprit.tn"

    email_body = """
    <html>
      <body>
        <p>Hello,</p>
        <p>Please find attached the document.</p>
        <p>Best regards,</p>
      </body>
    </html>
    """

    signature = generate_signature(sender)
    final_email = inject_signature(email_body, signature)

    print("Final email with signature:")
    print(final_email)