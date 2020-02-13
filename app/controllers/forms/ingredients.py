from wtforms import StringField, SubmitField
from wtforms import validators

from flask_wtf import FlaskForm

from app.controllers.forms.custom import ComaFloatField


class IngredientsForm(FlaskForm):
    name = StringField(
        "Název suroviny", [validators.InputRequired("Název musí být vyplněn")]
    )
    protein = ComaFloatField(
        "Množství bílkovin / 100 g",
        [
            validators.InputRequired("Množství musí být vyplněno"),
            validators.NumberRange(0, 100, "Musí být mezi 0 a 100"),
        ],
    )
    sugar = ComaFloatField(
        "Množství sacharidů / 100 g",
        [
            validators.InputRequired("Množství musí být vyplněno"),
            validators.NumberRange(0, 100, "Musí být mezi 0 a 100"),
        ],
    )
    fat = ComaFloatField(
        "Množství tuku / 100 g",
        [
            validators.InputRequired("Množství musí být vyplněno"),
            validators.NumberRange(0, 100, "Musí být mezi 0 a 100"),
        ],
    )
    calorie = ComaFloatField(
        "Energie (kJ) / 100 g", [validators.InputRequired("Množství musí být vyplněno")]
    )
    submit = SubmitField("Přidat surovinu")
