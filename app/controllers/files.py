from flask import abort, request, redirect, flash
from flask import render_template as template
from flask_classful import FlaskView, route

from app.auth import admin_required
from app.handlers.files import FileHandler

from app.models import File


class FileView(FlaskView):
    @admin_required
    def index(self):
        return template("admin/files/all.html.j2", files=FileHandler().all_files)

    def show(self, hash_value):
        file = File.load_first_by_attribute("hash", hash_value)
        if not file:
            abort(404)
        if not file.can_current_user_view:
            abort(403)
        thumbnail = request.args.get("thumbnail", False)

        return FileHandler().show(file, thumbnail=(thumbnail == "True"))

    @route("/<id>/delete", methods=["POST"])
    def delete(self, id):
        file = File.load(id)
        if file.can_current_user_delete:
            file.delete()
        else:
            flash("Nemáte právo toto foto smazat.", "error")

        return redirect(request.referrer)

    # def show_profile_pic(self, user_id):
    #     from app.models.users import User
    #     file = User.load(user_id).profile_picture_file
    #     if not file:
    #         return FileHandler().show_new_user_placeholder()
    #     if not file.can_view(current_user):
    #         abort(403)
    #     return FileHandler().show(file)

    def download(self, id):
        file = File.load(id)
        if not file:
            abort(404)
        if not file.can_current_user_view:
            abort(403)

        return FileHandler().download(file)
