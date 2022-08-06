from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators

from flask_wtf import FlaskForm


class UserForm(FlaskForm):
    username = StringField(
        "přihlašovací email", [validators.InputRequired("email musí být vyplněn")]
    )
    first_name = StringField(
        "křestní jméno", [validators.InputRequired("jméno musí být vyplněno")]
    )
    last_name = StringField(
        "příjmení", [validators.InputRequired("příjmení musí být vyplněno")]
    )
    submit = SubmitField("upravit")


class PasswordForm(FlaskForm):
    password = PasswordField(
        "heslo",
        [
            validators.InputRequired("heslo musí být vyplněno"),
            validators.Length(min=8, message="heslo musí mít alespoň 8 znaků"),
        ],
    )
    submit = SubmitField("změnit heslo")
