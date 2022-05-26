from flask import render_template as template
from flask import request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from flask_classful import route

from app.auth import admin_required

from app.models import Recipe, Diet, User, Ingredient, RecipeHasIngredient

from app.controllers.base_recipes import BaseRecipeView


class RecipeView(BaseRecipeView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None, **kwargs):
        self.recipe = Recipe.load(id)

    def before_show(self, id):
        self.validate_show(self.recipe)

    def before_edit(self, id):
        self.validate_edit(self.recipe)

    def before_update(self, id):
        self.validate_update(self.recipe)

    def index(self):
        self.diets = current_user.active_diets

        return self.template()

    def new(self):
        from app.helpers.general import list_without_duplicated

        active_diets = current_user.active_diets
        user_ingredients = Ingredient.load_all_by_author(current_user.username)
        shared_ingredients = Ingredient.load_all_shared(renamed=True)

        ingredients = user_ingredients + shared_ingredients
        self.ingredients = list_without_duplicated(ingredients)

        self.preset_ingredients = request.args.get("preset_ingredient_ids", [])
        self.diets = active_diets
        self.is_trialrecipe = False

        return self.template()

    def post(self):
        # TODO: implemented with ajax now, will change
        pass

    def show(self, id):
        from app.forms import PhotoForm

        self.is_print = False
        self.photo_form = PhotoForm()

        return self.template()

    def edit(self, id):
        return self.template()

    @route("update/<id>", methods=["POST"])
    def update(self, id):
        self.recipe.name = request.form["name"]
        self.recipe.description = request.form["description"]
        self.recipe.edit()
        self.recipe.refresh()
        flash("Recept byl upraven.", "success")

        return redirect(url_for("RecipeView:show", id=self.recipe.id))

    @route("/delete/<id>", methods=["POST"])
    def delete(self, id):
        self.recipe.remove()
        flash("Recept byl smazán.", "success")

        return redirect(url_for("DashboardView:index"))

    def print(self, id):
        return template(
            "recipes/show.html.j2",
            recipe=self.recipe,
            is_print=True,
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
        from app.forms.files import PhotoForm

        from app.models import RecipeImageFile

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
