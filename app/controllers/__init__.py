def register_all_controllers(application):
    from .dashboard import DashboardView
    from .diets import DietsView
    from .errors import ErrorsView
    from .index import IndexView
    from .ingredients import IngredientsView
    from .login import LoginView
    from .password_recovery import PasswordRecoveryView
    from .recipes import RecipesView
    from .register import RegisterView
    from .support import SupportView
    from .trial_recipes import TrialRecipesView
    from .users import UsersView

    DashboardView.register(application)
    DietsView.register(application)
    ErrorsView.register(application)
    IndexView.register(application)
    IngredientsView.register(application)
    LoginView.register(application)
    PasswordRecoveryView.register(application)
    RecipesView.register(application)
    RegisterView.register(application)
    SupportView.register(application)
    TrialRecipesView.register(application)
    UsersView.register(application)


def register_error_handlers(application):
    from .errors import error404
    from .errors import error405
    from .errors import error500

    application.register_error_handler(403, error404)
    application.register_error_handler(404, error404)
    application.register_error_handler(405, error405)
    application.register_error_handler(500, error500)