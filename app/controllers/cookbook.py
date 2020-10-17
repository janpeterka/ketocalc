from app.models.recipes import Recipe

from flask_login import login_required

from app.controllers.extended_flask_view import ExtendedFlaskView


class CookbookView(ExtendedFlaskView):
    template_folder = "cookbook"
    decorators = [login_required]

    def before_index(self):
        self.recipes = Recipe.public_recipes()
