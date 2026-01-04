from flask_mail import Message
from app import mail


def send_email(subject, recipients, body, html=None):
    """
    Send an email with a subject, plain text body, and optional HTML body.
    """
    msg = Message(subject, recipients=recipients)
    msg.body = body
    if html:
        msg.html = html
    mail.send(msg) 