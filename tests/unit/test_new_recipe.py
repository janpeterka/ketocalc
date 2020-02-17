import json

from app.models.ingredients import Ingredient
from app.models.diets import Diet

from flask import url_for

import helpers


def load_datasets_calc():
    datasets = []

    # 4
    diet = Diet.load_by_name("3.5")
    ingredients = [
        Ingredient.load_by_name("Brambory skladované").set_main().json,
        Ingredient.load_by_name("Filé z Aljašky").json,
        Ingredient.load_by_name("Máslo výběrové").json,
        Ingredient.load_by_name("Okurka salátová").json,
    ]
    test_dataset = {
        "ingredients": ingredients,
        "dietID": diet.id,
        "diet": diet.json,
        "none": "False",
    }
    datasets.append(test_dataset)

    # 4 + fixed
    diet = Diet.load_by_name("3.5")
    ingredients = [
        Ingredient.load_by_name("Brambory skladované").set_main().json,
        Ingredient.load_by_name("Filé z Aljašky").set_main(False).json,
        Ingredient.load_by_name("Máslo výběrové").set_main(False).json,
        Ingredient.load_by_name("Okurka salátová").set_main(False).json,
        Ingredient.load_by_name("Česnek").set_fixed(amount=0.5).set_main(False).json,
        Ingredient.load_by_name("Cuketa").set_fixed(amount=30).set_main(False).json,
        Ingredient.load_by_name("Kurkuma").set_fixed(amount=0.2).set_main(False).json,
    ]
    test_dataset = {
        "ingredients": ingredients,
        "dietID": diet.id,
        "diet": diet.json,
        "none": "False",
    }
    datasets.append(test_dataset)

    # too many / too few
    diet = Diet.load_by_name("3.5")
    ingredients = [
        Ingredient.load_by_name("Brambory skladované").json,
        Ingredient.load_by_name("Filé z Aljašky").json,
    ]
    test_dataset = {
        "ingredients": ingredients,
        "dietID": diet.id,
        "diet": diet.json,
        "none": "True",
    }
    datasets.append(test_dataset)

    # with no solution
    diet = Diet.load_by_name("3.5")
    ingredients = [
        Ingredient.load_by_name("Brambory skladované").set_main().json,
        Ingredient.load_by_name("Filé z Aljašky").json,
        Ingredient.load_by_name("Okurka salátová").json,
        Ingredient.load_by_name("Kurkuma").json,
    ]
    test_dataset = {
        "ingredients": ingredients,
        "dietID": diet.id,
        "diet": diet.json,
        "none": "True",
    }
    datasets.append(test_dataset)

    return datasets


def test_calc(app, db, client):
    url = url_for("RecipesView:calcRecipeAJAX")
    # test calculate_recipe_AJAX (json dataset)

    datasets = load_datasets_calc()

    helpers.test_with_authenticated_user(app)

    for dataset in datasets:
        response = client.post(url, json=dataset, follow_redirects=False)

        assert response == 200
        if dataset["none"] == "True":
            assert response.json is None
            pass
        else:
            assert response.json is not None
            assert (
                round(float(json.loads(response.json["totals"])["sugar"]))
                == dataset["diet"]["sugar"]
            )
            assert (
                round(float(json.loads(response.json["totals"])["fat"]))
                == dataset["diet"]["fat"]
            )
            assert (
                round(float(json.loads(response.json["totals"])["protein"]))
                == dataset["diet"]["protein"]
            )

    client.get("/logout")


# def test_recalc():
#     pass
