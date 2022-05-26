import datetime

from flask import request
from flask_login import current_user, login_required
from app.helpers.base_view import BaseView

from app.models import Diet, DailyPlan


class DashboardView(BaseView):
    decorators = [login_required]
    template_folder = "dashboard"

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

        self.first_name = current_user.first_name

        return self.template()
