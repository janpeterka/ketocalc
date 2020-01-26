from flask import redirect, url_for

from flask_classful import FlaskView
from flask_login import current_user


class IndexView(FlaskView):
    route_base = "/"

    def index(self):
        if not current_user.is_anonymous:
            return redirect(url_for("DashboardView:index"))
        else:
            return redirect(url_for("LoginView:show"))