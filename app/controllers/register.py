from flask import redirect, url_for, request, session, flash
from flask import render_template as template
from flask import current_app as application

from flask_classful import FlaskView, route
from flask_login import current_user

from app.controllers.forms.register import RegisterForm
from app.auth.routes import validate_register, do_register

from app.helpers.form import create_form

from app.models.users import User


class RegisterView(FlaskView):
    route_base = "/register"

    def before_request(self, name):
        if current_user.is_authenticated:
            return redirect(url_for("IndexView:index"))

    @route("")
    def show(self):
        form = create_form(RegisterForm)
        return template("auth/register.html.j2", form=form)

    def post(self):
        form = RegisterForm(request.form)
        if not form.validate_on_submit():
            session["formdata"] = request.form
            return redirect(url_for("RegisterView:show"))
        if not validate_register(form.username.data):
            # TODO: tohle teď nic nedělá - form se nezachová - přepsat jinam?
            form.username.errors = ["Toto jméno nemůžete použít"]
            # for now...
            flash("Toto jméno nemůžete použít")
            session["formdata"] = request.form
            return redirect(url_for("RegisterView:show"))

        user = User()
        form.populate_obj(user)
        user.set_password_hash(form.password.data.encode("utf-8"))
        user.password_version = application.config["PASSWORD_VERSION"]

        if do_register(user):
            return redirect(url_for("IndexView:index"))
        else:
            session["formdata"] = request.form
            return redirect(url_for("RegisterView:show"))
