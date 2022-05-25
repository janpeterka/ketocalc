from flask import request, url_for, redirect, flash, session
from flask import current_app as application
from flask_classful import route
from flask_login import login_required, current_user, login_user

from app.auth import admin_required

from app.handlers.mail import MailSender

from app.helpers.base_view import BaseView
from app.helpers.form import create_form, save_form_to_session

from app.models import User

from app.forms import UserForm, PasswordForm


class UserView(BaseView):
    decorators = [login_required]

    def before_request(self, name, *args, **kwargs):
        self.user = current_user

    def show(self, **kwargs):
        return self.template()

    def edit(self):
        self.user_form = create_form(UserForm, obj=self.user)
        self.password_form = create_form(PasswordForm)

        return self.template()

    @route("update", methods=["POST"])
    def update(self, page_type=None):
        form = UserForm(request.form)
        del form.username

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("UserView:edit"))

        self.user.first_name = form.first_name.data
        self.user.last_name = form.last_name.data

        if self.user.edit() is not None:
            flash("Uživatel byl upraven", "success")
        else:
            flash("Nepovedlo se změnit uživatele", "error")

        return redirect(url_for("UserView:show"))

    @route("update_password", methods=["POST"])
    def update_password(self):
        form = PasswordForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("UserView:edit"))

        self.user.set_password_hash(form.password.data)
        self.user.password_version = application.config["PASSWORD_VERSION"]

        if self.user.edit():
            flash("Heslo bylo změněno", "success")
        else:
            flash("Nepovedlo se změnit heslo", "error")

        return redirect(url_for("UserView:show"))

    @admin_required
    def show_by_id(self, id):
        return self.template("users/show.html.j2")

    @admin_required
    def show_all(self):
        users = User.load_all()

        return self.template("admin/users/all.html.j2", users=users)

    @admin_required
    def login_as(self, user_id, back=False):
        if "back" in request.args:
            back = request.args["back"]
        session.pop("logged_from_admin", None)
        if not back:
            session["logged_from_admin"] = current_user.id
        login_user(User.load(user_id))
        return redirect(url_for("IndexView:index"))

    @admin_required
    def send_mail(self, user_id, mail_type):
        user = User.load(user_id)

        if mail_type == "onboarding_inactive":
            MailSender().send_onboarding_inactive(recipients=[user])
            flash("email byl odeslán", "success")
        elif mail_type == "onboarding_welcome":
            MailSender().send_onboarding_welcome(recipients=[user])
            flash("email byl odeslán", "success")
        else:
            flash("nejspíš neznáme typ mailu", "error")

        return redirect(url_for("UserView:show_all"))
