# import math

from app.calc import calculations
from app.main.routes import calcRecipeAJAX
from app.models import Ingredient, Diet


def test_calc(app, client):
    # test both calculation.calculateRecipe and calcRecipeAJAX (json dataset)
    # 4

    diet = Diet.load_by_name("3.5")
    ingredients = [Ingredient.load_by_name("Brambory skladované"),
                   Ingredient.load_by_name("Filé z Aljašky"),
                   Ingredient.load_by_name("Máslo výběrové"),
                   Ingredient.load_by_name("Okurka salátová")]

    # calculations

    results = calculations.calculateRecipe(ingredients, diet)

    total_sugar = 0
    total_fat = 0
    total_protein = 0

    for ingredient in results:
        total_sugar += ingredient.sugar * ingredient.amount
        total_fat += ingredient.fat * ingredient.amount
        total_protein += ingredient.protein * ingredient.amount

    assert round(total_fat) == diet.fat
    assert round(total_sugar) == diet.sugar
    assert round(total_protein) == diet.protein

    # AJAX
    json_ingredients = []
    for ingredient in ingredients:
        ingredient.fixed = False
        ingredient.main = False
        json_ingredients.append(ingredient.json)

    test_dataset = {"ingredients": json_ingredients, "diet_id": diet.id}

    result = calcRecipeAJAX(test_dataset)

    assert round(result['sugar']) == diet.sugar
    assert round(result['fat']) == diet.fat
    assert round(result['protein']) == diet.protein

    # TODO 4 + fixed
    # assert calculations.calculateRecipe([
    #     Ingredient.load_by_name("Brambory skladované"),
    #     Ingredient.load_by_name("Česnek"),
    #     Ingredient.load_by_name("Cuketa"),
    #     Ingredient.load_by_name("Filé z Aljašky"),
    #     Ingredient.load_by_name("Kurkuma"),
    #     Ingredient.load_by_name("Máslo výběrové"),
    #     Ingredient.load_by_name("Okurka salátová")
    # ]) == 1
    # TODO too many / too few
    # TODO with no solution


# def test_recalc():
#     pass
