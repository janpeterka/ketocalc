from flask import render_template as template
from flask import redirect, url_for

from flask_login import current_user
from flask_classful import FlaskView

from app.models.ingredients import Ingredient
from app.models.users import User


class TrialRecipesView(FlaskView):
    def before_show(self):
        if current_user.is_authenticated:
            return redirect(url_for("IndexView:index"))

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
