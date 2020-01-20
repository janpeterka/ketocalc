from werkzeug import MultiDict

from flask import render_template as template
from flask import request, redirect, url_for, session
from flask import abort

from flask_login import login_required, current_user

from flask_classful import FlaskView

from app.models.diets import Diet
from app.models.users import User

from app.controllers.forms.diets import NewDietsForm


class DietsView(FlaskView):
    decorators = [login_required]

    def before_index(self):
        self.diets = User.load(current_user.id).diets
        self.diets.sort(key=lambda x: (-x.active, x.name))

    def before_request(self, name, id=None):
        if id is not None and name != "post":
            self.diet = Diet.load(id)

            if self.diet is None:
                abort(404)
            elif self.diet.author.username != current_user.username:
                abort(405)

    def index(self):
        return template("diets/all.html.j2", diets=self.diets)

    def new(self):
        if session.get("formdata") is not None:
            data = MultiDict(session.get("formdata"))
            session.pop("formdata")
            form = NewDietsForm(data)
            form.validate()
        else:
            form = NewDietsForm()
        session["form_type"] = "new"
        return template("diets/new.html.j2", form=form)

    def post(self, id=None):
        form = NewDietsForm(request.form)
        form_type = session["form_type"]
        session.pop("form_type")

        if not form.validate_on_submit():
            session["formdata"] = request.form
            if form_type == "edit":
                return redirect(url_for("DietsView:edit"))
            elif form_type == "new":
                return redirect(url_for("DietsView:new"))
            else:
                return redirect(url_for("DietsView:new"))

        if form_type == "edit":
            diet.name = request.form["name"]
            diet.id = id
            diet.small_size = request.form["small_size"]
            diet.big_size = request.form["big_size"]

            if not diet.is_used:
                diet.protein = request.form["protein"]
                diet.fat = request.form["fat"]
                diet.sugar = request.form["sugar"]

            diet.save()
            return redirect(url_for("DietsView:show", id=diet.id))

        diet = Diet()
        form.populate_obj(diet)
        diet.active = 1
        diet.author = User.load(current_user.id)

        if diet.save():
            # TODO: nezohledňuje změněnou
            flash("Nová dieta byla vytvořena", "success")
            return redirect(url_for("DietsView:show", id=diet.id))
        else:
            flash("Nepodařilo se vytvořit dietu", "error")
            return redirect(url_for("DietsView:new"))

    def show(self, id):
        return template(
            "diets/show.html.j2",
            diet=self.diet,
            recipes=self.diet.recipes,
            diets=self.diet.author.diets,
        )

    def edit(self, id):
        return template(
            "diets/edit.html.j2",
            diet=diet,
            recipes=diet.recipes,
            diets=diet.author.diets,
        )

    def delete(self, id):
        diet = Diet.load(id)
        if diet is None:
            abort(404)
        elif diet.author.username != current_user.username:
            abort(405)

        if not diet.is_used:
            diet.remove()
            flash("Dieta byla smazána", "success")
            return redirect("/alldiets")
        else:
            flash("Tato dieta má recepty, nelze smazat", "error")
            # return redirect("/diet={}".format(id))
            return redirect(url_for("DietsView:show", id=id))

    def archive(self, id):
        # diet = Diet.load(id)
        # if diet is None:
        #     abort(404)
        # elif diet.author.username != current_user.username:
        #     abort(405)

        self.diet.refresh()
        self.diet.active = not diet.active
        self.diet.edit()

        if self.diet.active:
            flash("Dieta byla aktivována", "success")
        else:
            flash("Dieta byla archivována", "success")

        return redirect("/diet={}".format(id))

    def print(self, id):
        return None
