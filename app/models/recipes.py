import datetime
import math
import types

from app import db

# from app import cache

from flask_login import current_user

from app.models.item_mixin import ItemMixin

from app.models import Ingredient


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
        primaryjoin="and_(Recipe.id == remote(RecipeHasIngredient.recipes_id), foreign(Ingredient.id) == RecipeHasIngredient.ingredients_id)",
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

        return Recipe.query.filter(
            Recipe.ingredients.any(Ingredient.id == ingredient_id)
        ).all()

    @staticmethod
    def load_by_ingredient_and_user(ingredient, user):
        recipes = Recipe.load_by_ingredient(ingredient)
        return [r for r in recipes if r.author == user]

    @staticmethod
    def public_recipes():
        return Recipe.query.filter(Recipe.public).all()

    @property
    def has_reaction_by_current_user(self):
        from app.models import UserHasRecipeReaction

        reactions = UserHasRecipeReaction.load_by_recipe_and_current_user(self)
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
            if getattr(self, "amount", None) is None:
                value = total
            elif self.totals.amount > 0:
                value = (total / self.totals.amount) * self.amount
            else:
                value = 0
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
