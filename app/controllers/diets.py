from flask import render_template as template
from flask import request, redirect, url_for, session
from flask import abort, flash

from flask_login import login_required, current_user

from flask_classful import FlaskView, route

from app.helpers.form import create_form

from app.models.diets import Diet
from app.models.users import User

from app.controllers.forms.diets import DietsForm


class DietsView(FlaskView):
    decorators = [login_required]

    def before_request(self, name, id=None):
        if id is not None:
            self.diet = Diet.load(id)

            if self.diet is None:
                abort(404)
            elif self.diet.author.username != current_user.username:
                abort(405)

    def before_index(self):
        self.diets = User.load(current_user.id).diets
        self.diets.sort(key=lambda x: (-x.active, x.name))

    def index(self):
        return template("diets/all.html.j2", diets=self.diets)

    def new(self):
        form = create_form(DietsForm)
        return template("diets/new.html.j2", form=form)

    def post(self):
        form = DietsForm(request.form)

        if not form.validate_on_submit():
            session["formdata"] = request.form
            return redirect(url_for("DietsView:new"))

        diet = Diet()
        form.populate_obj(diet)
        diet.active = 1
        diet.author = User.load(current_user.id)

        if diet.save():
            flash("Nová dieta byla vytvořena", "success")
            return redirect(url_for("DietsView:show", id=diet.id))
        else:
            flash("Nepodařilo se vytvořit dietu", "error")
            return redirect(url_for("DietsView:new"))

    @route("<id>/edit", methods=["POST"])
    def post_edit(self, id):
        form = DietsForm(request.form)

        if self.diet.is_used:
            del form.calorie
            del form.protein
            del form.fat
            del form.sugar

        if not form.validate_on_submit():
            session["formdata"] = request.form
            return redirect(url_for("DietsView:edit", id=self.diet.id))

        form.populate_obj(self.diet)
        self.diet.edit()
        return redirect(url_for("DietsView:show", id=self.diet.id))

    def show(self, id):
        return template(
            "diets/show.html.j2",
            diet=self.diet,
            recipes=self.diet.recipes,
            diets=self.diet.author.diets,
        )

    def edit(self, id):
        form = create_form(DietsForm)

        return template(
            "diets/edit.html.j2",
            diet=self.diet,
            recipes=self.diet.recipes,
            diets=self.diet.author.diets,
            form=form,
        )

    @route("/<id>/delete", methods=["POST"])
    def delete(self, id):
        if not self.diet.is_used:
            self.diet.remove()
            flash("Dieta byla smazána", "success")
            return redirect(url_for("DietsView:index"))
        else:
            flash("Tato dieta má recepty, nelze smazat", "error")
            return redirect(url_for("DietsView:show", id=id))

    @route("/<id>/archive", methods=["POST"])
    def archive(self, id):
        self.diet.active = not self.diet.active
        self.diet.edit()

        if self.diet.active:
            flash("Dieta byla aktivována", "success")
        else:
            flash("Dieta byla archivována", "success")

        return redirect(url_for("DietsView:show", id=id))
