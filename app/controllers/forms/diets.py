from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms import validators

from app.controllers.forms.custom import MyFloatField


class DietsForm(FlaskForm):
    name = StringField(
        "Název diety", [validators.InputRequired("Název musí být vyplněn")]
    )
    calorie = MyFloatField(
        "Množství (kJ) kalorií / den",
        [validators.InputRequired("Množství musí být vyplněno")],
    )
    protein = MyFloatField(
        "Množství (g) bílkovin / den",
        [validators.InputRequired("Množství musí být vyplněno")],
    )
    sugar = MyFloatField(
        "Množství (g) sacharidů / den",
        [validators.InputRequired("Množství musí být vyplněno")],
    )
    fat = MyFloatField(
        "Množství (g) tuku / den",
        [validators.InputRequired("Množství musí být vyplněno")],
    )
    small_size = MyFloatField(
        "Procentuální velikost malého jídla",
        [validators.InputRequired("Množství musí být vyplněno")],
    )
    big_size = MyFloatField(
        "Procentuální velikost velkého jídla",
        [validators.InputRequired("Množství musí být vyplněno")],
    )
    submit = SubmitField("Přidat dietu")
