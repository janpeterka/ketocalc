from flask import redirect, url_for, request, flash
from flask import render_template as template
from flask import current_app as application
from flask_classful import FlaskView, route
from flask_login import current_user

from app.auth.routes import do_register
from app.helpers.form import create_form, save_form_to_session

from app.models import User

from app.forms import RegisterForm


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
            save_form_to_session(request.form)
            return redirect(url_for("RegisterView:show"))

        user = User()
        form.populate_obj(user)
        user.set_password_hash(form.password.data.encode("utf-8"))
        user.password_version = application.config["PASSWORD_VERSION"]

        if do_register(user):
            return redirect(url_for("IndexView:index"))
        flash("registrace se nepodařila", "error")
        save_form_to_session(request.form)
        return redirect(url_for("RegisterView:show"))
