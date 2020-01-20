def register_all_controllers(application):
    from app.controllers.diets import DietsView
    from app.controllers.users import UsersView
    from app.controllers.ingredients import IngredientsView
    from app.controllers.recipes import RecipesView
    from app.controllers.dashboard import DashboardView
    from app.controllers.index import IndexView

    DietsView.register(application)
    UsersView.register(application)
    IngredientsView.register(application)
    RecipesView.register(application)
    DashboardView.register(application)
    IndexView.register(application)
