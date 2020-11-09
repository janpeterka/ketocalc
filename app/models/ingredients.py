import datetime
import unidecode

from sqlalchemy import and_

from flask_login import current_user

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
    def load_all_by_author(author, ordered=True):
        if type(author) == str:
            author_name = author
        elif hasattr(author, "username"):
            author_name = author.username
        else:
            raise AttributeError(
                "Wrong type for 'author', expected `str` or object having attribute `username`"
            )

        ingredients = (
            db.session.query(Ingredient).filter(Ingredient.author == author_name).all()
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
            .filter(
                and_(Ingredient.is_shared == True, Ingredient.is_approved == True)
            )  # noqa: E712
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
            .filter(
                and_(Ingredient.is_shared == True, Ingredient.is_approved == False)
            )  # noqa: E712
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

    def is_author(self, user) -> bool:
        return self.author_user == user

    # PERMISSIONS

    def can_add(self, user) -> bool:
        return self.is_author(user) or self.public

    @property
    def can_current_user_add(self) -> bool:
        return self.can_add(current_user)

    # PROPERTIES

    @property
    def author_user(self):
        from app.models.users import User

        user = User.load(self.author, load_type="username")
        return user

    @property
    def is_used(self):
        return True if self.recipes else False

    # TESTING
    # TODO: only used for testing, should be moved to tests
    def set_fixed(self, value=True, amount=0):
        self.fixed = value
        self.amount = amount
        return self

    def set_main(self, value=True):
        self.main = value
        return self

    @staticmethod
    def load_by_name(ingredient_name):
        ingredient = (
            db.session.query(Ingredient)
            .filter(Ingredient.name == ingredient_name)
            .first()
        )
        return ingredient
