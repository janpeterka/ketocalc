import datetime
import unidecode

from sqlalchemy import and_

from app import db

from app.models.item_mixin import ItemMixin
from app.models.recipes_has_ingredients import RecipeHasIngredients


class Ingredient(db.Model, ItemMixin):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    calorie = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    sugar = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    fat = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    protein = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    author = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, onupdate=datetime.datetime.now)

    is_shared = db.Column(db.Boolean)
    is_approved = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(255), default="user")

    recipes = db.relationship(
        "Recipe",
        primaryjoin="and_(Ingredient.id == remote(RecipeHasIngredients.ingredients_id), foreign(Recipe.id) == RecipeHasIngredients.recipes_id)",
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
    def load_all_shared(renamed=False, ordered=True):
        ingredients = (
            db.session.query(Ingredient)
            .filter(and_(Ingredient.is_shared == True, Ingredient.is_approved == True))
            .all()
        )

        if ordered:
            ingredients.sort(
                key=lambda x: unidecode.unidecode(x.name.lower()), reverse=False
            )

        if renamed:
            for ingredient in ingredients:
                ingredient.name = ingredient.name + " (sdílené)"

        return ingredients

    @staticmethod
    def load_all_unapproved():
        ingredients = (
            db.session.query(Ingredient)
            .filter(and_(Ingredient.is_shared == True, Ingredient.is_approved == False))
            .all()
        )
        ingredients.sort(
            key=lambda x: unidecode.unidecode(x.name.lower()), reverse=False
        )
        return ingredients

    def load_amount_by_recipe(self, recipe_id):
        rhi = (
            db.session.query(RecipeHasIngredients)
            .filter(RecipeHasIngredients.recipes_id == recipe_id)
            .filter(RecipeHasIngredients.ingredients_id == self.id)
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

        if "min" in json_ing and len(json_ing["min"]) > 0:
            self.min = float(json_ing["min"])

        if "max" in json_ing and len(json_ing["max"]) > 0:
            self.max = float(json_ing["max"])

    @property
    def author_user(self):
        from app.models.users import User

        user = User.load(self.author, load_type="username")
        return user

    def is_author(self, user) -> bool:
        return self.author_user == user

    @property
    def is_used(self):
        if len(self.recipes) == 0:
            return False
        else:
            return True

    @property
    def public(self) -> bool:
        """alias for is_shared"""
        return self.is_shared

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
