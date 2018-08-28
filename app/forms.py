# import flask_wtf
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms import validators
# from wtforms.validators import DataRequired


class MyFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Toto není desetinné číslo'))


class LoginForm(FlaskForm):
    username = StringField('Přihlašovací email', [validators.InputRequired('Email musí být vyplněn')])
    password = PasswordField('Heslo', [validators.InputRequired('Heslo musí být vyplněno')])
    submit = SubmitField('Přihlásit')


class RegisterForm(FlaskForm):
    username = StringField('Přihlašovací email', [validators.InputRequired('Email musí být vyplněn'), validators.Email('Toto není emailová adresa!')])
    password = PasswordField('Heslo', [validators.InputRequired('Heslo musí být vyplněno'), validators.Length(min=8, message='Heslo musí mít alespoň 8 znaků')])
    password_again = PasswordField('Heslo', [validators.InputRequired('Heslo musí být vyplněno'), validators.EqualTo('password', message='Hesla musí být stejná!')])
    first_name = StringField('Křestní jméno', [validators.InputRequired('Jméno musí být vyplněno')])
    last_name = StringField('Příjmení', [validators.InputRequired('Jméno musí být vyplněno')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Registrovat')


class NewIngredientForm(FlaskForm):
    name = StringField('Název suroviny', [validators.InputRequired('Název musí být vyplněn')])
    protein = MyFloatField('Množství bílkovin / 100 g', [validators.InputRequired('Množství musí být vyplněno'), validators.NumberRange(0, 100, 'Musí být mezi 0 a 100')])
    sugar = MyFloatField('Množství sacharidů / 100 g', [validators.InputRequired('Množství musí být vyplněno'), validators.NumberRange(0, 100, 'Musí být mezi 0 a 100')])
    fat = MyFloatField('Množství tuku / 100 g', [validators.InputRequired('Množství musí být vyplněno'), validators.NumberRange(0, 100, 'Musí být mezi 0 a 100')])
    calorie = MyFloatField('Množství kalorií (kcal) / 100 g', [validators.InputRequired('Množství musí být vyplněno'), validators.NumberRange(0, 100, 'Musí být mezi 0 a 100')])
    submit = SubmitField('Přidat surovinu')
