from flask_login import current_user
from app.models import UserHasRecipeReaction


class RecipeReactionManager:
    def __init__(self, recipe):
        self.recipe = recipe

    def add_reaction(self):
        UserHasRecipeReaction(recipe=self.recipe, user=current_user).save()

    def remove_reaction(self):
        UserHasRecipeReaction.load_by_recipe_and_current_user(
            recipe=self.recipe
        ).remove()

    def toggle_reaction(self):
        if self.recipe.has_reaction_by_current_user is True:
            self.remove_reaction()
        else:
            self.add_reaction()
