from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators

from flask_wtf import FlaskForm
from flask_wtf import RecaptchaField


class NewPasswordForm(FlaskForm):
    password = PasswordField(
        "Nové heslo",
        [
            validators.InputRequired("Heslo musí být vyplněno"),
            validators.Length(min=8, message="Heslo musí mít alespoň 8 znaků"),
        ],
    )
    recaptcha = RecaptchaField()
    submit = SubmitField("Změnit heslo")


class GetNewPasswordForm(FlaskForm):
    username = StringField(
        "Přihlašovací email",
        [
            validators.InputRequired("Email musí být vyplněn"),
            validators.Email("Toto není emailová adresa!"),
        ],
    )
    submit = SubmitField("Získat nové heslo")
