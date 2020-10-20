from app.models.recipes import Recipe

from flask import redirect, url_for

from flask_login import current_user

from app.controllers.extended_flask_view import ExtendedFlaskView


class CookbookView(ExtendedFlaskView):
    template_folder = "cookbook"

    def before_index(self):
        if not current_user.is_authenticated:
            return redirect(
                url_for(
                    "CookbookView:not_logged_in",
                    message="Sdílené recepty jsou přístupné pouze pro přihlášené uživatele.",
                )
            )

        self.recipes = Recipe.public_recipes()
