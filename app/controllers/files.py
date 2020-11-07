from flask import abort
from flask import render_template as template

from flask_classful import FlaskView

from app.models.files import File

# from app.models.users import User
from app.handlers.files import FileHandler


class FilesView(FlaskView):
    def show(self, hash_value):
        file = File.load_first_by_attribute("hash", hash_value)
        if not file:
            abort(404)
        if not file.can_current_user_view:
            abort(403)
        return FileHandler().show(file)

    # def show_profile_pic(self, user_id):
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

    def index(self):
        return template("admin/files/all.html.j2", files=FileHandler().all_files)
