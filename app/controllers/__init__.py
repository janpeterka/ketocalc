from .admin import AdminView
from .base_recipes import BaseRecipeView
from .cookbook import CookbookView
from .daily_plans import DailyPlanView
from .daily_recipes import DailyRecipeView
from .dashboard import DashboardView
from .diets import DietView
from .errors import ErrorView
from .files import FileView
from .index import IndexView
from .ingredients import IngredientView
from .login import LoginView
from .mails import MailView
from .password_recovery import PasswordRecoveryView
from .recipes import RecipeView
from .register import RegisterView
from .simple_calculator import SimpleCalculatorView
from .support import SupportView
from .trial_recipes import TrialRecipeView
from .users import UserView

__all__ = [
    "AdminView",
    "BaseRecipeView",
    "CookbookView",
    "DailyPlanView",
    "DailyRecipeView",
    "DashboardView",
    "DietView",
    "ErrorView",
    "FileView",
    "IndexView",
    "IngredientView",
    "LoginView",
    "MailView",
    "PasswordRecoveryView",
    "RecipeView",
    "RegisterView",
    "SimpleCalculatorView",
    "SupportView",
    "TrialRecipeView",
    "UserView",
]


def register_all_controllers(application):
    AdminView.register(application)
    BaseRecipeView.register(application)
    CookbookView.register(application)
    DailyPlanView.register(application)
    DailyRecipeView.register(application)
    DashboardView.register(application)
    DietView.register(application)
    ErrorView.register(application)
    FileView.register(application)
    IndexView.register(application)
    IngredientView.register(application)
    LoginView.register(application)
    MailView.register(application)
    PasswordRecoveryView.register(application)
    RecipeView.register(application)
    RegisterView.register(application)
    SimpleCalculatorView.register(application)
    SupportView.register(application)
    TrialRecipeView.register(application)
    UserView.register(application)


def register_error_handlers(application):
    from .errors import error404
    from .errors import error405
    from .errors import error500

    application.register_error_handler(403, error404)
    application.register_error_handler(404, error404)
    application.register_error_handler(405, error405)
    application.register_error_handler(500, error500)
