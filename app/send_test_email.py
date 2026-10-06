import smtplib
from email.message import EmailMessage


def send_test_email():
    message = EmailMessage()

    message["From"] = "Afnen Belhassen <afnen.belhassen@intern-insomea.com>"
    message["To"] = "client@example.com"
    message["Subject"] = "Test email through SMTP relay"

    message.set_content("This is the plain text version.")

    message.add_alternative("""
    <html>
      <body>
        <p>Hello,</p>
        <p>This email was sent through the local SMTP relay.</p>
        <p>Best regards,</p>
      </body>
    </html>
    """, subtype="html")

    with smtplib.SMTP("127.0.0.1", 1025) as smtp:
        smtp.send_message(message)

    print("Test email sent to local SMTP relay")


if __name__ == "__main__":
    send_test_email()