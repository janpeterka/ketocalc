from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators, ValidationError

from flask_wtf import FlaskForm
from flask_wtf import RecaptchaField

from app.models.users import User


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

    def validate_username(form, field):
        user = User.load(field.data, load_type="username")
        if user is None:
            raise ValidationError("Uživatel s tímto emailem neexistuje")
