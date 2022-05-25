from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators

from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField(
        "Přihlašovací email", [validators.InputRequired("Email musí být vyplněn")]
    )
    password = PasswordField(
        "Heslo", [validators.InputRequired("Heslo musí být vyplněno")]
    )
    submit = SubmitField("Přihlásit")
