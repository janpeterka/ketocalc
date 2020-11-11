from flask import redirect

# from flask_login import current_user

from app.auth import admin_required

from app.models.recipes import Recipe
from app.models.users import User
from app.models.ingredients import Ingredient
from app.models.files import ImageFile
from app.models.request_log import RequestLog


from app.controllers.extended_flask_view import ExtendedFlaskView


class AdminView(ExtendedFlaskView):
    template_folder = "admin"
    decorators = [admin_required]

    def index(self):
        self.days = 30
        self.new_users = User.created_recently(days=self.days)
        self.new_recipes = Recipe.created_recently(days=self.days)
        self.new_ingredients = Ingredient.created_recently(days=self.days)
        self.new_images = ImageFile.created_recently(days=self.days)
        self.share_recipe_toggles = RequestLog.load_by_like(
            attribute="url", pattern="recipes/toggle_shared"
        )

        self.test = User.load_all()

        return self.template()

    def update_recipe_ratios(self):
        recipes = Recipe.load_all()

        for recipe in recipes:
            recipe.update_ratio()

        return redirect("/admin/")
