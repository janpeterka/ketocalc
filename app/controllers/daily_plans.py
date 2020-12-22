import datetime

from flask import redirect, url_for, request, abort
from flask_classful import route
from flask_login import current_user, login_required

from app.helpers.formaters import parse_date

from app.data.texts import texts

from app.models.daily_plans import DailyPlan
from app.models.recipes import Recipe

from app.controllers.extended_flask_view import ExtendedFlaskView


class DailyPlansView(ExtendedFlaskView):
    def before_index(self):
        if not current_user.is_authenticated:
            message = texts.daily_plan.not_logged_in
            return redirect(url_for("DailyPlansView:not_logged_in", message=message))

    def before_request(self, name, id=None, *args, **kwargs):
        super().before_request(name, id, *args, **kwargs)

        if "date" in kwargs:
            self.date = kwargs["date"]
            if not isinstance(self.date, datetime.date):
                self.date = parse_date(self.date)
            self.daily_plan = DailyPlan.load_by_date_or_create(self.date)

    @login_required
    def index(self):
        return redirect(url_for("DailyPlansView:show", date=datetime.date.today()))

    @login_required
    def show(self, date):
        date_before = self.date + datetime.timedelta(days=-1)
        date_after = self.date + datetime.timedelta(days=1)
        self.dates = {"active": self.date, "previous": date_before, "next": date_after}

        # self.daily_plan = DailyPlan.load_by_date_or_create(date)
        self.daily_recipes = self.daily_plan.daily_recipes
        self.daily_recipes.sort(key=lambda x: x.order_index)
        self.diets = current_user.active_diets

        return self.template()

    @login_required
    def remove_daily_recipe(self, daily_recipe_id, date):
        daily_plan = DailyPlan.load_by_date_or_create(date)
        daily_plan.remove_daily_recipe_by_id(daily_recipe_id)
        return redirect(url_for("DailyPlansView:show", date=date))

    @route("/add_recipe", methods=["POST"])
    @login_required
    def add_recipe(self):
        recipe = Recipe.load(request.form["recipe_id"])
        if not recipe.can_current_user_add:
            abort(403)

        date = request.form["date"]

        recipe_percentage = float(request.form["recipe_percentage"])
        amount = round(recipe.totals.amount * (recipe_percentage / 100), 2)

        daily_plan = DailyPlan.load_by_date(date)

        daily_plan.add_recipe(recipe, amount)

        return redirect(url_for("DailyPlansView:show", date=date))

    def sort_up(self, daily_recipe_id, date):
        self.daily_plan.change_order(daily_recipe_id, order_type="up")
        return redirect(url_for("DailyPlansView:show", date=date))

    def sort_down(self, daily_recipe_id, date):
        self.daily_plan.change_order(daily_recipe_id, order_type="down")
        return redirect(url_for("DailyPlansView:show", date=date))
