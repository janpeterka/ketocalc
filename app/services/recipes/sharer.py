class RecipeSharer:
    def __init__(self, recipe):
        self.recipe = recipe

    def toggle_shared(self):
        self.recipe.is_shared = not self.recipe.is_shared
        self.recipe.edit()

        return self.recipe.is_shared
