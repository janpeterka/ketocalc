import datetime

from flask import request, redirect, url_for
from flask_login import current_user, login_required

from app.models.diets import Diet
from app.models.daily_plans import DailyPlan

from app.controllers.extended_flask_view import ExtendedFlaskView


class DashboardView(ExtendedFlaskView):
    decorators = [login_required]

    def before_index(self):
        self.selected_diet_id = request.args.get("selected_diet_id", None)

    def index(self):
        if self.selected_diet_id is not None:
            self.selected_diet = Diet.load(self.selected_diet_id)
        elif len(current_user.active_diets) > 0:
            self.selected_diet = current_user.active_diets[0]
        else:
            self.selected_diet = None

        self.diets = current_user.active_diets
        self.daily_plan = DailyPlan.load_by_date_or_create(date=datetime.date.today())
        self.daily_recipes = self.daily_plan.daily_recipes

        return self.template(
            "dashboard/dashboard.html.j2", first_name=current_user.first_name,
        )

    def show(self, **kwargs):
        return redirect(url_for("DashboardView:index"))

    def post(self):
        return redirect(
            url_for("DashboardView:index", selected_diet_id=request.form["select_diet"])
        )
