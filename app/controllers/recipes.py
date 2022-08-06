from flask import request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from flask_classful import route

from app.auth import admin_required
from app.helpers.general import list_without_duplicated
from app.models import Recipe, Diet, User, Ingredient
from app.forms import PhotoForm
from app.helpers.base_view import BaseView
from app.services import RecipeReactionManager, RecipeSharer


class RecipeView(BaseView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None, **kwargs):
        self.recipe = Recipe.load(id)

    def before_show(self, id):
        self.validate_show(self.recipe)

    def before_edit(self, id):
        self.validate_edit(self.recipe)

    def before_update(self, id):
        self.validate_edit(self.recipe)

    def index(self):
        return self.template()

    def new(self):
        active_diets = current_user.active_diets
        user_ingredients = Ingredient.load_all_by_author(current_user.username)
        shared_ingredients = Ingredient.load_all_shared(renamed=True)

        ingredients = user_ingredients + shared_ingredients
        self.ingredients = list_without_duplicated(ingredients)

        self.preset_ingredients = request.args.get("preset_ingredient_ids", [])
        print(self.preset_ingredients)
        self.diets = active_diets
        self.is_trialrecipe = False

        return self.template()

    def post(self):
        # TODO: implemented with ajax now, will change
        pass

    def show(self, id):
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
        return self.template("show", is_print=True)

    @route("/toggle_shared/<id>", methods=["POST"])
    def toggle_shared(self, id):
        toggled = RecipeSharer(self.recipe).toggle_shared()
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
        from app.services import RecipeCreator

        temp_ingredients = request.json["ingredients"]
        diet = Diet.load(request.json["dietID"])
        name = request.json["name"]

        recipe = RecipeCreator.create(
            name=name, diet=diet, ingredient_dict=temp_ingredients
        )

        return url_for("RecipeView:show", id=recipe.id)

    @route("/toggleReactionAJAX", methods=["POST"])
    def toggle_reaction_AJAX(self):
        recipe = Recipe.load(request.json["recipe_id"])
        RecipeReactionManager(recipe).toggle_reaction()

        return jsonify(recipe.has_reaction_by_current_user)

    @route("/upload_photo/<id>", methods=["POST"])
    def upload_photo(self, id):
        from werkzeug.datastructures import CombinedMultiDict
        from app.forms import PhotoForm
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
