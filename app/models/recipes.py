import datetime
import math
import types

from app import db

# from app import cache

from flask_login import current_user

from app.models.item_mixin import ItemMixin

from app.models.ingredients import Ingredient
from app.models.recipes_has_ingredients import RecipeHasIngredients

from app.models.user_recipe_reactions import UserRecipeReactions


class Recipe(db.Model, ItemMixin):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum("small", "big", "full"), nullable=False, default="full")

    description = db.Column(db.Text)

    created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)

    is_shared = db.Column(db.Boolean, default=False)

    diet = db.relationship("Diet", secondary="diets_has_recipes", uselist=False)
    ingredients = db.relationship(
        "Ingredient",
        primaryjoin="and_(Recipe.id == remote(RecipeHasIngredients.recipes_id), foreign(Ingredient.id) == RecipeHasIngredients.ingredients_id)",
        viewonly=True,
        order_by="Ingredient.name",
    )

    has_daily_plans = db.relationship("DailyPlanHasRecipes", back_populates="recipe")

    @staticmethod
    def load(recipe_id):
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        if recipe is None:
            return None

        for ingredient in recipe.ingredients:
            ingredient.amount = round(ingredient.load_amount_by_recipe(recipe.id), 2)

        return recipe

    @staticmethod
    def load_by_ingredient(ingredient):
        # TODO refactor code and only have object
        if type(ingredient) == int:
            ingredient_id = ingredient
        elif type(ingredient) == Ingredient:
            ingredient_id = ingredient.id
        else:
            AttributeError("Wrong ingredient type")

        recipes = Recipe.query.filter(
            Recipe.ingredients.any(Ingredient.id == ingredient_id)
        ).all()
        return recipes

    @staticmethod
    def load_by_ingredient_and_user(ingredient, user):
        recipes = Recipe.load_by_ingredient(ingredient)
        private_recipes = [r for r in recipes if r.author == user]

        return private_recipes

    @staticmethod
    def public_recipes():
        recipes = Recipe.query.filter(Recipe.public).all()
        return recipes

    def create_and_save(self, ingredients):
        db.session.add(self)
        db.session.flush()

        for i in ingredients:
            i.recipes_id = self.id
            db.session.add(i)

        db.session.commit()
        return self.id

    def remove(self):
        # TODO: - to improve w/ orphan cascade (80)
        ingredients = RecipeHasIngredients.query.filter(
            RecipeHasIngredients.recipes_id == self.id
        )
        for i in ingredients:
            db.session.delete(i)

        db.session.delete(self)
        db.session.commit()
        return True

    def toggle_shared(self):
        self.is_shared = not self.is_shared
        self.edit()
        return self.is_shared

    def toggle_reaction(self, user=None):
        user = current_user if user is None else user

        if self.has_reaction is True:
            self.remove_reaction(user)
        else:
            self.add_reaction(user)

    def add_reaction(self, user):
        UserRecipeReactions(recipe=self, user=user).save()

    def remove_reaction(self, user):
        UserRecipeReactions.load_by_recipe_and_current_user(recipe=self).remove()

    @property
    def has_reaction(self):
        reactions = UserRecipeReactions.load_by_recipe_and_current_user(self)
        return bool(reactions)

    @property
    # @cache.cached(timeout=50, key_prefix="recipe_totals")
    def totals(self):
        totals = types.SimpleNamespace()
        metrics = ["calorie", "sugar", "fat", "protein"]

        totals.amount = 0

        for ingredient in self.ingredients:
            ingredient.amount = round(ingredient.load_amount_by_recipe(self.id), 2)
            for metric in metrics:
                value = getattr(totals, metric, 0)
                ing_value = getattr(ingredient, metric)
                setattr(totals, metric, value + (ingredient.amount * ing_value))

            totals.amount += ingredient.amount

        for metric in metrics:
            value = getattr(totals, metric, 0)
            setattr(totals, metric, math.floor(value) / 100)

        totals.amount = math.floor(totals.amount)

        if totals.protein + totals.sugar > 0:
            totals.ratio = (
                math.floor((totals.fat / (totals.protein + totals.sugar)) * 100) / 100
            )
        else:
            totals.ratio = 0

        return totals

    @property
    def ratio(self):
        return self.totals.ratio

    @property
    def values(self):
        values = types.SimpleNamespace()
        metrics = ["calorie", "sugar", "fat", "protein"]
        for metric in metrics:
            total = getattr(self.totals, metric)
            if getattr(self, "amount", None) is not None:
                value = (total / self.totals.amount) * self.amount
            else:
                value = total
            setattr(values, metric, value)
        return values

    @property
    def author(self):
        return self.diet.author

    @property
    def concat_ingredients(self) -> str:
        return ", ".join([o.name for o in self.ingredients])

    # PERMISSIONS

    def can_add(self, user) -> bool:
        return self.is_author(user)

    @property
    def can_current_user_add(self) -> bool:
        return self.can_add(current_user)

    @property
    def can_current_user_show(self) -> bool:
        return current_user == self.author or current_user.is_admin or self.public
