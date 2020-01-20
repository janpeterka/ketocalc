def register_all_controllers(application):
    from app.controllers.diets import DietsView
    from app.controllers.users import UsersView
    from app.controllers.ingredients import IngredientsView
    from app.controllers.recipes import RecipesView
    from app.controllers.dashboard import DashboardView
    from app.controllers.index import IndexView
    from app.controllers.trial_recipes import TrialRecipesView
    from app.controllers.support import SupportView
    from app.controllers.errors import ErrorsView

    DietsView.register(application)
    UsersView.register(application)
    IngredientsView.register(application)
    RecipesView.register(application)
    DashboardView.register(application)
    IndexView.register(application)
    TrialRecipesView.register(application)
    SupportView.register(application)
    ErrorsView.register(application)


def register_error_handlers(application):
    from app.controllers.errors import error404
    from app.controllers.errors import error405
    from app.controllers.errors import error500

    application.register_error_handler(404, error404)
    application.register_error_handler(405, error405)
    application.register_error_handler(500, error500)
    application.register_error_handler(403, error404)
