import pytest

from app import create_app
from app import db as _db
from app.data import template_data

from app.models.ingredients import Ingredient
from app.models.diets import Diet

from tests.unit.helpers import create_user


@pytest.fixture
def app(scope="session"):
    app = create_app(config_name="test")

    @app.context_processor
    def inject_globals():
        return dict(
            icons=template_data.icons,
            social_icons=template_data.social_icons,
            texts=template_data.texts,
        )

    return app


@pytest.fixture
def db(app):
    # _db.init_app(app)
    # _db.drop_all()
    # _db.create_all()

    # insert default data
    with app.app_context():
        # _db.drop_all()
        _db.create_all()

    db_fill_calc()

    return _db


def db_fill_calc():
    user = create_user(username="calc", password="calc_clack")
    user.save()

    diets = [
        {
            "name": "3.5",
            "calorie": 0,
            "sugar": 10,
            "fat": 81,
            "protein": 13,
            "active": 1,
            "user_id": 1,
        }
    ]

    for diet in diets:
        Diet(
            name=diet["name"],
            calorie=diet["calorie"],
            sugar=diet["sugar"],
            fat=diet["fat"],
            protein=diet["protein"],
            active=diet["active"],
            user_id=diet["user_id"],
        ).save()

    ingredients = [
        {
            "name": "Brambory skladované",
            "calorie": 219,
            "sugar": 12.2,
            "fat": 0.1,
            "protein": 1.1,
            "author": "calc",
        },
        {
            "name": "Česnek",
            "calorie": 366,
            "sugar": 21.8,
            "fat": 0.2,
            "protein": 5.4,
            "author": "calc",
        },
        {
            "name": "Cuketa",
            "calorie": 57,
            "sugar": 1.8,
            "fat": 0.1,
            "protein": 0.8,
            "author": "calc",
        },
        {
            "name": "Filé z Aljašky",
            "calorie": 352,
            "sugar": 0,
            "fat": 2.76,
            "protein": 14.7,
            "author": "calc",
        },
        {
            "name": "Kurkuma",
            "calorie": 1435,
            "sugar": 65.9,
            "fat": 2.5,
            "protein": 10.8,
            "author": "calc",
        },
        {
            "name": "Máslo výběrové",
            "calorie": 3056,
            "sugar": 0.6,
            "fat": 82,
            "protein": 0.7,
            "author": "calc",
        },
        {
            "name": "Okurka salátová",
            "calorie": 54,
            "sugar": 2.1,
            "fat": 0.2,
            "protein": 1,
            "author": "calc",
        },
        # for do_register add_default_ingredients confirmation
        {
            "name": "Default salátová",
            "calorie": 100,
            "sugar": 2.1,
            "fat": 0.2,
            "protein": 1,
            "author": "default",
            "is_shared": True,
            "is_approved": True,
        },
        {
            "name": "Okurka defaultová",
            "calorie": 54,
            "sugar": 100,
            "fat": 0.2,
            "protein": 1,
            "author": "default",
            "is_shared": True,
            "is_approved": True,
        },
        {
            "name": "Okurka salátová",
            "calorie": 54,
            "sugar": 2.1,
            "fat": 100,
            "protein": 1,
            "author": "default",
            "is_shared": True,
            "is_approved": True,
        },
    ]

    for ingredient in ingredients:
        Ingredient(
            name=ingredient["name"],
            calorie=ingredient["calorie"],
            sugar=ingredient["sugar"],
            fat=ingredient["fat"],
            protein=ingredient["protein"],
            author=ingredient["author"],
            is_shared=getattr(ingredient, "is_shared", None),
            is_approved=getattr(ingredient, "is_approved", None),
        ).save()
