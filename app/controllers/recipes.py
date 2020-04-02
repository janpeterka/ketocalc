from flask import render_template as template
from flask import request, redirect, url_for, flash, abort

from flask_login import login_required, current_user

from flask_classful import route

from app.models.recipes import Recipe
from app.models.diets import Diet
from app.models.users import User
from app.models.ingredients import Ingredient
from app.models.recipes_has_ingredients import RecipesHasIngredient
from app.controllers.base_recipes import BaseRecipesView


class RecipesView(BaseRecipesView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None):
        if id is not None:
            self.recipe = Recipe.load(id)

            if self.recipe is None:
                abort(404)
            if current_user.username != self.recipe.author.username:
                abort(403)

    def index(self):
        user = User.load(current_user.id)
        return template("recipes/all.html.j2", diets=user.active_diets)

    def new(self):
        active_diets = User.load(current_user.id).active_diets
        ingredients = Ingredient.load_all_by_author(current_user.username)
        shared_ingredients = Ingredient.load_all_shared(renamed=True)

        all_ingredients = ingredients + shared_ingredients
        return template(
            "recipes/new.html.j2",
            ingredients=all_ingredients,
            diets=active_diets,
            is_trialrecipe=False,
        )

    def post(self):
        # TODO: implemented with ajax not, will change
        pass

    @route("<id>/edit", methods=["POST"])
    def post_edit(self, id):
        self.recipe.name = request.form["name"]
        self.recipe.type = request.form["size"]
        self.recipe.edit()
        self.recipe.refresh()
        flash("Recept byl upraven.", "success")
        return redirect(url_for("RecipesView:show", id=self.recipe.id))

    def show(self, id):
        self.recipe.log_view()

        return template(
            "recipes/show.html.j2",
            recipe=self.recipe,
            totals=self.recipe.totals,
            is_print=False,
        )

    def print(self, id):
        return template(
            "recipes/show.html.j2",
            recipe=self.recipe,
            totals=self.recipe.totals,
            is_print=True,
        )

    def print_all(self, diet_id=None):
        if diet_id is None:
            recipes = User.load(current_user.id).recipes
        else:
            recipes = Diet.load(diet_id).recipes

        for recipe in recipes:
            recipe_data = recipe.load_recipe_for_show()
            recipe.show_totals = recipe_data["totals"]
        return template("recipes/print_all.html.j2", recipes=recipes)

    def edit(self, id):
        return template(
            "recipes/edit.html.j2", recipe=self.recipe, totals=self.recipe.totals
        )

    @route("/delete/<id>", methods=["POST"])
    def delete(self, id):
        self.recipe.remove()
        flash("Recept byl smazán.", "success")
        return redirect(url_for("DashboardView:show"))

    @route("/saveRecipeAJAX", methods=["POST"])
    def saveRecipeAJAX(self):
        temp_ingredients = request.json["ingredients"]
        diet_id = request.json["dietID"]

        ingredients = []
        for temp_i in temp_ingredients:
            rhi = RecipesHasIngredient()
            rhi.ingredients_id = temp_i["id"]
            rhi.amount = temp_i["amount"]
            ingredients.append(rhi)

        recipe = Recipe()
        recipe.name = request.json["name"]
        recipe.type = request.json["size"]
        recipe.diet = Diet.load(diet_id)

        last_id = recipe.save(ingredients)
        return url_for("RecipesView:show", id=last_id)
