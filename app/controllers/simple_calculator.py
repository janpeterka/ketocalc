from flask_login import current_user

from app.models.ingredients import Ingredient

from .extended_flask_view import ExtendedFlaskView


class SimpleCalculatorView(ExtendedFlaskView):
    template_folder = "simple_calculator"

    def index(self):
        shared_ingredients = Ingredient.load_all_shared(renamed=True)

        if current_user.is_authenticated:
            users_ingredients = Ingredient.load_all_by_author(current_user.username)
            self.ingredients = users_ingredients + shared_ingredients
            self.diets = current_user.active_diets
        else:
            self.ingredients = shared_ingredients
            self.diets = None
        return self.template()
