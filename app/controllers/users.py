from flask import render_template as template
from flask import request, url_for, redirect, abort, flash
from flask import current_app as application

from flask_classful import FlaskView, route
from flask_login import login_required, current_user

from app.auth import admin_required

from app.helpers.form import create_form, save_form_to_session

from app.controllers.forms.users import UserForm, PasswordForm
from app.models.users import User


class UsersView(FlaskView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, *args, **kwargs):
        self.user = User.load(current_user.id)
        if self.user is None:
            abort(404)

    def post(self, page_type=None):
        form = UserForm(request.form)
        del form.username

        if not form.validate_on_submit():
            print("no validate")
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
        return template("users/show.html.j2", user=self.user)

    def edit(self):
        user_form = create_form(UserForm, obj=self.user)
        password_form = create_form(PasswordForm)
        return template(
            "users/edit.html.j2",
            user=self.user,
            user_form=user_form,
            password_form=password_form,
        )

    @admin_required
    def show_by_id(self, id):
        user = User.load(id)
        if user:
            return template("users/show.html.j2", user=user)
        else:
            flash("Uživatel neexistuje", "error")
            return redirect(url_for("UsersView:show_all"))

    @admin_required
    def show_all(self):
        users = User.load_all()
        return template("admin/users/all.html.j2", users=users)
