import os
import re
from flask import request, redirect

from flask_login import current_user

from app import create_app

# from app.models import db
# from app import db
# from app.models.users import User
from app.models.request_log import RequestLog

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
        "/static/css/style.css",
    ]:
        return redirect("/shutdown")
    elif request.path == "/shutdown" and application.config["APP_STATE"] != "shutdown":
        return redirect("/")


@application.before_request
def log_request():
    pattern = re.compile("^/static/([A-Za-z0-9])*$")
    if not pattern.match(request.path):
        url = request.path
        remote_addr = request.environ["REMOTE_ADDR"]
        if hasattr(current_user, "id"):
            user_id = current_user.id
        else:
            user_id = None
        log = RequestLog(url=url, user_id=user_id, remote_addr=remote_addr)
        log.save()


# @application.shell_context_processor
# def make_shell_context():
#     return {"db": db, "User": User}
