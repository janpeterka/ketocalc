from flask import redirect, url_for
from flask import render_template as template
from flask_login import current_user

from app.helpers.base_view import BaseView
from app.models import Ingredient, User


class TrialRecipeView(BaseView):
    def before_index(self):
        if current_user.is_authenticated:
            return redirect(url_for("IndexView:index"))

    def index(self):
        shared_user = User.load_shared_user()
        preset_ingredients = self._get_preset_trial_ingredients()

        return template(
            "recipes/new.html.j2",
            ingredients=Ingredient.load_all_shared(),
            preset_ingredients=[i.id for i in preset_ingredients],
            diets=shared_user.active_diets,
            is_trialrecipe=True,
        )

    def _get_preset_trial_ingredients(self):
        preset_ingredients = []

        ingredient = Ingredient.load_shared_by_name("Ananas")
        if ingredient:
            preset_ingredients.append(ingredient)
        else:
            preset_ingredients.append(Ingredient.load_random_by_nutrient("sugar"))

        ingredient = Ingredient.load_shared_by_name("Avokádo")
        if ingredient:
            preset_ingredients.append(ingredient)
        else:
            preset_ingredients.append(Ingredient.load_random_by_nutrient("fat"))

        ingredient = Ingredient.load_shared_by_name("Maso - krůtí, prsa bez kosti")
        if ingredient:
            preset_ingredients.append(ingredient)
        else:
            preset_ingredients.append(Ingredient.load_random_by_nutrient("protein"))

        return preset_ingredients
