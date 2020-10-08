import json

from flask import jsonify, request, abort
from flask import render_template as template

from flask_classful import FlaskView, route
from flask_login import current_user

from app.helpers import calculations
from app.models.diets import Diet
from app.models.ingredients import Ingredient


class BaseRecipesView(FlaskView):
    @route("/addIngredientAJAX", methods=["POST"])
    def addIngredientAJAX(self):
        ingredient = Ingredient.load(request.json["ingredient_id"])
        if not ingredient.is_author(current_user) and not ingredient.public:
            abort(403)
        template_data = template(
            "recipes/_add_ingredient.html.j2", ingredient=ingredient
        )
        result = {"ingredient": ingredient.json, "template_data": template_data}
        return jsonify(result)

    @route("/addIngredientWithAmount", methods=["POST"])
    def addIngredientWithAmount(self):
        ingredient = Ingredient.load(request.json["ingredient_id"])
        if not ingredient.is_author(current_user) and not ingredient.public:
            abort(403)
        template_data = template(
            "recipes/_add_ingredient_with_amount.html.j2", ingredient=ingredient
        )
        result = {"ingredient": ingredient.json, "template_data": template_data}
        return jsonify(result)

    @route("/calcRecipeAJAX", methods=["POST"])
    def calcRecipeAJAX(self):
        json_ingredients = request.json["ingredients"]
        diet = Diet.load(request.json["dietID"])
        if "trial" in request.json and request.json["trial"] == "True":
            is_trialrecipe = True
        else:
            is_trialrecipe = False

        if diet is None:
            abort(400, "no diet")

        ingredients = []
        for json_i in json_ingredients:
            ingredient = Ingredient.load(json_i["id"])
            ingredient.fill_from_json(json_i)
            ingredients.append(ingredient)

        try:
            result = calculations.calculate_recipe(ingredients, diet)
        except Exception as e:
            abort(400, str(e.args[0]))

        ingredients = result["ingredients"]
        totals = result["totals"]

        json_ingredients = []
        for ing in ingredients:
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
        totals.amount = round(totals.amount * 100, 2)
        totals.ratio = round((totals.fat / (totals.protein + totals.sugar)), 2)

        template_data = template(
            "recipes/_right_form.html.j2",
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
