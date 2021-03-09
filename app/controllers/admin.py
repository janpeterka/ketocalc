# from flask import redirect, url_for

# from flask_login import current_user

from app.auth import admin_required

from app.models.recipes import Recipe
from app.models.users import User
from app.models.daily_plans import DailyPlan
from app.models.ingredients import Ingredient
from app.models.files import ImageFile
from app.models.request_log import RequestLog


from app.controllers.extended_flask_view import ExtendedFlaskView


class AdminView(ExtendedFlaskView):
    template_folder = "admin"
    decorators = [admin_required]

    def index(self):
        from app.helpers.general import created_recently

        self.days = 30
        self.new_users = User.created_in_last_30_days()
        self.new_recipes = Recipe.created_in_last_30_days()
        self.new_ingredients = Ingredient.created_in_last_30_days()
        self.daily_plans = [
            plan
            for plan in DailyPlan.created_in_last_30_days()
            if len(plan.daily_recipes) > 0
        ]
        self.new_images = ImageFile.created_in_last_30_days()
        self.share_recipe_toggles = created_recently(
            RequestLog.load_by_like(attribute="url", pattern="recipes/toggle_shared"),
            days=self.days,
        )

        return self.template()
