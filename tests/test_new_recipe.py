# import math
import json

from app.main.routes import calculate_recipe_AJAX
from app.models import Ingredient, Diet

# def load_datasets_calc():
    # datasets = []


def test_calc(app, client):
    url = "/calcRecipeAJAX"
    # test calculate_recipe_AJAX (json dataset)
    # 4

    diet = Diet.load_by_name("3.5")
    ingredients = [
        Ingredient.load_by_name("Brambory skladované").set_main().json,
        Ingredient.load_by_name("Filé z Aljašky").json,
        Ingredient.load_by_name("Máslo výběrové").json,
        Ingredient.load_by_name("Okurka salátová").json
    ]
    test_dataset = {"ingredients": ingredients, "dietID": diet.id, "test": 'True'}

    result = calculate_recipe_AJAX(test_dataset)

    assert round(result['sugar']) == diet.sugar
    assert round(result['fat']) == diet.fat
    assert round(result['protein']) == diet.protein

    response = client.post(url, json=test_dataset)
    assert response == 200
    assert response.json is not None
    assert round(float(json.loads(response.json['totals'])['sugar'])) == diet.sugar
    assert round(float(json.loads(response.json['totals'])['fat'])) == diet.fat
    assert round(float(json.loads(response.json['totals'])['protein'])) == diet.protein

    # 4 + fixed
    diet = Diet.load_by_name("3.5")
    ingredients = [
        Ingredient.load_by_name("Brambory skladované").set_main().json,
        Ingredient.load_by_name("Filé z Aljašky").set_main(False).json,
        Ingredient.load_by_name("Máslo výběrové").set_main(False).json,
        Ingredient.load_by_name("Okurka salátová").set_main(False).json,

        Ingredient.load_by_name("Česnek").set_fixed(amount=0.5).set_main(False).json,
        Ingredient.load_by_name("Cuketa").set_fixed(amount=30).set_main(False).json,
        Ingredient.load_by_name("Kurkuma").set_fixed(amount=0.2).set_main(False).json
    ]
    test_dataset = {"ingredients": ingredients, "dietID": diet.id, "test": 'True'}

    result = calculate_recipe_AJAX(test_dataset)

    assert round(result['sugar']) == diet.sugar
    assert round(result['fat']) == diet.fat
    assert round(result['protein']) == diet.protein

    response = client.post(url, json=test_dataset)
    assert response == 200
    assert response is not None

    # too many / too few
    diet = Diet.load_by_name("3.5")
    ingredients = [
        Ingredient.load_by_name("Brambory skladované").json,
        Ingredient.load_by_name("Filé z Aljašky").json
    ]
    test_dataset = {"ingredients": ingredients, "dietID": diet.id, "test": 'True'}

    result = calculate_recipe_AJAX(test_dataset)
    assert result == 'False'

    response = client.post(url, json=test_dataset)
    assert response == 200
    assert response.json is None

    # with no solution
    diet = Diet.load_by_name("3.5")
    ingredients = [
        Ingredient.load_by_name("Brambory skladované").set_main().json,
        Ingredient.load_by_name("Filé z Aljašky").json,
        Ingredient.load_by_name("Okurka salátová").json,
        Ingredient.load_by_name("Kurkuma").json
    ]
    test_dataset = {"ingredients": ingredients, "dietID": diet.id, "test": 'True'}

    result = calculate_recipe_AJAX(test_dataset)
    assert result == 'False'

    response = client.post(url, json=test_dataset)
    assert response == 200
    assert response.json is None


# def test_recalc():
#     pass
