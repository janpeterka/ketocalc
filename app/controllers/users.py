from werkzeug import MultiDict

from flask import render_template as template
from flask import request, redirect, url_for, session
from flask import abort

from flask_login import login_required, current_user

from flask_classful import FlaskView

from app.models.users import User

# from app.controllers.forms.users import NewUsersForm


class UsersView(FlaskView):
    decorators = [login_required]

    # def before_request(self, id):
    #     print(id)
    #     if id is not None:
    #         diet = Diet.load(id)

    #         if diet is None:
    #             # abort(404)
    #             print("no diet")
    #         elif diet.author.username != current_user.username:
    #             print("not your diet")
    #             # abort(405)

    def index(self):
        # Users = User.load(current_user.id).Users
        # Users.sort(key=lambda x: (-x.active, x.name))

        return template("users/all.html.j2", Users=Users)

    def new(self):
        # if session.get("formdata") is not None:
        #     data = MultiDict(session.get("formdata"))
        #     session.pop("formdata")
        #     form = NewUsersForm(data)
        #     form.validate()
        # else:
        #     form = NewUsersForm()
        # session["form_type"] = "new"
        return template("users/new.html.j2", form=form)

    def post(self):
        # form = NewUsersForm(request.form)
        # if not form.validate_on_submit():
        #     session["formdata"] = request.form
        #     form_type = session["form_type"]
        #     session.pop("form_type")
        #     if form_type == "edit":
        #         return redirect(url_for("UsersView:edit"))
        #     elif form_type == "new":
        #         return redirect(url_for("UsersView:new"))
        #     else:
        #         return redirect(url_for("UsersView:new"))

        # if form_type == "edit":
        #     diet.name = request.form["name"]
        #     diet.id = id
        #     diet.small_size = request.form["small_size"]
        #     diet.big_size = request.form["big_size"]

        #     if not diet.is_used:
        #         diet.protein = request.form["protein"]
        #         diet.fat = request.form["fat"]
        #         diet.sugar = request.form["sugar"]
        #     # flash("Dieta je používána, nemůžete ji změnit")
        #     diet.save()
        #     return redirect(url_for("UsersView:show", id=diet.id))

        # diet = Diet()
        # form.populate_obj(diet)
        # diet.active = 1
        # diet.author = User.load(current_user.id)

        # if diet.save():
        #     # TODO: nezohledňuje změněnou
        #     flash("Nová dieta byla vytvořena", "success")
        #     return redirect(url_for("UsersView:show", id=diet.id))
        # else:
        #     flash("Nepodařilo se vytvořit dietu", "error")
        #     return redirect(url_for("UsersView:new"))
        return None

    def show(self):
        # diet = Diet.load(id)

        # if diet is None:
        #     abort(404)
        # elif diet.author.username != current_user.username:
        #     abort(405)

        # return template(
        #     "Users/show.html.j2",
        #     diet=diet,
        #     recipes=diet.recipes,
        #     Users=diet.author.Users,
        # )
        return None

    def edit(self):
        # diet = Diet.load(id)

        # if diet is None:
        #     abort(404)
        # elif diet.author.username != current_user.username:
        #     abort(405)
        # return template(
        #     "Users/edit.html.j2",
        #     diet=diet,
        #     recipes=diet.recipes,
        #     Users=diet.author.Users,
        # )
        return None

    def delete(self):
        # diet = Diet.load(id)
        # if diet is None:
        #     abort(404)
        # elif diet.author.username != current_user.username:
        #     abort(405)

        # if not diet.is_used:
        #     diet.remove()
        #     flash("Dieta byla smazána", "success")
        #     return redirect("/allUsers")
        # else:
        #     flash("Tato dieta má recepty, nelze smazat", "error")
        #     # return redirect("/diet={}".format(id))
        #     return redirect(url_for("UsersView:show", id=id))
        return None