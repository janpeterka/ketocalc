from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators

from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField(
        "přihlašovací e-mail", [validators.InputRequired("e-mail musí být vyplněn")]
    )
    password = PasswordField(
        "heslo", [validators.InputRequired("heslo musí být vyplněno")]
    )
    submit = SubmitField("přihlásit se")
