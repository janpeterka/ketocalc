from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, FloatField, SelectField
from wtforms import validators
# from wtforms.fields.html5 import EmailField


class MyFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Toto není desetinné číslo'))


class NewIngredientForm(FlaskForm):
    name = StringField('Název suroviny', [validators.InputRequired('Název musí být vyplněn')])
    protein = MyFloatField('Množství bílkovin / 100 g', [validators.InputRequired('Množství musí být vyplněno'), validators.NumberRange(0, 100, 'Musí být mezi 0 a 100')])
    sugar = MyFloatField('Množství sacharidů / 100 g', [validators.InputRequired('Množství musí být vyplněno'), validators.NumberRange(0, 100, 'Musí být mezi 0 a 100')])
    fat = MyFloatField('Množství tuku / 100 g', [validators.InputRequired('Množství musí být vyplněno'), validators.NumberRange(0, 100, 'Musí být mezi 0 a 100')])
    calorie = MyFloatField('Energie (kJ) / 100 g', [validators.InputRequired('Množství musí být vyplněno')])
    submit = SubmitField('Přidat surovinu')


class NewDietForm(FlaskForm):
    name = StringField('Název diety', [validators.InputRequired('Název musí být vyplněn')])
    calorie = MyFloatField('Množství (kJ) kalorií / den', [validators.InputRequired('Množství musí být vyplněno')])
    protein = MyFloatField('Množství (g) bílkovin / den', [validators.InputRequired('Množství musí být vyplněno')])
    sugar = MyFloatField('Množství (g) sacharidů / den', [validators.InputRequired('Množství musí být vyplněno')])
    fat = MyFloatField('Množství (g) tuku / den', [validators.InputRequired('Množství musí být vyplněno')])
    small_size = MyFloatField('Procentuální velikost malého jídla', [validators.InputRequired('Množství musí být vyplněno')])
    big_size = MyFloatField('Procentuální velikost velkého jídla', [validators.InputRequired('Množství musí být vyplněno')])
    submit = SubmitField('Přidat dietu')
