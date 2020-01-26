from werkzeug import MultiDict

from flask import redirect, url_for, request, session
from flask import render_template as template

from flask_classful import FlaskView, route
from flask_login import current_user

from app.controllers.forms.login import LoginForm
from app.auth.routes import do_login


class LoginView(FlaskView):
    route_base = "/login"

    def before_request(self, name):
        if current_user.is_authenticated:
            return redirect(url_for("IndexView:index"))

    @route("")
    def show(self):
        form_data = None
        if session.get("formdata") is not None:
            form_data = MultiDict(session.get("formdata"))
            session.pop("formdata")
        if form_data:
            form = LoginForm(form_data)
            form.validate()
        else:
            form = LoginForm()

        return template("auth/login.html.j2", form=form)

    def post(self):
        form = LoginForm(request.form)
        if not form.validate_on_submit():
            session["formdata"] = request.form
            return redirect(url_for("LoginView:show"))

        if do_login(
            username=form.username.data, password=form.password.data.encode("utf-8")
        ):
            return redirect(url_for("IndexView:index"))
        else:
            return redirect(url_for("LoginView:show"))
