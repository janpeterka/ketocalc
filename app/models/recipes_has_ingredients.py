from app import db
from app.models.base_mixin import BaseMixin


class RecipeHasIngredient(db.Model, BaseMixin):
    """Recipe-Ingredient connection class

    Extends:
        Base

    Variables:
        __tablename__ {str} -- [description]
        recipes_id {int} -- [description]
        ingredients_id {int} -- [description]
        amount {int} -- [description]
        ingredients {relationship} -- [description]
        recipes {relationship} -- [description]
    """

    __tablename__ = "recipes_has_ingredients"

    recipes_id = db.Column(
        db.ForeignKey("recipes.id"), primary_key=True, nullable=False, index=True
    )
    ingredients_id = db.Column(
        db.ForeignKey("ingredients.id"), primary_key=True, nullable=False, index=True
    )
    amount = db.Column(db.Float, nullable=False)

    ingredients = db.relationship(
        "Ingredient",
        backref=db.backref(
            "ingredient_recipes", cascade="all, delete, delete-orphan", viewonly=False
        ),
    )
    recipes = db.relationship(
        "Recipe",
        backref=db.backref(
            "recipe_ingredients", cascade="all, delete, delete-orphan", viewonly=False
        ),
    )
