from app.email_injector import inject_signature, SIGNATURE_MARKER


def test_inject_signature_before_body_end():
    html_body = """
    <html>
      <body>
        <p>Hello</p>
      </body>
    </html>
    """

    signature = "<p>My Signature</p>"

    result = inject_signature(html_body, signature)

    assert "My Signature" in result
    assert SIGNATURE_MARKER in result
    assert result.index("My Signature") < result.index("</body>")


def test_does_not_inject_signature_twice():
    html_body = f"""
    <html>
      <body>
        <p>Hello</p>
        {SIGNATURE_MARKER}
        <p>Existing Signature</p>
      </body>
    </html>
    """

    signature = "<p>New Signature</p>"

    result = inject_signature(html_body, signature)

    assert "New Signature" not in result
    assert "Existing Signature" in result