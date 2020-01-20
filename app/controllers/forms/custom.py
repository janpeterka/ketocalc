from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, FloatField
from wtforms import validators

# from wtforms.fields.html5 import EmailField


class MyFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(",", "."))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext("Toto není desetinné číslo"))
