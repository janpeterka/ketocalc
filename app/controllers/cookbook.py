from app.models.recipes import Recipe

from flask import redirect, url_for, request

from flask_classful import route

# from flask import request

from flask_login import current_user

from app.data.texts import texts
from .extended_flask_view import ExtendedFlaskView
from .forms.cookbook_filter import CookbookFilterForm


class CookbookView(ExtendedFlaskView):
    template_folder = "cookbook"

    def before_index(self):
        if not current_user.is_authenticated:
            message = texts.cookbook.not_logged_in
            return redirect(url_for("CookbookView:not_logged_in", message=message))

        # page = request.args.get("page", 1, type=int)
        # self.recipe_pagination = Recipe.public_recipes_paginated(page, 30)
        # self.recipes = self.recipe_pagination.items
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

        if request.method == "POST":
            if not self.form.ingredient_name.data == "--všechny--":
                ingredient_name = self.form.ingredient_name.data
            ratio_from = self.form.ratio_from.data
            ratio_to = self.form.ratio_to.data

        # Filter recipes
        if ingredient_name:
            self.recipes = [
                x for x in self.recipes if ingredient_name in x.concat_ingredients
            ]

        if ratio_from:
            self.recipes = [x for x in self.recipes if x.ratio >= ratio_from]

        if ratio_to:
            self.recipes = [x for x in self.recipes if x.ratio <= ratio_to]

    @route("/", methods=["GET", "POST"])
    def index(self):
        return self.template()
