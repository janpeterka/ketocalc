from flask import request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_classful import route

from app.helpers.base_view import BaseView
from app.helpers.form import create_form

from app.models import Diet

from app.forms import DietForm


class DietView(BaseView):
    decorators = [login_required]
    template_folder = "diets"

    def before_request(self, name, id=None, *args, **kwargs):
        self.diet = Diet.load(id)

    def before_index(self):
        self.diets = current_user.diets
        self.diets.sort(key=lambda x: (-x.active, x.name))

    def before_show(self, id):
        self.recipes = self.diet.recipes
        self.validate_show(self.diet)

    def before_edit(self, id):
        self.recipes = self.diet.recipes
        self.validate_edit(self.diet)

    def before_update(self, id):
        self.validate_edit(self.diet)

    def index(self):
        return self.template()

    def new(self):
        self.form = create_form(DietForm)

        return self.template()

    def post(self):
        self.form = DietForm(request.form)

        if not self.form.validate_on_submit():
            return self.template("new"), 422

        diet = Diet(author=current_user)
        self.form.populate_obj(diet)
        diet.save()

        return redirect(url_for("DietView:show", id=diet.id))

    def show(self, id):
        return self.template()

    def edit(self, id):
        self.form = create_form(DietForm, obj=self.diet)

        return self.template()

    @route("update/<id>", methods=["POST"])
    def update(self, id):
        self.form = DietForm(request.form)

        if self.diet.is_used:
            del self.form.calorie
            del self.form.protein
            del self.form.fat
            del self.form.sugar

        if not self.form.validate_on_submit():
            return self.template("edit"), 422

        self.form.populate_obj(self.diet)
        self.diet.edit()

        return redirect(url_for("DietView:show", id=self.diet.id))

    @route("delete/<id>", methods=["POST"])
    def delete(self, id):
        if not self.diet.is_used:
            self.diet.remove()
            flash("Dieta byla smazána", "success")
            return redirect(url_for("DietView:index"))
        else:
            flash("Tato dieta má recepty, nelze smazat", "error")
            return redirect(url_for("DietView:show", id=id))

    @route("archive/<id>", methods=["POST"])
    def archive(self, id):
        self.diet.active = not self.diet.active
        self.diet.edit()

        if self.diet.active:
            flash("Dieta byla aktivována", "success")
        else:
            flash("Dieta byla archivována", "success")

        return redirect(url_for("DietView:show", id=id))
