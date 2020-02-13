import os
from flask import request, redirect

from app import create_app

# from app.models import db
# from app import db
# from app.models.users import User

from app.data import template_data

env = os.environ.get("FLASK_ENV", "default")
application = create_app(config_name=env)


@application.context_processor
def inject_globals():
    return dict(icons=template_data.icons, texts=template_data.texts)


@application.before_request
def session_management():
    if application.config["APP_STATE"] == "shutdown" and request.path not in [
        "/shutdown",
        "/static/style.css",
    ]:
        return redirect("/shutdown")
    elif request.path == "/shutdown" and application.config["APP_STATE"] != "shutdown":
        return redirect("/")


# @application.shell_context_processor
# def make_shell_context():
#     return {"db": db, "User": User}
