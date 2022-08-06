from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators, ValidationError

from flask_wtf import FlaskForm

# from flask_wtf import RecaptchaField

from app.models.users import User


class NewPasswordForm(FlaskForm):
    password = PasswordField(
        "nové heslo",
        [
            validators.InputRequired("heslo musí být vyplněno"),
            validators.Length(min=8, message="heslo musí mít alespoň 8 znaků"),
        ],
    )
    # recaptcha = RecaptchaField()
    submit = SubmitField("změnit heslo")


class GetNewPasswordForm(FlaskForm):
    username = StringField(
        "přihlašovací e-mail",
        [
            validators.InputRequired("e-mail musí být vyplněn"),
            validators.Email("toto není emailová adresa!"),
        ],
    )
    submit = SubmitField("získat nové heslo")

    def validate_username(self, field):
        user = User.load_by_username(field.data)
        if user is None:
            raise ValidationError("Uživatel s tímto emailem neexistuje")
