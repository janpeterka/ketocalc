from flask import abort, flash, request, redirect, url_for
from flask import render_template as template

from flask_classful import route
from flask_login import login_required, current_user

from app.auth import admin_required
from app.helpers.form import create_form, save_form_to_session
from app.models.ingredients import Ingredient
from app.controllers.extended_flask_view import ExtendedFlaskView
from app.models.recipes import Recipe
from app.controllers.forms.ingredients import IngredientsForm


class IngredientsView(ExtendedFlaskView):
    decorators = [login_required]

    def before_request(self, name, id=None, *args, **kwargs):
        super().before_request(name, id, *args, **kwargs)

        if id is not None:
            if self.ingredient is None:
                abort(404)
            if not self.ingredient.can_current_user_view:
                abort(403)

    def before_edit(self, id):
        super().before_edit(id)
        self.recipes = Recipe.load_by_ingredient_and_user(
            self.ingredient.id, current_user
        )
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

    def before_show(self, id):
        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient.id)

    def before_index(self):
        self.ingredients = Ingredient.load_all_by_author(current_user)
        self.shared_ingredients = Ingredient.load_all_shared()

    def before_shared(self):
        self.shared_ingredients = Ingredient.load_all_shared()
        self.unapproved_ingredients = Ingredient.load_all_unapproved()

    @admin_required
    def all_shared(self):
        return self.template(template_name="ingredients/all_shared.html.j2",)

    def new_shared(self):
        # TODO can be simplified -> redirect? calling super with kwargs?
        form = create_form(IngredientsForm)
        return template("ingredients/new.html.j2", form=form, shared=True)

    def post(self):
        form = IngredientsForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientsView:new"))

        ingredient = Ingredient(author=current_user.username)
        form.populate_obj(ingredient)

        if ingredient.save():
            return redirect(url_for("IngredientsView:show", id=ingredient.id))
        else:
            flash("Nepodařilo se vytvořit surovinu", "error")
            return redirect(url_for("IngredientsView:new"))

    @route("edit/<id>", methods=["POST"])
    def post_edit(self, id):
        form = IngredientsForm(request.form)

        if self.ingredient.is_used:
            del form.calorie
            del form.protein
            del form.fat
            del form.sugar

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientsView:edit", id=self.ingredient.id))

        form.populate_obj(self.ingredient)

        if not self.ingredient.is_shared or current_user.is_admin:
            self.ingredient.edit()
            flash("Surovina byla upravena.", "success")
        else:
            self.ingredient.refresh()
            flash("Sdílenou surovinu nelze upravit", "error")
        return redirect(url_for("IngredientsView:show", id=self.ingredient.id))

    @route("post/shared", methods=["POST"])
    def post_shared(self):
        form = IngredientsForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientsView:new_shared"))

        ingredient = Ingredient(is_shared=True, source=current_user.username)
        form.populate_obj(ingredient)

        if ingredient.save():
            flash(
                "Děkujeme za vytvoření sdílené suroviny. Až ji zkontrolujeme, bude zobrazena všem uživatelům.",
                "success",
            )
            return redirect(url_for("IngredientsView:index"))
        else:
            flash("Nepodařilo se vytvořit surovinu", "error")
            return redirect(url_for("IngredientsView:new_shared"))

    # def edit(self, id):
    # self.form = create_form(IngredientsForm, obj=self.ingredient)
    # return self.template()

    @route("delete/<id>", methods=["POST"])
    def delete(self, id):
        if not self.ingredient.is_used:
            self.ingredient.remove()
            flash("Surovina byla smazána", "success")
            return redirect(url_for("DashboardView:show"))
        else:
            flash("Tato surovina je použita, nelze smazat", "error")
            return redirect(url_for("IngredientsView:show", id=self.ingredient.id))

    @admin_required
    @route("approve/<id>", methods=["GET"])
    def approve(self, id):
        self.ingredient.is_approved = True
        self.ingredient.edit()
        flash("Surovina schválena", "success")
        return redirect(url_for("IngredientsView:shared"))

    @admin_required
    @route("disapprove/<id>", methods=["GET"])
    def disapprove(self, id):
        self.ingredient.is_approved = None
        self.ingredient.edit()
        flash("Surovina neschválena", "info")
        return redirect(url_for("IngredientsView:shared"))
