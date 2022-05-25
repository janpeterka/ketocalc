from flask import abort, flash, request, redirect, url_for, jsonify
from flask_classful import route
from flask_login import login_required, current_user

from app.auth import admin_required
from app.helpers.form import create_form, save_form_to_session
from app.helpers.base_view import BaseView

from app.models import Ingredient, Recipe

from app.controllers.forms import IngredientsForm


class IngredientsView(BaseView):
    decorators = [login_required]
    template_folder = "ingredients"

    def before_request(self, name, id=None, *args, **kwargs):
        self.ingredient = Ingredient.load(id)

    def before_index(self):
        self.ingredients = Ingredient.load_all_by_author(current_user)
        self.shared_ingredients = Ingredient.load_all_shared()

    def before_show(self, id):
        self.validate_show(self.ingredient)
        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient.id)

    def before_edit(self, id):
        self.validate_edit(self.ingredient)
        self.recipes = Recipe.load_by_ingredient_and_user(
            self.ingredient.id, current_user
        )
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

    def before_update(self, id):
        self.validate_edit(self.ingredient)

    def before_all_shared(self):
        self.shared_ingredients = Ingredient.load_all_shared()
        self.unapproved_ingredients = Ingredient.load_all_unapproved()

    def index(self):
        return self.template()

    def new(self):
        self.form = create_form(IngredientsForm)

        return self.template()

    def show(self, id):
        return self.template()

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

    def edit(self, id):
        self.form = create_form(IngredientsForm, obj=self.ingredient)

        if self.ingredient.is_used:
            self.form.calorie.errors = []
            self.form.protein.errors = []
            self.form.fat.errors = []
            self.form.sugar.errors = []

        return self.template()

    @route("update/<id>", methods=["POST"])
    def update(self, id):
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
    def all_shared(self):
        return self.template(
            template_name="ingredients/all_shared.html.j2",
        )

    def new_shared(self):
        # TODO can be simplified -> redirect? calling super with kwargs?
        form = create_form(IngredientsForm)

        return self.template("ingredients/new.html.j2", form=form, shared=True)

    @route("duplicateAJAX", methods=["POST"])
    def duplicateAJAX(self):
        if request.json.get("ingredient_id") is None:
            abort(500)
        new_ingredient = Ingredient.load(request.json["ingredient_id"]).duplicate()
        new_ingredient.save()
        result = {"ingredient_id": new_ingredient.id}

        return jsonify(result)

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

    @admin_required
    @route("approve/<id>", methods=["GET"])
    def approve(self, id):
        self.ingredient.is_approved = True
        self.ingredient.edit()
        flash("Surovina schválena", "success")
        return redirect(url_for("IngredientsView:all_shared"))

    @admin_required
    @route("disapprove/<id>", methods=["GET"])
    def disapprove(self, id):
        self.ingredient.is_approved = None
        self.ingredient.edit()
        flash("Surovina neschválena", "info")
        return redirect(url_for("IngredientsView:all_shared"))
