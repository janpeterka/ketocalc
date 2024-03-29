from wtforms import StringField, SubmitField, SelectField, EmailField
from wtforms import validators

# from wtforms.fields.html5 import

from flask_wtf import FlaskForm
from flask_wtf.file import FileField


class FeedbackForm(FlaskForm):
    option = SelectField(
        "vyberte typ reakce",
        choices=[
            ("bug", "Chyba v programu"),
            ("ux", "Problém s používáním uživatelského rozhraní"),
            ("suggestion", "Doporučení na zlepšení aplikace"),
            ("other", "Jiné"),
        ],
    )
    message = StringField("Popište", [validators.InputRequired("Musí být vyplněno")])
    email = EmailField("Váš email (pro případ nutnosti upřesnění)")
    feedback_file = FileField("Screenshot s problémem")
    submit = SubmitField("Poslat reakci")
