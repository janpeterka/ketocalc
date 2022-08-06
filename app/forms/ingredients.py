from wtforms import StringField, SubmitField
from wtforms import validators, ValidationError

from flask_wtf import FlaskForm

from app.forms.custom import ComaFloatField


class IngredientForm(FlaskForm):
    name = StringField(
        "název suroviny", [validators.InputRequired("název musí být vyplněn")]
    )
    description = StringField("další popis")
    ean_code = StringField("EAN kód")

    protein = ComaFloatField(
        "množství bílkovin / 100 g",
        [
            validators.InputRequired("množství musí být vyplněno"),
            validators.NumberRange(0, 100, "musí být mezi 0 a 100"),
        ],
    )
    sugar = ComaFloatField(
        "množství sacharidů / 100 g",
        [
            validators.InputRequired("množství musí být vyplněno"),
            validators.NumberRange(0, 100, "musí být mezi 0 a 100"),
        ],
    )
    fat = ComaFloatField(
        "množství tuku / 100 g",
        [
            validators.InputRequired("množství musí být vyplněno"),
            validators.NumberRange(0, 100, "musí být mezi 0 a 100"),
        ],
    )
    calorie = ComaFloatField(
        "energie (kJ) / 100 g", [validators.InputRequired("množství musí být vyplněno")]
    )
    submit = SubmitField("přidat surovinu")

    def validate_ean_code(self, field):
        if field.data and (not field.data.isdigit() or len(field.data) != 13):
            raise ValidationError("EAN kód je zadaný ve špatném formátu (13 číslic)")
