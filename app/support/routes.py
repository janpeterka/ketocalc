#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run by pyserver
from flask import request, redirect, flash
from flask import Blueprint
from flask import render_template as template
from flask import current_app as application

from flask_login import login_required, current_user

from app.support import forms

from app.models import Log

from app.email import send_email
from app.auth import admin_required


support_blueprint = Blueprint("support_blueprint", __name__)

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


@support_blueprint.route("/tests")
@support_blueprint.route("/testing")
@login_required
@admin_required
def testingPage():
    tests = []
    # tests.append()
    return template(
        "support/testing.tpl", tests=tests, version=application.config["APP_STATE"]
    )


@support_blueprint.route("/test_landing")
def testingLandingPage():
    # tests.append()
    return template("support/tests.html.j2")


@support_blueprint.route("/logs")
@support_blueprint.route("/logs/<date>")
@support_blueprint.route("/logging")
@support_blueprint.route("/logging/<date>")
@login_required
@admin_required
def logPage(date="2019-05-01"):
    application.logger.info("{} accessed logs.".format(current_user.id))
    logs = Log.load_since(date)
    return template("support/logs.tpl", logs=logs)


# @support_blueprint.route('/terms')
# def showTerms():
#     return template('support/terms.tpl')


# @support_blueprint.route('/privacy')
# def showPrivacy():
#     return template('support/privacy.tpl')


@support_blueprint.route("/google3748bc0390347e56.html")
def googleVerification():
    return template("support/google3748bc0390347e56.html")


@support_blueprint.route("/feedback", methods=["GET", "POST"])
@login_required
def showFeedback():
    from werkzeug.datastructures import CombinedMultiDict

    form = forms.FeedbackForm(CombinedMultiDict((request.files, request.form)))
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


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# S'MORE
@support_blueprint.route("/changelog")
@login_required
def showChangelog():
    return template("support/changelog.tpl")


@support_blueprint.route("/help")
def showHelp():
    return template("support/help.tpl")
