import os
import re
import time

from flask import request, redirect
from flask import g

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
def log_request_start():
    g.start = time.time()


@application.teardown_request
def log_request(exception=None):
    pattern = re.compile("/static/")
    if not pattern.search(request.path):
        user_id = getattr(current_user, "id", None)
        item_type = getattr(g, "request_item_type", None)
        item_id = getattr(g, "request_item_id", None)

        log = RequestLog(
            url=request.path,
            user_id=user_id,
            remote_addr=request.environ["REMOTE_ADDR"],
            item_type=item_type,
            item_id=item_id,
            duration=time.time() - g.start,
        )
        log.save()


# @application.shell_context_processor
# def make_shell_context():
#     return {"db": db, "User": User}
