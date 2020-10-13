from app.models.recipes import Recipe

from app.controllers.extended_flask_view import ExtendedFlaskView


class CookbookView(ExtendedFlaskView):
    template_folder = "cookbook"

    def before_index(self):
        self.recipes = Recipe.public_recipes()
