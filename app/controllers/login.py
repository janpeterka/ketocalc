from flask import redirect, url_for, request
from flask import render_template as template

from flask_classful import FlaskView, route
from flask_login import current_user

from app.helpers.form import create_form, save_form_to_session

from app.controllers.forms.login import LoginForm
from app.auth.routes import do_login


class LoginView(FlaskView):
    route_base = "/login"

    def before_request(self, name):
        if current_user.is_authenticated:
            return redirect(url_for("IndexView:index"))

    @route("")
    def show(self):
        form = create_form(LoginForm)
        return template("auth/login.html.j2", form=form)

    def post(self):
        form = LoginForm(request.form)
        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("LoginView:show"))

        if do_login(username=form.username.data, password=form.password.data):
            return redirect(url_for("IndexView:index"))
        else:
            return redirect(url_for("LoginView:show"))
