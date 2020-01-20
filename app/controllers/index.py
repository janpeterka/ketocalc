from flask_classful import FlaskView

from flask import redirect, url_for


class IndexView(FlaskView):
    route_base = "/"

    def index(self):
        return redirect(url_for("DashboardView:index"))
