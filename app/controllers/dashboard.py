from flask import render_template as template
from flask import request, redirect, url_for

from flask_classful import FlaskView
from flask_login import current_user, login_required

from app.models.diets import Diet


class DashboardView(FlaskView):
    decorators = [login_required]

    def index(self, selected_diet_id=None):
        if selected_diet_id is None and len(current_user.active_diets) > 0:
            self.selected_diet = current_user.active_diets[0]
        else:
            self.selected_diet = Diet.load(selected_diet_id)

        return template(
            "dashboard/dashboard.html.j2",
            diets=current_user.active_diets,
            selected_diet=self.selected_diet,
            first_name=current_user.first_name,
        )

    def show(self):
        return redirect(url_for("DashboardView:index"))

    def post(self):
        self.selected_diet = Diet.load(request.form["select_diet"])
        return template(
            "dashboard/dashboard.html.j2",
            diets=current_user.active_diets,
            selected_diet=self.selected_diet,
            first_name=current_user.first_name,
        )
