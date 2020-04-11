import datetime
import math
import types

from app import db

from app.models.base_mixin import BaseMixin

from app.models.ingredients import Ingredient
from app.models.recipes_has_ingredients import RecipeHasIngredients


class Recipe(db.Model, BaseMixin):
    """[summary]

    [description]

    Extends:
        Base

    Variables:
        __tablename__ {str} -- [description]
        id {int} -- [description]
        name {string} -- [description]
        type {string} -- [description]
        diet {relationship} -- [description]
        ingredients {relationship} -- [description]
    """

    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum("small", "big", "full"), nullable=False, default="full")

    created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)

    view_count = db.Column(db.Integer, nullable=True, default=0)

    diet = db.relationship("Diet", secondary="diets_has_recipes", uselist=False)
    ingredients = db.relationship(
        "Ingredient",
        primaryjoin="and_(Recipe.id == remote(RecipeHasIngredients.recipes_id), foreign(Ingredient.id) == RecipeHasIngredients.ingredients_id)",
        viewonly=True,
        order_by="Ingredient.name",
    )

    @staticmethod
    def load(recipe_id):
        recipe = db.session.query(Recipe).filter(Recipe.id == recipe_id).first()

        if recipe.type == "big":
            coef = float(recipe.diet.big_size / 100)
        else:
            coef = float(recipe.diet.small_size / 100)

        for ingredient in recipe.ingredients:
            ingredient.amount = (
                float(
                    math.floor(
                        ingredient.load_amount_by_recipe(recipe.id) * coef * 100000
                    )
                )
                / 100000
            )

        return recipe

    def load_recipe_for_show(self):
        """Load Recipe for print

        Returns:
            json -- recipe, totals
        """
        if self.type == "big":
            coef = float(self.diet.big_size / 100)
        else:
            coef = float(self.diet.small_size / 100)

        for ingredient in self.ingredients:
            ingredient.amount = (
                float(
                    math.floor(
                        ingredient.load_amount_by_recipe(self.id) * coef * 100000
                    )
                )
                / 100000
            )

        totals = types.SimpleNamespace()
        totals.calorie = 0
        totals.protein = 0
        totals.fat = 0
        totals.sugar = 0
        totals.amount = 0

        for i in self.ingredients:
            totals.calorie += i.amount * i.calorie
            totals.protein += i.amount * i.protein
            totals.fat += i.amount * i.fat
            totals.sugar += i.amount * i.sugar
            totals.amount += i.amount

        totals.calorie = math.floor(totals.calorie) / 100
        totals.protein = math.floor(totals.protein) / 100
        totals.fat = math.floor(totals.fat) / 100
        totals.sugar = math.floor(totals.sugar) / 100
        totals.amount = math.floor(totals.amount)

        totals.ratio = (
            math.floor((totals.fat / (totals.protein + totals.sugar)) * 100) / 100
        )
        return {"recipe": self, "totals": totals}

    @staticmethod
    def load_by_ingredient(ingredient_id):
        recipes = (
            db.session.query(Recipe)
            .filter(Recipe.ingredients.any(Ingredient.id == ingredient_id))
            .all()
        )
        return recipes

    @staticmethod
    def load_by_ingredient_and_username(ingredient_id, username):
        recipes = Recipe.load_by_ingredient(ingredient_id)
        private_recipes = []
        for recipe in recipes:
            if recipe.author.username == username:
                private_recipes.append(recipe)

        return private_recipes

    def save(self, ingredients):
        db.session.add(self)
        db.session.flush()

        for i in ingredients:
            i.recipes_id = self.id
            db.session.add(i)

        db.session.commit()
        return self.id

    def remove(self):
        # TODO: - to improve w/ orphan cascade (80)
        ingredients = db.session.query(RecipeHasIngredients).filter(
            RecipeHasIngredients.recipes_id == self.id
        )
        for i in ingredients:
            db.session.delete(i)

        db.session.delete(self)
        db.session.commit()
        return True

    def log_view(self):
        if self.view_count is not None:
            self.view_count += 1
        else:
            self.view_count = 1
        self.edit()

    @property
    def totals(self):
        totals = types.SimpleNamespace()
        totals.calorie = 0
        totals.protein = 0
        totals.fat = 0
        totals.sugar = 0
        totals.amount = 0

        if self.type == "big":
            coef = float(self.diet.big_size / 100)
        else:
            coef = float(self.diet.small_size / 100)

        for ingredient in self.ingredients:
            ingredient.amount = (
                float(
                    math.floor(
                        ingredient.load_amount_by_recipe(self.id) * coef * 100000
                    )
                )
                / 100000
            )
            totals.calorie += ingredient.amount * ingredient.calorie
            totals.protein += ingredient.amount * ingredient.protein
            totals.fat += ingredient.amount * ingredient.fat
            totals.sugar += ingredient.amount * ingredient.sugar
            totals.amount += ingredient.amount

        totals.calorie = math.floor(totals.calorie) / 100
        totals.protein = math.floor(totals.protein) / 100
        totals.fat = math.floor(totals.fat) / 100
        totals.sugar = math.floor(totals.sugar) / 100
        totals.amount = math.floor(totals.amount)

        totals.ratio = (
            math.floor((totals.fat / (totals.protein + totals.sugar)) * 100) / 100
        )
        return totals

    @property
    def author(self):
        return self.diet.author
