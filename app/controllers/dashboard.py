from flask import render_template as template

from flask_classful import FlaskView, route
from flask_login import current_user

from app.models.users import User
from app.models.diets import Diet


class DashboardView(FlaskView):
    def index(self):
        user = User.load(current_user.id)

        if len(user.active_diets) > 0:
            selected_diet = user.active_diets[0]
        else:
            selected_diet = None

        return template(
            "dashboard/dashboard.html.j2",
            diets=user.active_diets,
            selected_diet=selected_diet,
            first_name=user.first_name,
        )

    def post(self):
        selected_diet = Diet.load(request.form["select_diet"])
        return template(
            "dashboard/dashboard.html.j2",
            diets=user.active_diets,
            selected_diet=selected_diet,
            first_name=user.first_name,
        )
