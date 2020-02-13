# This is needed for Flask-Migrate to work
# import all tables that are not classes (only raw M:N relationship tables)
# imports automatically (because it's __init__.py file)

from .diets_has_recipes import diets_has_recipes  # noqa: F401
from .users_has_diets import users_has_diets  # noqa: F401
