import json

from flask import jsonify, request, abort
from flask import render_template as template
from flask_classful import route
from app.helpers.base_view import BaseView

from app.helpers import calculations
from app.handlers.data import DataHandler
from app.models.diets import Diet
from app.models.ingredients import Ingredient


class BaseRecipeView(BaseView):
    @route("/addIngredientAJAX", methods=["POST"])
    def addIngredientAJAX(self):
        ingredient = Ingredient.load(request.json["ingredient_id"])
        if not ingredient:
            abort(404)
        if not (ingredient.can_current_user_add or ingredient.can_current_user_copy):
            abort(403)
        template_data = template(
            "recipes/_add_ingredient.html.j2", ingredient=ingredient
        )
        result = {"ingredient": ingredient.json, "template_data": template_data}

        DataHandler.set_additional_request_data(
            item_type="add_ingredient_AJAX", item_id=ingredient.id
        )
        return jsonify(result)

    @route("/addIngredientWithAmount", methods=["POST"])
    def addIngredientWithAmount(self):
        ingredient = Ingredient.load(request.json["ingredient_id"])
        if not ingredient:
            abort(404)
        if not ingredient.can_current_user_add:
            abort(403)
        template_data = template(
            "recipes/_add_ingredient_with_amount.html.j2", ingredient=ingredient
        )
        result = {"ingredient": ingredient.json, "template_data": template_data}
        DataHandler.set_additional_request_data(
            item_type="add_ingredient_with_amount_AJAX", item_id=ingredient.id
        )
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
            if not ingredient.can_current_user_add:
                return ("Tuto surovinu nemůžete použít", 403)
            ingredient.fill_from_json(json_i)
            ingredients.append(ingredient)

        try:
            result = calculations.calculate_recipe(ingredients, diet)
        except ValueError:
            return ("Recept nelze vytvořit", 204)

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

        DataHandler.set_additional_request_data(
            item_type="calculate_recipe_AJAX", item_id=ingredient.id
        )
        return jsonify(result)
