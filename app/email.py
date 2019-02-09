from flask_mail import Message

from app import mail


def send_email(subject, sender, recipients, text_body, html_body, attachments=None):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(attachment.filename, 'application/octact-stream', attachment.read())
    mail.send(msg)
