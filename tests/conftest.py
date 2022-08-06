import pytest

from app import create_app
from app import db as _db
from app.data import template_data

from tests.helpers import create_user


@pytest.fixture
def app(scope="session"):
    app = create_app(config_name="test")

    @app.context_processor
    def inject_globals():
        return dict(texts=template_data.texts)

    return app


@pytest.fixture
def db(app):
    # _db.init_app(app)
    # _db.drop_all()
    # _db.create_all()

    # insert default data
    with app.app_context():
        _db.drop_all()
        _db.create_all()

    db_fill_calc()

    return _db


def db_fill_calc():
    from tests.factories import DietFactory, IngredientFactory

    user = create_user(username="calc", password="calc_clack")
    user.save()

    DietFactory(name="3.5", calorie=0, sugar=10, fat=81, protein=13).save()

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
        IngredientFactory(**ingredient).save()
