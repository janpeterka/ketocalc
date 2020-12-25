# from flask import redirect, url_for

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
        from app.helpers.general import created_recently

        self.days = 30
        self.new_users = User.created_recently(days=self.days)
        self.new_recipes = Recipe.created_recently(days=self.days)
        self.new_ingredients = Ingredient.created_recently(days=self.days)
        self.new_images = ImageFile.created_recently(days=self.days)
        self.share_recipe_toggles = created_recently(
            RequestLog.load_by_like(attribute="url", pattern="recipes/toggle_shared"),
            days=self.days,
        )

        return self.template()
