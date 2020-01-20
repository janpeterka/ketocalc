def register_all_controllers(application):
    from app.controllers.diets import DietsView
    from app.controllers.users import UsersView
    from app.controllers.ingredients import IngredientsView
    from app.controllers.recipes import RecipesView

    DietsView.register(application)
    UsersView.register(application)
    IngredientsView.register(application)
    RecipesView.register(application)
