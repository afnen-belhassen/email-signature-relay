from signature_engine import generate_signature


def inject_signature(html_body: str, signature_html: str) -> str:
    """
    Injects the signature before the closing </body> tag.
    If there is no </body>, it adds the signature at the end.
    """

    if "</body>" in html_body:
        return html_body.replace("</body>", signature_html + "\n</body>")

    return html_body + signature_html


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