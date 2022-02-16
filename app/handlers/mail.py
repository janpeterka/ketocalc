from flask import render_template
from flask import current_app as application

from flask_mail import Message

from app import mail

from app.models.sent_mails import SentMail

DEFAULT_SENDER = "ketocalc.jmp@gmail.com"
DEFAULT_BCC = "ketocalc.jmp+bcc@gmail.com"
DEFAULT_DEV = "ketocalc.jmp+dev@gmail.com"


class MailSender(object):
    """[summary]

    Class for handling all mail sending

    Usage:
        MailSender().send_email(subject="Nové heslo", recipients=[user], html_body=html_body)

    Using send_email() is preferrable to using send_single_email()

    When using send_email(), you must provide:
        - subject
        - recipients (list of Users) and/or reciptient_mails (list of strings)
        - text_body or html_body or template
    """

    def send_email(
        self,
        subject,
        recipients=[],
        recipient_mails=[],
        text_body=None,
        html_body=None,
        template=None,
        template_args={},
        attachments=None,
        sender=DEFAULT_SENDER,
    ):
        if recipients and not isinstance(recipients, list):
            raise ValueError("Recipients are in wrong format, should be list")

        for recipient in recipients:
            self.send_single_email(
                subject=subject,
                recipient=recipient,
                recipient_mail=recipient.username,
                text_body=text_body,
                html_body=html_body,
                template=template,
                template_args=template_args,
                attachments=attachments,
                sender=sender,
            )

        for recipient in recipient_mails:
            self.send_single_email(
                subject=subject,
                recipient_mail=recipient,
                text_body=text_body,
                html_body=html_body,
                template=template,
                template_args=template_args,
                attachments=attachments,
                sender=sender,
            )

    def send_single_email(
        self,
        subject,
        recipient=None,
        recipient_mail=None,
        text_body=None,
        html_body=None,
        template=None,
        template_args={},
        attachments=None,
        sender=DEFAULT_SENDER,
    ):
        if recipient:
            if recipient.last_name.endswith(tuple(("ová", "ova"))):
                template_args["gender"] = "f"
            else:
                template_args["gender"] = "m"

        if template:
            template = "mails/" + template
            html_body = render_template(template, **template_args)

        if text_body is None and html_body is None:
            raise ValueError("No message body, will not send empty e-mail")

        if application.config["APP_STATE"] != "production":
            recipient_mail = DEFAULT_DEV
            subject = f"[DEV only] {subject}"

        message = Message(
            subject=subject,
            sender=sender,
            recipients=[recipient_mail],
            bcc=[DEFAULT_BCC],
            body=text_body,
            html=html_body,
        )

        if attachments:
            for attachment in attachments:
                message.attach(
                    attachment.filename, "application/octact-stream", attachment.read()
                )

        mail.send(message)

        if template:
            message.template = template

        if application.config["APP_STATE"] == "production" and recipient:
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

    def send_onboarding_welcome(self, recipients):
        self.send_email(
            subject="Ketokalkulačka - vítejte!",
            recipients=recipients,
            template="onboarding/welcome.html.j2",
        )
