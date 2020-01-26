from werkzeug import MultiDict

from flask import render_template as template
from flask import request, redirect, url_for, session, abort, flash

from flask_classful import FlaskView, route
from flask_login import login_required, current_user

from app.models.ingredients import Ingredient
from app.models.recipes import Recipe

from app.controllers.forms.ingredients import NewIngredientsForm


class IngredientsView(FlaskView):
    decorators = [login_required]

    def before_request(self, name, id=None):
        if id is not None:
            self.ingredient = Ingredient.load(id)

            if self.ingredient is None:
                abort(404)
            if current_user.username != self.ingredient.author:
                abort(403)

    def before_edit(self, id=None):
        self.ingredient.recipes = Recipe.load_by_ingredient(self.ingredient.id)

    def before_show(self, id=None):
        self.ingredient.recipes = Recipe.load_by_ingredient(self.ingredient.id)

    def before_index(self):
        self.ingredients = Ingredient.load_all_by_author(current_user.username)

    def index(self):
        return template("ingredients/all.html.j2", ingredients=self.ingredients)

    def new(self):
        form_data = None
        if session.get("formdata") is not None:
            form_data = MultiDict(session.get("formdata"))
            session.pop("formdata")

        if form_data:
            form = NewIngredientsForm(form_data)
            form.validate()
        else:
            form = NewIngredientsForm()
        session["form_type"] = "new"
        return template("ingredients/new.html.j2", form=form)

    def post(self, id=None):
        form_type = session["form_type"]
        session.pop("form_type")
        form = NewIngredientsForm(request.form)

        if not form.validate_on_submit():
            session["formdata"] = request.form
            if form_type == "edit":
                return redirect(url_for("IngredientsView:edit", id=self.ingredient.id))
            elif form_type == "new":
                return redirect(url_for("IngredientsView:new"))
            else:
                return redirect(url_for("IngredientsView:new"))

        if form_type == "edit":
            self.ingredient.id = id
            self.ingredient.name = request.form["name"]
            self.ingredient.calorie = request.form["calorie"]
            if not self.ingredient.is_used:
                self.ingredient.protein = request.form["protein"]
                self.ingredient.fat = request.form["fat"]
                self.ingredient.sugar = request.form["sugar"]
                self.ingredient.edit()
                flash("Surovina byla upravena.", "success")
                return redirect(url_for("IngredientsView:show", id=self.ingredient.id))
            else:
                self.ingredient.edit()
                flash("Název a kalorická hodnota byly upraveny.", "success")
                return redirect(url_for("IngredientsView:show", id=self.ingredient.id))

        ingredient = Ingredient()
        form.populate_obj(ingredient)
        ingredient.author = current_user.username

        if ingredient.save():
            flash("Nová surovina byla vytvořena", "success")
            return redirect(url_for("IngredientsView:show", id=ingredient.id))
        else:
            flash("Nepodařilo se vytvořit surovinu", "error")
            return redirect(url_for("IngredientsView:new"))

        return None

    def show(self, id):
        return template(
            "ingredients/show.html.j2",
            ingredient=self.ingredient,
            recipes=self.ingredient.recipes,
        )

    def edit(self, id):
        session["form_type"] = "edit"
        return template(
            "ingredients/edit.html.j2",
            ingredient=self.ingredient,
            recipes=self.ingredient.recipes,
        )

    @route("/ingredients/<id>", methods=["POST"])
    def delete(self, id):
        if not self.ingredient.is_used:
            self.ingredient.remove()
            flash("Surovina byla smazána", "success")
            return redirect("/")
        else:
            flash("Tato surovina je použita, nelze smazat", "error")
            return redirect(url_for("IngredientsView:show", id=self.ingredient.id))
        return None
