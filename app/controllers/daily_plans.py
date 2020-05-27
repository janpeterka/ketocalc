import datetime
from datetime import date

from flask import redirect, url_for

from app.controllers.extended_flask_view import ExtendedFlaskView

from app.models.daily_plans import DailyPlan


class DailyPlansView(ExtendedFlaskView):
    def index(self):
        return redirect(url_for("DailyPlansView:show", date=date.today()))

    def show(self, date):
        date = self.__parse_date(date)
        date_before = date + datetime.timedelta(days=-1)
        date_after = date + datetime.timedelta(days=1)
        self.dates = {"active": date, "previous": date_before, "next": date_after}

        # daily_recipes = DailyPlan.load_by_date(date)
        return self.template("daily_plans/show.html.j2")

    def show_add_recipe(self):
        return None

    def add_recipe_AJAX(self, recipeID):
        return None

    # private
    def __parse_date(self, date):
        return datetime.datetime.strptime(date, "%Y-%m-%d").date()
