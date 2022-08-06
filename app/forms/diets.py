from wtforms import StringField, SubmitField
from wtforms import validators

from flask_wtf import FlaskForm

from app.forms.custom import ComaFloatField


class DietForm(FlaskForm):
    name = StringField("název", [validators.InputRequired("název musí být vyplněn")])
    calorie = ComaFloatField(
        "množství (kJ) kalorií / den",
        [validators.InputRequired("množství musí být vyplněno")],
    )
    protein = ComaFloatField(
        "množství (g) bílkovin / den",
        [validators.InputRequired("množství musí být vyplněno")],
    )
    sugar = ComaFloatField(
        "množství (g) sacharidů / den",
        [validators.InputRequired("množství musí být vyplněno")],
    )
    fat = ComaFloatField(
        "množství (g) tuku / den",
        [validators.InputRequired("množství musí být vyplněno")],
    )
    submit = SubmitField("přidat")
