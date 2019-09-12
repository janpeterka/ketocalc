import pytest

from app import create_app
from app import db as _db
from app.data import template_data

from app.models import Ingredient, Diet


@pytest.fixture
def app(scope="session"):
    app = create_app(config_name="test")

    @app.context_processor
    def inject_globals():
        return dict(icons=template_data.icons, texts=template_data.texts)

    return app


@pytest.fixture
def db(app):
    _db.drop_all()
    _db.create_all()

    # insert default data
    # calc
    db_fill_calc()

    return _db


def db_fill_calc():
    Diet(
        name="3.5",
        calorie=0,
        sugar=10,
        fat=81,
        protein=13,
        small_size=10,
        big_size=20,
        active=1,
    ).save()

    Ingredient(
        name="Brambory skladované",
        calorie=219,
        sugar=12.2,
        fat=0.1,
        protein=1.1,
        author="test",
    ).save()
    Ingredient(
        name="Česnek", calorie=366, sugar=21.8, fat=0.2, protein=5.4, author="test"
    ).save()
    Ingredient(
        name="Cuketa", calorie=57, sugar=1.8, fat=0.1, protein=0.8, author="test"
    ).save()
    Ingredient(
        name="Filé z Aljašky",
        calorie=352,
        sugar=0,
        fat=2.76,
        protein=14.7,
        author="test",
    ).save()
    Ingredient(
        name="Kurkuma", calorie=1435, sugar=65.9, fat=2.5, protein=10.8, author="test"
    ).save()
    Ingredient(
        name="Máslo výběrové",
        calorie=3056,
        sugar=0.6,
        fat=82,
        protein=0.7,
        author="test",
    ).save()
    Ingredient(
        name="Okurka salátová", calorie=54, sugar=2.1, fat=0.2, protein=1, author="test"
    ).save()
    # for do_register add_default_ingredients confirmation
    Ingredient(
        name="Default salátová",
        calorie=54,
        sugar=2.1,
        fat=0.2,
        protein=1,
        author="default",
    ).save()
    Ingredient(
        name="Okurka defaultová",
        calorie=54,
        sugar=2.1,
        fat=0.2,
        protein=1,
        author="default",
    ).save()
    Ingredient(
        name="Okurka salátová",
        calorie=54,
        sugar=2.1,
        fat=0.2,
        protein=1,
        author="default",
    ).save()
