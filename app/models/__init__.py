# This is needed for Flask-Migrate to work
# import all tables that are not classes (only raw M:N relationship tables)
# imports automatically (because it's __init__.py file)

from app.models.diets_has_recipes import diets_has_recipes
from app.models.users_has_diets import users_has_diets
