from flask import render_template

from flask_mail import Message

from app import mail

from app.models.sent_mails import SentMail


class MailHandler(object):
    def send_email(
        self,
        subject,
        recipients=None,
        recipient_mails=[],
        text_body=None,
        html_body=None,
        template=None,
        attachments=None,
        sender="ketocalc.jmp@gmail.com",
    ):
        if recipients and not isinstance(recipients, list):
            raise ValueError

        if recipients:
            for recipient in recipients:
                recipient_mails.append(recipient.username)

        message = Message(
            subject=subject,
            sender=sender,
            recipients=recipient_mails,
            bcc=["ketocalc.jmp+bcc@gmail.com"],
        )

        if template:
            template = "mails/" + template
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
            recipients=recipients,
            template="onboarding/inactive.html.j2",
        )

    def send_test_mail(self, recipients):
        self.send_email(
            subject="Ketokalkulačka - testovací e-mail",
            recipients=recipients,
            template="onboarding/inactive.html.j2",
        )
