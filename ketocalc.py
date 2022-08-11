import os
import re
import time

from flask import request, redirect, session, g

from flask_login import current_user

from app import create_app
from app import db
import cli

# from app.models import db
# from app.models.users import User
from app.models.request_log import RequestLog

from app.data import template_data

from app.handlers.data import DataHandler


env = os.environ.get("APP_STATE", "default")
application = create_app(config_name=env)

cli.register(application)


@application.before_request
def sentry_add_user():
    from sentry_sdk import set_user
    from flask_security import current_user

    if current_user.is_authenticated:
        set_user({"id": current_user.id, "username": current_user.full_name})


@application.context_processor
def inject_globals():
    return dict(texts=template_data.texts)


@application.before_request
def session_management():
    current_user.logged_from_admin = session.get("logged_from_admin")

    if application.config["APP_STATE"] == "shutdown" and request.path not in [
        "/shutdown",
        "/static/css/style.css",
    ]:
        return redirect("/shutdown")
    elif request.path == "/shutdown" and application.config["APP_STATE"] != "shutdown":
        return redirect("/")


@application.before_request
def log_request_start():
    g.log_request_start_time = time.time()


@application.teardown_request
def log_request(exception=None):
    # if application.config["APP_STATE"] == "development":
    #     return
    db.session.expire_all()
    pattern = re.compile("/static/")
    if not pattern.search(request.path):
        user_id = getattr(current_user, "id", None)

        item_type = DataHandler.get_additional_request_data("item_type")
        item_id = DataHandler.get_additional_request_data("item_id")

        log = RequestLog(
            url=request.path,
            user_id=user_id,
            remote_addr=request.environ["REMOTE_ADDR"],
            item_type=item_type,
            item_id=item_id,
            duration=time.time() - g.log_request_start_time,
        )
        log.save()


# @application.shell_context_processor
# def make_shell_context():
#     return {"db": db, "User": User}
