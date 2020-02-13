from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators

from flask_wtf import FlaskForm


class UserForm(FlaskForm):
    username = StringField(
        "Přihlašovací email", [validators.InputRequired("Email musí být vyplněn")]
    )
    first_name = StringField(
        "Křestní jméno", [validators.InputRequired("Jméno musí být vyplněno")]
    )
    last_name = StringField(
        "Příjmení", [validators.InputRequired("Jméno musí být vyplněno")]
    )
    submit = SubmitField("Upravit")


class PasswordForm(FlaskForm):
    password = PasswordField(
        "Heslo",
        [
            validators.InputRequired("Heslo musí být vyplněno"),
            validators.Length(min=8, message="Heslo musí mít alespoň 8 znaků"),
        ],
    )
    submit = SubmitField("Změnit heslo")
