# import math

# from app.calc import calculations
from app.main.routes import calcRecipeAJAX
from app.models import Ingredient, Diet


def test_calc(app, client):
    # test calcRecipeAJAX (json dataset)
    # 4

    diet = Diet.load_by_name("3.5")
    ingredients = [Ingredient.load_by_name("Brambory skladované"),
                   Ingredient.load_by_name("Filé z Aljašky"),
                   Ingredient.load_by_name("Máslo výběrové"),
                   Ingredient.load_by_name("Okurka salátová")]

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

    # 4 + fixed
    diet = Diet.load_by_name("3.5")
    ingredients = [
        Ingredient.load_by_name("Brambory skladované").set_main(),
        Ingredient.load_by_name("Filé z Aljašky").set_main(False),
        Ingredient.load_by_name("Máslo výběrové").set_main(False),
        Ingredient.load_by_name("Okurka salátová").set_main(False),

        Ingredient.load_by_name("Česnek").set_fixed(amount=0.5).set_main(False),
        Ingredient.load_by_name("Cuketa").set_fixed(amount=30).set_main(False),
        Ingredient.load_by_name("Kurkuma").set_fixed(amount=0.2).set_main(False)
    ]

    json_ingredients = []
    for ingredient in ingredients:
        json_ingredients.append(ingredient.json)

    test_dataset = {"ingredients": json_ingredients, "diet_id": diet.id}

    result = calcRecipeAJAX(test_dataset)

    assert round(result['sugar']) == diet.sugar
    assert round(result['fat']) == diet.fat
    assert round(result['protein']) == diet.protein

    # TODO too many / too few
    diet = Diet.load_by_name("3.5")
    ingredients = [
        Ingredient.load_by_name("Brambory skladované"),
        Ingredient.load_by_name("Filé z Aljašky")
    ]

    json_ingredients = []
    for ingredient in ingredients:
        ingredient.fixed = False
        ingredient.main = False
        json_ingredients.append(ingredient.json)

    test_dataset = {"ingredients": json_ingredients, "diet_id": diet.id}

    result = calcRecipeAJAX(test_dataset)

    assert result == 'False'

    # TODO with no solution


# def test_recalc():
#     pass
