import json

from flask import render_template as template
from flask import jsonify, request, abort

from flask_classful import FlaskView, route

from app.models.ingredients import Ingredient
from app.models.diets import Diet

from app.helpers import calculations


class BaseRecipesView(FlaskView):
    @route("/addIngredientAJAX", methods=["POST"])
    def addIngredientAJAX(self):
        print("add_ingredient")
        print(request.json)
        ingredient = Ingredient.load(request.json["ingredient_id"])
        template_data = template(
            "recipes/_add_ingredient.html.j2", ingredient=ingredient
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

        result = calculations.calculate_recipe(ingredients, diet)
        if result is None:
            abort(400, "cannot be calculated")

        ingredients = result["ingredients"]
        totals = result["totals"]

        json_ingredients = []
        for ing in ingredients:
            if ing.amount < 0:
                abort(400, "ingredient with negative amount")

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
