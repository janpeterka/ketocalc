from app import db

from flask_login import current_user

from app.models.base_mixin import BaseMixin


class UserRecipeReactions(db.Model, BaseMixin):
    __tablename__ = "user_recipe_reactions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(
        db.DateTime, nullable=True, default=db.func.current_timestamp()
    )

    recipe_id = db.Column(db.ForeignKey("recipes.id"), nullable=False, index=True)
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False, index=True)

    recipe = db.relationship("Recipe", backref="reactions")
    user = db.relationship("User", backref="reactions")

    # LOADERS

    @staticmethod
    def load_by_recipe(recipe):
        return UserRecipeReactions.load_by_attribute("recipe_id", recipe.id)

    @staticmethod
    def load_by_recipe_and_user(recipe, user):
        reactions = UserRecipeReactions.query.filter_by(
            recipe_id=recipe.id, user_id=user.id
        ).first()
        return reactions

    @staticmethod
    def load_by_recipe_and_current_user(recipe):
        return UserRecipeReactions.load_by_recipe_and_user(recipe, current_user)
