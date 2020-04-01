from flask import render_template as template
from flask import request, redirect, url_for, abort, flash

from flask_classful import FlaskView, route
from flask_login import login_required, current_user

from app.helpers.form import create_form, save_form_to_session

from app.models.ingredients import Ingredient
from app.models.recipes import Recipe

from app.controllers.forms.ingredients import IngredientsForm


class IngredientsView(FlaskView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None):
        if id is not None:
            self.ingredient = Ingredient.load(id)

            if self.ingredient is None:
                abort(404)
            if not (
                self.ingredient.is_shared
                or current_user.is_admin
                or current_user.username == self.ingredient.author
            ):
                abort(403)

    def before_edit(self, id):
        self.ingredient.recipes = Recipe.load_by_ingredient_and_username(
            self.ingredient.id, current_user.username
        )

    def before_show(self, id):
        self.ingredient.recipes = Recipe.load_by_ingredient_and_username(
            self.ingredient.id, current_user.username
        )
        self.ingredient.all_recipes = Recipe.load_by_ingredient(self.ingredient.id)

    def before_index(self):
        self.ingredients = Ingredient.load_all_by_author(current_user.username)
        self.shared_ingredients = Ingredient.load_all_shared()

    def before_shared(self):
        self.shared_ingredients = Ingredient.load_all_shared()
        self.unverified_shared_ingredients = Ingredient.load_all_unverified_shared()

    def index(self):
        return template(
            "ingredients/all.html.j2",
            ingredients=self.ingredients,
            shared_ingredients=self.shared_ingredients,
        )

    def shared(self):
        return template(
            "ingredients/all_shared.html.j2",
            shared_ingredients=self.shared_ingredients,
            unverified_shared_ingredients=self.unverified_shared_ingredients,
        )

    def new(self):
        form = create_form(IngredientsForm)
        return template("ingredients/new.html.j2", form=form)

    def new_shared(self):
        form = create_form(IngredientsForm)
        return template("ingredients/new.html.j2", form=form, shared=True)

    def post(self):
        form = IngredientsForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientsView:new"))

        ingredient = Ingredient()
        form.populate_obj(ingredient)
        ingredient.author = current_user.username

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

        ingredient = Ingredient()
        form.populate_obj(ingredient)
        ingredient.is_shared = True

        if ingredient.save():
            flash(
                "Děkujeme za vytvoření sdílené suroviny. Až ji zkontrolujeme, bude zobrazena všem uživatelům.",
                "success",
            )
            return redirect(url_for("IngredientsView:index"))
        else:
            flash("Nepodařilo se vytvořit surovinu", "error")
            return redirect(url_for("IngredientsView:new_shared"))

    def show(self, id):
        return template(
            "ingredients/show.html.j2",
            ingredient=self.ingredient,
            recipes=self.ingredient.recipes,
            all_recipes=self.ingredient.all_recipes,
        )

    def edit(self, id):
        form = create_form(IngredientsForm, obj=self.ingredient)

        return template(
            "ingredients/edit.html.j2",
            ingredient=self.ingredient,
            recipes=self.ingredient.recipes,
            form=form,
        )

    @route("delete/<id>", methods=["POST"])
    def delete(self, id):
        if not self.ingredient.is_used:
            self.ingredient.remove()
            flash("Surovina byla smazána", "success")
            return redirect(url_for("DashboardView:show"))
        else:
            flash("Tato surovina je použita, nelze smazat", "error")
            return redirect(url_for("IngredientsView:show", id=self.ingredient.id))

    @route("approve/<id>", methods=["GET"])
    def approve(self, id):
        self.ingredient.is_approved = True
        self.ingredient.edit()
        flash("Surovina schválena", "success")
        return redirect(url_for("IngredientsView:shared"))
