from flask import redirect, url_for, request, flash
from flask import render_template as template
from flask import current_app as application

from flask_classful import FlaskView, route
from flask_login import current_user

from app.auth.routes import generate_new_password_token
from app.helpers.form import create_form, save_form_to_session
from app.handlers.mail import MailHandler
from app.models.users import User
from app.controllers.forms.password_recovery import NewPasswordForm, GetNewPasswordForm


class PasswordRecoveryView(FlaskView):
    def before_request(self, name):
        if current_user.is_authenticated:
            return redirect(url_for("IndexView:index"))

    def show(self):
        form = create_form(GetNewPasswordForm)
        return template("auth/get_new_password.html.j2", form=form)

    def post(self):
        form = GetNewPasswordForm(request.form)
        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("PasswordRecoveryView:show"))

        user = User.load(form.username.data, load_type="username")

        html_body = template(
            "auth/mails/_new_password_email.html.j2",
            token=generate_new_password_token(user),
        )

        MailHandler().send_email(
            subject="Nové heslo", recipients=[user], html_body=html_body,
        )

        flash("Nové heslo vám bylo zasláno do emailu", "success")
        return redirect(url_for("LoginView:show"))

    def show_token(self):
        token = request.args["token"]
        form = create_form(NewPasswordForm)

        user = User.load(token, load_type="new_password_token")
        if user is None:
            flash("tento token již není platný", "error")
            return redirect(url_for("LoginView:show"))

        return template(
            "auth/new_password.html.j2", form=form, username=user.username, token=token
        )

    @route("/post_token", methods=["POST"])
    def post_token(self):
        token = request.args["token"]
        form = NewPasswordForm(request.form)
        user = User.load(token, load_type="new_password_token")

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("PasswordRecoveryView:show_token", token=token))

        if user is None:
            flash("nemůžete změnit heslo", "error")
        else:
            user.set_password_hash(form.password.data.encode("utf-8"))
            user.password_version = application.config["PASSWORD_VERSION"]
            user.new_password_token = None
            user.edit()
            flash("heslo bylo změněno", "success")

        return redirect(url_for("LoginView:show"))
