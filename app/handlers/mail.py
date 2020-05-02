from flask import render_template
from flask import current_app as application

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
        template_args={},
        attachments=None,
        sender="ketocalc.jmp@gmail.com",
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
        sender="ketocalc.jmp@gmail.com",
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
            recipient = None
            recipient_mail = "dev"

        message = Message(
            subject=subject,
            sender=sender,
            recipients=[recipient_mail],
            bcc=["ketocalc.jmp+bcc@gmail.com"],
            body=text_body,
            html=html_body,
        )

        # with application.open_resource("static/img/banner.png") as fp:
        #     message.attach("logo.png", "image/png", fp.read())

        if attachments:
            for attachment in attachments:
                message.attach(
                    attachment.filename, "application/octact-stream", attachment.read()
                )

        mail.send(message)

        if recipient:
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
