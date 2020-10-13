def register_all_controllers(application):
    from .base_recipes import BaseRecipesView
    from .cookbook import CookbookView
    from .daily_plans import DailyPlansView
    from .dashboard import DashboardView
    from .diets import DietsView
    from .errors import ErrorsView
    from .index import IndexView
    from .ingredients import IngredientsView
    from .login import LoginView
    from .mails import MailsView
    from .password_recovery import PasswordRecoveryView
    from .recipes import RecipesView
    from .register import RegisterView
    from .simple_calculator import SimpleCalculatorView
    from .support import SupportView
    from .trial_recipes import TrialRecipesView
    from .users import UsersView

    BaseRecipesView.register(application)
    CookbookView.register(application)
    DailyPlansView.register(application)
    DashboardView.register(application)
    DietsView.register(application)
    ErrorsView.register(application)
    IndexView.register(application)
    IngredientsView.register(application)
    LoginView.register(application)
    MailsView.register(application)
    PasswordRecoveryView.register(application)
    RecipesView.register(application)
    RegisterView.register(application)
    SimpleCalculatorView.register(application)
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
