from flask import redirect, url_for, request
from flask_classful import route
from flask_login import current_user

from app.helpers.base_view import BaseView

from app.models import Recipe

from app.controllers.forms import CookbookFilterForm


class CookbookView(BaseView):
    template_folder = "cookbook"

    def before_request(self, name):
        if name == "index" and not current_user.is_authenticated:
            return redirect(url_for("CookbookView:public_index"))

        self.recipes = Recipe.public_recipes()
        # Get values for filters
        ingredients = [x.ingredients for x in self.recipes]
        flatten_ingredients = [y for x in ingredients for y in x]
        ingredient_names = [x.name for x in flatten_ingredients]
        self.ingredient_names = ["--všechny--"]
        self.ingredient_names.extend(list(set(ingredient_names)))
        self.ingredient_names.sort()

        if request.method == "GET":
            self.form = CookbookFilterForm(ingredient_names=self.ingredient_names)
        else:
            self.form = CookbookFilterForm(
                request.form, ingredient_names=self.ingredient_names
            )

        # Get filters from request
        ingredient_name = None
        ratio_from = None
        ratio_to = None
        with_reaction = None

        if request.method == "POST":
            if not self.form.ingredient_name.data == "--všechny--":
                ingredient_name = self.form.ingredient_name.data
            ratio_from = self.form.ratio_from.data
            ratio_to = self.form.ratio_to.data
            with_reaction = self.form.with_reaction.data

        # Filter recipes
        if ingredient_name:
            self.recipes = [
                x for x in self.recipes if ingredient_name in x.concat_ingredients
            ]

        if ratio_from:
            self.recipes = [x for x in self.recipes if x.ratio >= ratio_from]

        if ratio_to:
            self.recipes = [x for x in self.recipes if x.ratio <= ratio_to]

        if with_reaction:
            self.recipes = [x for x in self.recipes if x.has_reaction]

    @route("/", methods=["GET", "POST"])
    def index(self):
        return self.template()

    @route("/public", methods=["GET", "POST"])
    def public_index(self):
        return self.template(template_name="cookbook/index.html.j2", public=True)
