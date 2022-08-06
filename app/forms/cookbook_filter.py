from wtforms import SubmitField, SelectField, BooleanField

from flask_wtf import FlaskForm

from app.forms.custom import ComaFloatField


class CookbookFilterForm(FlaskForm):
    ratio_from = ComaFloatField("poměr (od)")
    ratio_to = ComaFloatField("poměr (do)")
    ingredient_name = SelectField("surovina")
    with_reaction = BooleanField("moje oblíbené")

    submit = SubmitField("filtrovat")

    def __init__(self, *args, ingredient_names=None):
        if ingredient_names is None:
            raise Exception(f"{self.__class__.__name__} has no select values")

        super().__init__(*args)
        self.set_ingredient_names(ingredient_names)

    def set_ingredient_names(self, ingredient_names):
        self.ingredient_name.choices = list(ingredient_names)
