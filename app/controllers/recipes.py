from flask import render_template as template
from flask import request, redirect, url_for, flash, abort, g, jsonify
from flask_login import login_required, current_user
from flask_classful import route

from app.auth import admin_required

from app.models import Recipe, Diet, User, Ingredient, RecipeHasIngredient

from app.controllers.base_recipes import BaseRecipeView


class RecipeView(BaseRecipeView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None, **kwargs):
        g.request_item_type = "recipe"
        if id is not None:
            g.request_item_id = id
            self.recipe = Recipe.load(id)

            if self.recipe is None:
                abort(404)
            if not self.recipe.can_current_user_show:
                abort(403)

    def index(self):
        self.diets = current_user.active_diets

        return template("recipes/index.html.j2", diets=self.diets)

    def new(self):
        active_diets = current_user.active_diets
        ingredients = Ingredient.load_all_by_author(current_user.username)
        shared_ingredients = Ingredient.load_all_shared(renamed=True)

        # TODO - this causes duplication for admin. shouldn't be problem for users.
        all_ingredients = ingredients + shared_ingredients
        return template(
            "recipes/new.html.j2",
            ingredients=all_ingredients,
            preset_ingredients=request.args.get("preset_ingredient_ids", []),
            diets=active_diets,
            is_trialrecipe=False,
        )

    def post(self):
        # TODO: implemented with ajax now, will change
        pass

    @route("update/<id>", methods=["POST"])
    def post_edit(self, id):
        self.recipe.name = request.form["name"]
        self.recipe.description = request.form["description"]
        self.recipe.edit()
        self.recipe.refresh()
        flash("Recept byl upraven.", "success")
        return redirect(url_for("RecipeView:show", id=self.recipe.id))

    def show(self, id):
        from .forms.files import PhotoForm

        return template(
            "recipes/show.html.j2",
            recipe=self.recipe,
            is_print=False,
            photo_form=PhotoForm(),
        )

    def print(self, id):
        return template(
            "recipes/show.html.j2",
            recipe=self.recipe,
            is_print=True,
        )

    # def print_all(self, diet_id=None):
    #     if diet_id is None:
    #         recipes = current_user.recipes
    #     else:
    #         recipes = Diet.load(diet_id).recipes

    #     return template("recipes/print_all.html.j2", recipes=recipes)

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
        return redirect(url_for("RecipeView:show", id=self.recipe.id))

    @route("/make_all_recipes_public")
    def make_all_public(self):
        for recipe in current_user.recipes:
            recipe.is_shared = True
            recipe.save()
        flash("Všechny Vaše recepty byly zveřejněny", "success")
        return redirect(url_for("DashboardView:index"))

    @admin_required
    @route("/make_all_recipes_public/user=<user_id>")
    def make_all_public_for_user(self, user_id):
        if user_id is not None:
            user = User.load(user_id)
        else:
            flash("No user", "error")

        for recipe in user.recipes:
            recipe.is_shared = True
            recipe.save()
        flash(f"Všechny recepty uživatele {user.full_name} byly zveřejněny", "success")
        return redirect(url_for("DashboardView:index"))

    @route("/delete/<id>", methods=["POST"])
    def delete(self, id):
        self.recipe.remove()
        flash("Recept byl smazán.", "success")
        return redirect(url_for("DashboardView:index"))

    @route("/saveRecipeAJAX", methods=["POST"])
    def saveRecipeAJAX(self):
        temp_ingredients = request.json["ingredients"]
        diet = Diet.load(request.json["dietID"])

        ingredients = []
        for temp_i in temp_ingredients:
            rhi = RecipeHasIngredient()
            rhi.ingredients_id = temp_i["id"]
            rhi.amount = temp_i["amount"]
            ingredients.append(rhi)

        recipe = Recipe(name=request.json["name"], diet=diet)

        last_id = recipe.create_and_save(ingredients)
        return url_for("RecipeView:show", id=last_id)

    @route("/toggleReactionAJAX", methods=["POST"])
    def toggle_reaction_AJAX(self):
        recipe = Recipe.load(request.json["recipe_id"])
        recipe.toggle_reaction()
        return jsonify(recipe.has_reaction)

    @route("/upload_photo/<id>", methods=["POST"])
    def upload_photo(self, id):
        from werkzeug.datastructures import CombinedMultiDict
        from .forms.files import PhotoForm

        from app.models.files import RecipeImageFile

        form = PhotoForm(CombinedMultiDict((request.files, request.form)))

        if form.file.data:
            file = RecipeImageFile(recipe_id=id)
            file.data = form.file.data
            file.save()

        return redirect(url_for("RecipeView:show", id=id))

    @route("/load_recipes_AJAX", methods=["POST"])
    # @login_required
    def load_recipes_AJAX(self):
        diet_id = request.json["diet_id"]
        if diet_id is None:
            return ("", 204)

        diet = Diet.load(diet_id)

        if diet is None:
            abort(404)
        if not diet.can_current_user_view:
            abort(403)

        json_recipes = [recipe.json for recipe in diet.recipes]

        return jsonify(json_recipes)
