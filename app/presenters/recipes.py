from app.presenters import BasePresenter


class RecipePresenter(BasePresenter):
    @property
    def ingredient_ids_list(self):
        return str([i.id for i in self.ingredients])
