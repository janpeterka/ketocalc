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

    def before_request(self, name, id=None):
        if id is not None:
            self.ingredient = Ingredient.load(id)

            if self.ingredient is None:
                abort(404)
            if current_user.username != self.ingredient.author:
                abort(403)

    def before_edit(self, id):
        self.ingredient.recipes = Recipe.load_by_ingredient(self.ingredient.id)

    def before_show(self, id):
        self.ingredient.recipes = Recipe.load_by_ingredient(self.ingredient.id)

    def before_index(self):
        self.ingredients = Ingredient.load_all_by_author(current_user.username)

    def index(self):
        return template("ingredients/all.html.j2", ingredients=self.ingredients)

    def new(self):
        form = create_form(IngredientsForm)
        return template("ingredients/new.html.j2", form=form)

    def post(self):
        form = IngredientsForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientsView:new"))

        ingredient = Ingredient()
        form.populate_obj(ingredient)
        ingredient.author = current_user.username

        if ingredient.save():
            flash("Nová surovina byla vytvořena", "success")
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
        self.ingredient.edit()
        flash("Surovina byla upravena.", "success")
        return redirect(url_for("IngredientsView:show", id=self.ingredient.id))

    def show(self, id):
        return template(
            "ingredients/show.html.j2",
            ingredient=self.ingredient,
            recipes=self.ingredient.recipes,
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
