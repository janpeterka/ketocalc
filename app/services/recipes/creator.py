class RecipeCreator:
    @staticmethod
    def create(name, diet, ingredient_dict):
        from app.models import RecipeHasIngredient, Recipe

        recipe = Recipe(name=name, diet=diet)
        recipe.save()

        for temp_i in ingredient_dict:
            rhi = RecipeHasIngredient(
                recipes_id=recipe.id,
                ingredients_id=temp_i["id"],
                amount=temp_i["amount"],
            )
            rhi.save()

        return recipe
