from flask import render_template

from flask_mail import Message

from app import mail

from app.models.sent_mails import SentMail


class MailHandler(object):
    def send_email(
        subject,
        recipients,
        text_body=None,
        html_body=None,
        template=None,
        attachments=None,
        sender="ketocalc.jmp@gmail.com",
    ):
        if not isinstance(recipients, list):
            raise ValueError

        message = Message(
            subject=subject,
            sender=sender,
            recipients=recipients,
            bcc=["ketocalc.jmp+bcc@gmail.com"],
        )

        if template:
            message.template = template
            html_body = render_template(template)

        if text_body is None and html_body is None:
            raise ValueError

        message.body = text_body
        message.html = html_body

        if attachments:
            for attachment in attachments:
                message.attach(
                    attachment.filename, "application/octact-stream", attachment.read()
                )
        mail.send(message)
        for recipient in recipients:
            message.recipient = recipient
            sent_mail = SentMail()
            sent_mail.fill_from_message(message)
            sent_mail.save()

    # Specific emails
    def send_onboarding_inactive(self, recipients):
        self.send_email(
            subject="Ketokalkulačka - mohu Vám pomoci?",
            template="onboarding/inactive_after_register.html.j2",
        )
