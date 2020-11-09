from app.models.recipes import Recipe

from flask import redirect, url_for, request

from flask_classful import route

# from flask import request

from flask_login import current_user

from app.data.texts import texts
from .extended_flask_view import ExtendedFlaskView
from .forms.cookbook_filter import CookbookFilterForm

from app.helpers.formaters import coma_to_float


class CookbookView(ExtendedFlaskView):
    template_folder = "cookbook"

    def before_index(self):
        if not current_user.is_authenticated:
            message = texts.cookbook.not_logged_in
            return redirect(url_for("CookbookView:not_logged_in", message=message))

        # Get filters from form/args
        ratio_from = coma_to_float(request.args.get("ratio_from", None))
        ratio_to = coma_to_float(request.args.get("ratio_to", None))

        if request.args.get("with_reaction", "n") == "y":
            with_reaction = True
        else:
            with_reaction = False

        if request.args.get("ingredient_name", "--všechny--") != "--všechny--":
            ingredient_name = request.args.get("ingredient_name", None)
        else:
            ingredient_name = None

        # page = request.args.get("page", 1, type=int)
        # self.recipe_pagination = Recipe.public_recipes_paginated(page, 30)
        # self.recipes = self.recipe_pagination.items
        self.recipes = Recipe.get_filtered_paginated_public_recipes(
            1,
            filters={
                "ratio_from": ratio_from,
                "ratio_to": ratio_to,
                "with_reaction": with_reaction,
            },
        )

        # Get values for filters
        ingredients = [x.ingredients for x in self.recipes]
        flatten_ingredients = [y for x in ingredients for y in x]
        ingredient_names = [x.name for x in flatten_ingredients]
        self.ingredient_names = ["--všechny--"]
        self.ingredient_names.extend(list(set(ingredient_names)))
        self.ingredient_names.sort()

        self.form = CookbookFilterForm(ingredient_names=self.ingredient_names)
        self.form.ratio_from.data = ratio_from
        self.form.ratio_to.data = ratio_to
        self.form.with_reaction.data = with_reaction
        self.form.ingredient_name.data = ingredient_name

        # Filter recipes
        if ingredient_name:
            self.recipes = [
                x for x in self.recipes if ingredient_name in x.concat_ingredients
            ]

        # if ratio_from:
        # self.recipes = [x for x in self.recipes if x.ratio >= ratio_from]

        # if ratio_to:
        # self.recipes = [x for x in self.recipes if x.ratio <= ratio_to]

        # if with_reaction:
        # self.recipes = [x for x in self.recipes if x.has_reaction]

    @route("/", methods=["GET", "POST"])
    def index(self):
        return self.template()
