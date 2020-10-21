from app.models.recipes import Recipe

from flask import redirect, url_for

# from flask import request

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

        # page = request.args.get("page", 1, type=int)
        # self.recipe_pagination = Recipe.public_recipes_paginated(page, 30)
        # self.recipes = self.recipe_pagination.items
        self.recipes = Recipe.public_recipes()
