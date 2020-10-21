from app.models.recipes import Recipe

from flask import redirect, url_for

from flask_login import current_user

from app.data.texts import texts
from app.controllers.extended_flask_view import ExtendedFlaskView


class CookbookView(ExtendedFlaskView):
    template_folder = "cookbook"

    def before_index(self):
        if not current_user.is_authenticated:
            message = texts.cookbook.not_logged_in
            return redirect(url_for("CookbookView:not_logged_in", message=message))

        self.recipes = Recipe.public_recipes()
