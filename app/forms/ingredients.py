from wtforms import StringField, SubmitField
from wtforms import validators, ValidationError

from flask_wtf import FlaskForm

from app.forms.custom import ComaFloatField


class IngredientForm(FlaskForm):
    name = StringField(
        "Název suroviny", [validators.InputRequired("Název musí být vyplněn")]
    )
    description = StringField("Další popis")
    ean_code = StringField("EAN kód")

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

    def validate_ean_code(form, field):
        if field.data and (not field.data.isdigit() or len(field.data) != 13):
            raise ValidationError("EAN kód je zadaný ve špatném formátu (13 číslic)")
