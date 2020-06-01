from flask import request, url_for, redirect, flash, session
from flask import current_app as application

from flask_classful import route
from flask_login import login_required, current_user, login_user

from app.auth import admin_required

from app.handlers.mail import MailHandler

from app.helpers.form import create_form, save_form_to_session

from app.models.users import User

from app.controllers.forms.users import UserForm, PasswordForm

from app.controllers.extended_flask_view import ExtendedFlaskView


class UsersView(ExtendedFlaskView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, *args, **kwargs):
        super().before_request(name, *args, **kwargs)
        if getattr(self, "user", None) is None:
            self.user = User.load(current_user.id)

    def post(self, page_type=None):
        form = UserForm(request.form)
        del form.username

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("UsersView:edit"))

        self.user.first_name = form.first_name.data
        self.user.last_name = form.last_name.data

        if self.user.edit() is not None:
            flash("Uživatel byl upraven", "success")
        else:
            flash("Nepovedlo se změnit uživatele", "error")

        return redirect(url_for("UsersView:show"))

    @route("edit_password", methods=["POST"])
    def post_password_edit(self):
        form = PasswordForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("UsersView:edit"))

        self.user.set_password_hash(form.password.data)
        self.user.password_version = application.config["PASSWORD_VERSION"]

        if self.user.edit():
            flash("Heslo bylo změněno", "success")
        else:
            flash("Nepovedlo se změnit heslo", "error")

        return redirect(url_for("UsersView:show"))

    def show(self):
        print(self.user)
        return self.template()

    def edit(self):
        self.user_form = create_form(UserForm, obj=self.user)
        self.password_form = create_form(PasswordForm)
        return self.template()

    @admin_required
    def show_by_id(self, id):
        user = User.load(id)
        if self.user:
            return self.template("users/show.html.j2", user=user)
        else:
            flash("Uživatel neexistuje", "error")
            return redirect(url_for("UsersView:show_all"))

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
            MailHandler().send_onboarding_inactive(recipients=[user])
            flash("email byl odeslán", "success")
        elif mail_type == "onboarding_welcome":
            MailHandler().send_onboarding_welcome(recipients=[user])
            flash("email byl odeslán", "success")
        else:
            flash("nejspíš neznáme typ mailu", "error")

        return redirect(url_for("UsersView:show_all"))
