from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators, ValidationError

from flask_wtf import FlaskForm

# from flask_wtf import RecaptchaField

from app.auth.routes import validate_register


class RegisterForm(FlaskForm):
    username = StringField(
        "přihlašovací e-mail",
        [
            validators.InputRequired("e-mail musí být vyplněn"),
            validators.Email("Toto není emailová adresa!"),
        ],
    )
    password = PasswordField(
        "Heslo",
        [
            validators.InputRequired("Heslo musí být vyplněno"),
            validators.Length(min=8, message="Heslo musí mít alespoň 8 znaků"),
        ],
    )
    first_name = StringField(
        "Křestní jméno", [validators.InputRequired("Jméno musí být vyplněno")]
    )
    last_name = StringField(
        "Příjmení", [validators.InputRequired("Jméno musí být vyplněno")]
    )
    # recaptcha = RecaptchaField()
    submit = SubmitField("Registrovat")

    def validate_username(self, field):
        if not validate_register(field.data):
            raise ValidationError("Toto jméno nemůžete použít")
