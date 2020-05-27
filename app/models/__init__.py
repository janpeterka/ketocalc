# This is needed for Flask-Migrate to work
# import all tables that are not classes (only raw M:N relationship tables)
# imports automatically (because it's __init__.py file)

from .daily_plan_has_recipes import DailyPlanHasRecipes  # noqa: F401
from .diets_has_recipes import diets_has_recipes  # noqa: F401
from .request_log import RequestLog  # noqa: F401
