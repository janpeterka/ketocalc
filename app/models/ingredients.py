import datetime
import unidecode

from app import db

from app.models.base_mixin import BaseMixin

from app.models.recipes_has_ingredients import RecipesHasIngredient


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
    author = db.Column(db.String(255))
    created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)

    is_shared = db.Column(db.Boolean)
    is_approved = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(255), default="user")

    recipes = db.relationship(
        "Recipe",
        primaryjoin="and_(Ingredient.id == remote(RecipesHasIngredient.ingredients_id), foreign(Recipe.id) == RecipesHasIngredient.recipes_id)",
        viewonly=True,
        order_by="Recipe.name",
    )

    @staticmethod
    def load_all_by_author(username, ordered=True):
        ingredients = (
            db.session.query(Ingredient).filter(Ingredient.author == username).all()
        )
        if ordered:
            ingredients.sort(
                key=lambda x: unidecode.unidecode(x.name.lower()), reverse=False
            )
        return ingredients

    @staticmethod
    def load_all_shared(renamed=False):
        ingredients = Ingredient.load_all_by_author("basic")

        if renamed:
            for ingredient in ingredients:
                ingredient.name = ingredient.name + " (sdílené)"

        return ingredients

    @staticmethod
    def load_all_unverified_shared():
        ingredients = Ingredient.load_all_by_author("basic_unverified")
        return ingredients

    def load_amount_by_recipe(self, recipe_id):
        rhi = (
            db.session.query(RecipesHasIngredient)
            .filter(RecipesHasIngredient.recipes_id == recipe_id)
            .filter(RecipesHasIngredient.ingredients_id == self.id)
            .first()
        )
        return rhi.amount

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

    @property
    def is_used(self):
        if len(self.recipes) == 0:
            return False
        else:
            return True

    # TODO: only used for testing
    def set_fixed(self, value=True, amount=0):
        self.fixed = value
        self.amount = amount
        return self

    # TODO: only used for testing
    def set_main(self, value=True):
        self.main = value
        return self

    # TODO: only used for testing
    @staticmethod
    def load_by_name(ingredient_name):
        ingredient = (
            db.session.query(Ingredient)
            .filter(Ingredient.name == ingredient_name)
            .first()
        )
        return ingredient
