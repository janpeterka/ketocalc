from flask import render_template as template

from flask_classful import FlaskView
from flask_login import current_user

from app.models.ingredients import Ingredient


class SimpleCalculatorView(FlaskView):
    def show(self):
        shared_ingredients = Ingredient.load_all_shared(renamed=True)

        if current_user.is_authenticated:
            ingredients = Ingredient.load_all_by_author(current_user.username)
            all_ingredients = ingredients + shared_ingredients
        else:
            all_ingredients = shared_ingredients
        return template("simple_calculator/show.html.j2", ingredients=all_ingredients)
