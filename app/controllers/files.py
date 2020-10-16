from flask import abort
from flask import render_template as template

from flask_security import current_user

from flask_classful import FlaskView

from app.models.files import File
from app.models.files import RecipeImageFile

# from app.models.users import User
from app.handlers.files import FileHandler
from app.handlers.files import AWSFileHandler


class FilesView(FlaskView):
    def show(self, hash_value):
        file = File.load_by_attribute("hash", hash_value)
        if not file:
            abort(404)
        if not file.can_view(current_user):
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
        if not file.can_view(current_user):
            abort(403)
        return FileHandler().download(file)

    def index(self):
        aws_files = AWSFileHandler().list_files()
        files = []
        for aws_file in aws_files:
            # file = File().load_by_attribute("path", aws_file['Key'])
            file = RecipeImageFile().load_by_attribute("path", aws_file["Key"])
            if file is not None:
                files.append(file)
        return template("admin/files/all.html.j2", files=files)
