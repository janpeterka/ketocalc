from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, FloatField
from wtforms import validators

from app.controllers.forms.custom import MyFloatField


class NewIngredientsForm(FlaskForm):
    name = StringField(
        "Název suroviny", [validators.InputRequired("Název musí být vyplněn")]
    )
    protein = MyFloatField(
        "Množství bílkovin / 100 g",
        [
            validators.InputRequired("Množství musí být vyplněno"),
            validators.NumberRange(0, 100, "Musí být mezi 0 a 100"),
        ],
    )
    sugar = MyFloatField(
        "Množství sacharidů / 100 g",
        [
            validators.InputRequired("Množství musí být vyplněno"),
            validators.NumberRange(0, 100, "Musí být mezi 0 a 100"),
        ],
    )
    fat = MyFloatField(
        "Množství tuku / 100 g",
        [
            validators.InputRequired("Množství musí být vyplněno"),
            validators.NumberRange(0, 100, "Musí být mezi 0 a 100"),
        ],
    )
    calorie = MyFloatField(
        "Energie (kJ) / 100 g", [validators.InputRequired("Množství musí být vyplněno")]
    )
    submit = SubmitField("Přidat surovinu")
