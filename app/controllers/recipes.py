from flask import render_template as template
from flask import request, redirect, url_for, flash, abort, g

from flask_login import login_required, current_user

from flask_classful import route

from app.models.recipes import Recipe
from app.models.diets import Diet
from app.models.ingredients import Ingredient
from app.models.recipes_has_ingredients import RecipeHasIngredients
from app.controllers.base_recipes import BaseRecipesView


class RecipesView(BaseRecipesView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None):
        g.request_item_type = "recipe"
        if id is not None:
            g.request_item_id = id
            self.recipe = Recipe.load(id)

            if self.recipe is None:
                abort(404)
            if not (
                current_user.username == self.recipe.author.username
                or current_user.is_admin
                or self.recipe.public
            ):
                abort(403)

    def index(self):
        return template("recipes/all.html.j2", diets=current_user.active_diets)

    def new(self):
        active_diets = current_user.active_diets
        ingredients = Ingredient.load_all_by_author(current_user.username)
        shared_ingredients = Ingredient.load_all_shared(renamed=True)

        # TODO - this couses duplication for admin. shouldn't be problem for users.
        all_ingredients = ingredients + shared_ingredients
        return template(
            "recipes/new.html.j2",
            ingredients=all_ingredients,
            diets=active_diets,
            is_trialrecipe=False,
        )

    def post(self):
        # TODO: implemented with ajax now, will change
        pass

    @route("<id>/edit", methods=["POST"])
    def post_edit(self, id):
        self.recipe.name = request.form["name"]
        self.recipe.edit()
        self.recipe.refresh()
        flash("Recept byl upraven.", "success")
        return redirect(url_for("RecipesView:show", id=self.recipe.id))

    def show(self, id):
        from .forms.files import PhotoForm

        return template(
            "recipes/show.html.j2",
            recipe=self.recipe,
            is_print=False,
            photo_form=PhotoForm(),
        )

    def print(self, id):
        return template("recipes/show.html.j2", recipe=self.recipe, is_print=True,)

    def print_all(self, diet_id=None):
        if diet_id is None:
            recipes = current_user.recipes
        else:
            recipes = Diet.load(diet_id).recipes

        return template("recipes/print_all.html.j2", recipes=recipes)

    def edit(self, id):
        return template(
            "recipes/edit.html.j2", recipe=self.recipe, totals=self.recipe.totals
        )

    @route("/toggle_shared/<id>", methods=["POST"])
    def toggle_shared(self, id):
        toggled = self.recipe.toggle_shared()
        if toggled is True:
            flash("Recept byl zveřejněn.", "success")
        else:
            flash("Recept byl skryt před veřejností.", "success")
        return redirect(url_for("RecipesView:show", id=self.recipe.id))

    @route("/make_all_recipes_public")
    def make_all_public(self):
        for recipe in current_user.recipes:
            recipe.is_shared = True
            recipe.save()
        flash("Všechny Vaše recepty byly zveřejněny", "success")
        return redirect(url_for("DashboardView:index"))

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
            rhi = RecipeHasIngredients()
            rhi.ingredients_id = temp_i["id"]
            rhi.amount = temp_i["amount"]
            ingredients.append(rhi)

        recipe = Recipe()
        recipe.name = request.json["name"]
        recipe.diet = Diet.load(diet_id)

        last_id = recipe.create_and_save(ingredients)
        return url_for("RecipesView:show", id=last_id)

    @route("/upload_photo/<id>", methods=["POST"])
    def upload_photo(self, id):
        from werkzeug.datastructures import CombinedMultiDict
        from .forms.files import PhotoForm

        from app.models.files import RecipeImageFile

        form = PhotoForm(CombinedMultiDict((request.files, request.form)))

        if form.file.data:
            file = RecipeImageFile()
            file.data = form.file.data
            file.recipe_id = id
            file.save()

        return redirect(url_for("RecipesView:show", id=id))
