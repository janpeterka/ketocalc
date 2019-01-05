from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms import validators


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
    calorie = MyFloatField('Energie (kJ) / 100 g', [validators.InputRequired('Množství musí být vyplněno')])
    submit = SubmitField('Přidat surovinu')


# U edit formů je problém s default values
# class EditIngredientForm(FlaskForm):
#     name = StringField('')
#     protein = MyFloatField('')

class NewDietForm(FlaskForm):
    name = StringField('Název diety', [validators.InputRequired('Název musí být vyplněn')])
    protein = MyFloatField('Množství bílkovin / den', [validators.InputRequired('Množství musí být vyplněno')])
    sugar = MyFloatField('Množství sacharidů / den', [validators.InputRequired('Množství musí být vyplněno')])
    fat = MyFloatField('Množství tuku / den', [validators.InputRequired('Množství musí být vyplněno')])
    small_size = MyFloatField('Procentuální velikost malého jídla', [validators.InputRequired('Množství musí být vyplněno')])
    big_size = MyFloatField('Procentuální velikost velkého jídla', [validators.InputRequired('Množství musí být vyplněno')])
    submit = SubmitField('Přidat dietu')

