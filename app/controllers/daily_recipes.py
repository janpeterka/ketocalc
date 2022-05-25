from flask import redirect, url_for, request, abort
from flask_classful import route
from flask_login import login_required

from app.helpers.base_view import BaseView

from app.models import DailyPlan, Recipe, DailyPlanHasRecipes


class DailyRecipeView(BaseView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None, *args, **kwargs):
        self.daily_recipe = DailyPlanHasRecipes.load(id)
        self.daily_plan = self.daily_recipe.daily_plan

    def before_add_recipe(self):
        self.recipe = Recipe.load(request.form["recipe_id"])
        if not self.recipe.can_current_user_add:
            abort(403)

    def remove_recipe(self, id, date):
        self.daily_recipe.daily_plan.remove_recipe_by_id(id)

        return redirect(url_for("DailyPlanView:show", date=date))

    @route("/add", methods=["POST"])
    def add_recipe(self):
        date = request.form["date"]

        recipe_percentage = float(request.form["recipe_percentage"])
        amount = round(self.recipe.totals.amount * (recipe_percentage / 100), 2)

        daily_plan = DailyPlan.load_by_date(date)

        daily_plan.add_recipe(self.recipe, amount)

        return redirect(url_for("DailyPlanView:show", date=date))

    def sort_up(self, id, date):
        self.daily_plan.change_order(id, order_type="up")

        return redirect(url_for("DailyPlanView:show", date=date))

    def sort_down(self, id, date):
        self.daily_plan.change_order(id, order_type="down")

        return redirect(url_for("DailyPlanView:show", date=date))
