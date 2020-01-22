from flask import render_template as template

from flask_classful import FlaskView

from app.models.ingredients import Ingredient
from app.models.users import User


class TrialRecipesView(FlaskView):
    def show(self):
        active_diets = User.load(
            "ketocalc.jmp@gmail.com", load_type="username"
        ).active_diets
        ingredients = Ingredient.load_all_by_author("basic")
        return template(
            "recipes/new.html.j2",
            ingredients=ingredients,
            diets=active_diets,
            is_trialrecipe=True,
        )
