import datetime

from flask import redirect, url_for
from flask_login import current_user, login_required

from app.helpers.formaters import parse_date
from app.helpers.base_view import BaseView

from app.models import DailyPlan


class DailyPlanView(BaseView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None, *args, **kwargs):
        self.daily_plan = DailyPlan.load(id)

        if "date" in kwargs:
            self.date = kwargs["date"]
            if not isinstance(self.date, datetime.date):
                self.date = parse_date(self.date)
            self.daily_plan = DailyPlan.load_by_date_or_create(self.date)

    def before_show(self, date):
        if not isinstance(self.date, datetime.date):
            self.date = parse_date(self.date)

        self.daily_plan = DailyPlan.load_by_date_or_create(self.date)

    def index(self):
        return redirect(url_for("DailyPlanView:show", date=datetime.date.today()))

    def show(self, date):
        date_before = self.date + datetime.timedelta(days=-1)
        date_after = self.date + datetime.timedelta(days=1)
        self.dates = {"active": self.date, "previous": date_before, "next": date_after}

        self.daily_recipes = self.daily_plan.daily_recipes
        self.daily_recipes.sort(key=lambda x: x.order_index)
        self.diets = current_user.active_diets

        return self.template()
