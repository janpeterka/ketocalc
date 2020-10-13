# import datetime

# from flask import request, redirect, url_for
# from flask_login import current_user, login_required

# from app.models.diets import Diet
# from app.models.daily_plans import DailyPlan

from app.models.recipes import Recipe

from app.controllers.extended_flask_view import ExtendedFlaskView


class CookbookView(ExtendedFlaskView):
    template_folder = "cookbook"

    def before_index(self):
        self.recipes = Recipe.public_recipes()
