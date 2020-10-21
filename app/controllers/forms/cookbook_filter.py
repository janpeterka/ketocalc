from wtforms import SubmitField, SelectField

# from wtforms import validators

from flask_wtf import FlaskForm

from app.controllers.forms.custom import ComaFloatField


class CookbookFilterForm(FlaskForm):
    ratio_from = ComaFloatField("Poměr (od)")
    ratio_to = ComaFloatField("Poměr (do)")
    ingredient_name = SelectField("Surovina")
    submit = SubmitField("Filtrovat")

    def __init__(self, *args, ingredient_names=None):
        if ingredient_names is None:
            raise Exception(f"{self.__class__.__name__} has no select values")

        super().__init__(*args)
        self.set_ingredient_names(ingredient_names)

    def set_ingredient_names(self, ingredient_names):
        self.ingredient_name.choices = [name for name in ingredient_names]
