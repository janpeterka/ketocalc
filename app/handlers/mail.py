from flask import render_template as template

from flask_mail import Message

from app import mail


class MailHandler(object):
    def send_email(
        subject,
        recipients,
        text_body=None,
        html_body=None,
        sender="ketocalc.jmp@gmail.com",
        attachments=None,
    ):
        if not isinstance(recipients, list):
            raise ValueError

        msg = Message(
            subject=subject,
            sender=sender,
            recipients=recipients,
            bcc=["ketocalc.jmp+bcc@gmail.com"],
        )
        if text_body is None and html_body is None:
            raise ValueError

        msg.body = text_body
        msg.html = html_body

        if attachments:
            for attachment in attachments:
                msg.attach(
                    attachment.filename, "application/octact-stream", attachment.read()
                )
        mail.send(msg)

    # Specific emails
    def send_onboarding_inactive(self, recipients):
        self.send_email(
            subject="Ketokalkulačka - mohu Vám pomoci?",
            html_body=template("mails/onboarding/inactive_after_register.html.j2"),
        )
