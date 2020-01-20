from flask import render_template as template
from flask import redirect, request, flash

from flask_classful import FlaskView, route

from flask_login import current_user, login_required

from app.email import send_email

from app.controllers.forms.feedback import FeedbackForm


class SupportView(FlaskView):
    @route("/terms")
    def showTerms(self):
        return template("support/terms.tpl")

    @route("/privacy")
    def showPrivacy(self):
        return template("support/privacy.tpl")

    @route("/google3748bc0390347e56.html")
    def googleVerification(self):
        return template("support/google3748bc0390347e56.html")

    @route("/feedback", methods=["GET", "POST"])
    @login_required
    def feedback(self):
        from werkzeug.datastructures import CombinedMultiDict

        form = FeedbackForm(CombinedMultiDict((request.files, request.form)))
        if request.method == "GET":
            return template("support/feedback.tpl", form=form)
        elif request.method == "POST":
            if not form.validate_on_submit():
                return template("support/feedback.tpl", form=form)

            attachments = []
            if form.feedback_file.data:
                attachments = [form.feedback_file.data]

            send_email(
                subject="[ketocalc] [{}]".format(form.option.data),
                sender="ketocalc",
                recipients=["ketocalc.jmp@gmail.com"],
                text_body="Message: {}\n Send by: {} [user: {}]".format(
                    form.message.data, form.email.data, current_user.username
                ),
                html_body=None,
                attachments=attachments,
            )

            flash("Vaše připomínka byla zaslána na vyšší místa.", "success")
            return redirect("/dashboard")

    @route("changelog")
    @login_required
    def changelog(self):
        return template("support/changelog.tpl")

    @route("help")
    def help(self):
        return template("support/help.tpl")
