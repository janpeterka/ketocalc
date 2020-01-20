import datetime
import unidecode

from app import db

from app.models.base_mixin import BaseMixin


class Ingredient(db.Model, BaseMixin):
    """Ingredient class

    [description]

    Extends:
        Base

    Variables:
        __tablename__ {str} -- [description]
        id {int} -- [description]
        name {string} -- [description]
        calorie {int} -- [description]
        sugar {int} -- [description]
        fat {int} -- [description]
        protein {int} -- [description]
        author {string} -- [description]
        recipes {relationship} -- [description]
    """

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    calorie = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    sugar = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    fat = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    protein = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    author = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)

    recipes = db.relationship(
        "Recipe",
        primaryjoin="and_(Ingredient.id == remote(RecipesHasIngredient.ingredients_id), foreign(Recipe.id) == RecipesHasIngredient.recipes_id)",
        viewonly=True,
        order_by="Recipe.name",
    )

    @staticmethod
    def load(ingredient_id):
        ingredient = (
            db.session.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        )
        return ingredient

    @staticmethod
    def load_by_name(ingredient_name):
        ingredient = (
            db.session.query(Ingredient)
            .filter(Ingredient.name == ingredient_name)
            .first()
        )
        return ingredient

    @staticmethod
    def load_all_by_author(username, ordered=True):
        """Load Ingredient objects by author

        used for loading all ingredients for user

        Arguments:
            username {string} -- [description]

        Keyword Arguments:
            ordered {bool} -- if ingredients ordered alphabetically (default: {True})

        Returns:
            list -- list of Ingredient objects
        """
        ingredients = (
            db.session.query(Ingredient).filter(Ingredient.author == username).all()
        )
        if ordered is True:
            ingredients.sort(
                key=lambda x: unidecode.unidecode(x.name.lower()), reverse=False
            )
        return ingredients

    def load_amount_by_recipe(self, recipe_id):
        """Load amount of Ingredient in Recipe

        Arguments:
            recipe_id {int} -- Recipe database ID

        Returns:
            int -- amount
        """
        rhi = (
            db.session.query(RecipesHasIngredient)
            .filter(RecipesHasIngredient.recipes_id == recipe_id)
            .filter(RecipesHasIngredient.ingredients_id == self.id)
            .first()
        )
        return rhi.amount

    def duplicate(self):
        new_ingredient = Ingredient()

        new_ingredient.name = self.name
        new_ingredient.calorie = self.calorie
        new_ingredient.sugar = self.sugar
        new_ingredient.fat = self.fat
        new_ingredient.protein = self.protein

        return new_ingredient

    def fill_from_json(self, json_ing):
        if "fixed" in json_ing:
            self.fixed = json_ing["fixed"]
        if "main" in json_ing:
            self.main = json_ing["main"]
        if "amount" in json_ing:
            self.amount = float(json_ing["amount"]) / 100  # from grams per 100g

        if "min" in json_ing:
            self.min = float(json_ing["min"])
        if "max" in json_ing:
            self.max = float(json_ing["max"])

    def set_fixed(self, value=True, amount=0):
        self.fixed = value
        self.amount = amount
        return self

    def set_main(self, value=True):
        self.main = value
        return self

    @property
    def is_used(self):
        if len(self.recipes) == 0:
            return False
        else:
            return True
