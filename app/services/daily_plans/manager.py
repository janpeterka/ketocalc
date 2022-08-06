from app.models import DailyPlanHasRecipes


class DailyPlanManager:
    def __init__(self, daily_plan):
        self.daily_plan = daily_plan

    def add_recipe(self, recipe, amount):
        order_index = len(self.daily_plan.daily_recipes) + 1

        dphr = DailyPlanHasRecipes(
            recipes_id=recipe.id,
            daily_plans_id=self.daily_plan.id,
            amount=amount,
            order_index=order_index,
        )

        dphr.save()

    def remove_recipe_by_id(self, daily_recipe_id):
        # TODO - jenom pokud je fakt v tomhle daily_planu
        selected_daily_recipe = DailyPlanHasRecipes.load(daily_recipe_id)

        if selected_daily_recipe in self.daily_plan.daily_recipes:
            for daily_recipe in self.daily_plan.daily_recipes:
                if daily_recipe.order_index > selected_daily_recipe.order_index:
                    daily_recipe.order_index -= 1
                    daily_recipe.edit()
            selected_daily_recipe.remove()
            return True
        else:
            return False

    def change_order(self, daily_recipe_id, order_type):
        coef = 1 if order_type == "up" else -1

        selected_daily_recipe = DailyPlanHasRecipes.load(daily_recipe_id)

        for daily_recipe in self.daily_plan.daily_recipes:
            if daily_recipe.order_index == selected_daily_recipe.order_index - (
                1 * coef
            ):
                daily_recipe.order_index += 1 * coef
                daily_recipe.edit()

                selected_daily_recipe.order_index -= 1 * coef
                selected_daily_recipe.edit()
                return
