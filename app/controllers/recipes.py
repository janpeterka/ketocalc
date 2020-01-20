from werkzeug import MultiDict

from flask import render_template as template
from flask import request, redirect, url_for, session
from flask import abort

from flask_login import login_required, current_user

from flask_classful import FlaskView, route

from app.models.recipes import Recipe
from app.models.diets import Diet

from app.calc import calculations


class RecipesView(FlaskView):
    decorators = [login_required]

    def before_request(self, name, id):
        if id is not None:
            self.recipe = Recipe.load(id)

            if self.recipe is None:
                abort(404)
            if current_user.username != self.recipe.author.username:
                abort(403)

    def index(self):
        user = User.load(current_user.id)
        return template("recipe/all.html.j2", diets=user.active_diets)

    def new(self):
        active_diets = User.load(current_user.id).active_diets
        ingredients = Ingredient.load_all_by_author(current_user.username)
        return template(
            "recipes/new.html.j2",
            ingredients=ingredients,
            diets=active_diets,
            is_trialrecipe=False,
        )

    def post(self):
        form_type = session["form_type"]
        session.pop("form_type")

        if form_type == "edit":
            recipe.name = request.form["name"]
            recipe.type = request.form["size"]
            recipe.edit()
            recipe.refresh()
            flash("Recept byl upraven.", "success")
            return redirect("/recipe={}".format(recipe_id))

    def show(self, id):
        if application.config["APP_STATE"] == "production":
            if recipe.view_count is not None:
                recipe.view_count += 1
            else:
                recipe.view_count = 1
            recipe.edit()

        return template(
            "recipe/show.html.j2", recipe=recipe, totals=recipe.totals, is_print=False,
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
        return template("recipe/print_all.html.j2", recipes=recipes)

    def edit(self, id):
        session["form_type"] = "edit"
        return template("recipes/edit.html.j2", recipe=recipe, totals=recipe.totals)

    def delete(self, id):
        recipe.remove()
        flash("Recept byl smazán.", "success")
        return redirect(url_for("DashboardView:show"))

    @route("/addIngredientAJAX", methods=["POST"])
    def add_ingredient_to_recipe_AJAX():
        ingredient = Ingredient.load(request.json["ingredient_id"])
        template_data = template(
            "recipes/_add_ingredient.html.j2", ingredient=ingredient
        )
        result = {"ingredient": ingredient.json, "template_data": template_data}
        return jsonify(result)

    @route("/calcRecipeAJAX", methods=["POST"])
    def calculate_recipe_AJAX():

        json_ingredients = request.json["ingredients"]
        diet = Diet.load(request.json["dietID"])
        if "trial" in request.json and request.json["trial"] == "True":
            is_trialrecipe = True
        else:
            is_trialrecipe = False

        if diet is None:
            return "False"

        ingredients = []
        for json_i in json_ingredients:
            ingredient = Ingredient.load(json_i["id"])
            ingredient.fill_from_json(json_i)
            ingredients.append(ingredient)

        result = calculations.calculate_recipe(ingredients, diet)
        if result is None:
            return "False"

        ingredients = result["ingredients"]
        totals = result["totals"]

        json_ingredients = []
        for ing in ingredients:
            if ing.amount < 0:
                return "False"

            ing.calorie = round(ing.calorie * ing.amount, 2)
            ing.fat = round(ing.fat, 2)
            ing.sugar = round(ing.sugar, 2)
            ing.protein = round(ing.protein, 2)
            ing.amount = round(ing.amount * 100, 2)

            json_ingredients.append(ing.json)

        totals.calorie = round(totals.calorie, 2)
        totals.sugar = round(totals.sugar, 2)
        totals.fat = round(totals.fat, 2)
        totals.protein = round(totals.protein, 2)
        totals.amount = round(totals.amount, 2)
        totals.ratio = round((totals.fat / (totals.protein + totals.sugar)), 2)

        template_data = template(
            "recipe/_right_form.html.j2",
            ingredients=ingredients,
            totals=totals,
            diet=diet,
            is_trialrecipe=is_trialrecipe,
        )

        result = {
            "template_data": str(template_data),
            "totals": json.dumps(totals.__dict__),
            "ingredients": json_ingredients,
            "diet": diet.json,
        }

        # reset ingredients (so they are not changed in db)
        for ing in ingredients:
            ing.expire()

        return jsonify(result)

    @route("/saveRecipeAJAX", methods=["POST"])
    def saveRecipeAJAX():
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
        flash("Recept byl uložen", "success")
        return "/recipe=" + str(last_id)
