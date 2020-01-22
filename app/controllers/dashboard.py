from flask import render_template as template
from flask import request

from flask_classful import FlaskView
from flask_login import current_user, login_required

from app.models.users import User
from app.models.diets import Diet


class DashboardView(FlaskView):
    decorators = [login_required]

    def before_request(self, name):
        if hasattr(current_user, "id"):
            self.user = User.load(current_user.id)

    def index(self, selected_diet_id=None):
        if selected_diet_id is None:
            if len(self.user.active_diets) > 0:
                selected_diet = self.user.active_diets[0]
            else:
                selected_diet = None
        else:
            selected_diet = Diet.load(selected_diet_id)

        return template(
            "dashboard/dashboard.html.j2",
            diets=self.user.active_diets,
            selected_diet=selected_diet,
            first_name=self.user.first_name,
        )

    def post(self):
        selected_diet = Diet.load(request.form["select_diet"])
        return template(
            "dashboard/dashboard.html.j2",
            diets=self.user.active_diets,
            selected_diet=selected_diet,
            first_name=self.user.first_name,
        )
