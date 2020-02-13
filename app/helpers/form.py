from werkzeug.utils import MultiDict

from flask import session

from app.controllers.forms.diets import *
from app.controllers.forms.ingredients import *
from app.controllers.forms.feedback import *
from app.controllers.forms.login import *
from app.controllers.forms.password_recovery import *
from app.controllers.forms.register import *


def create_form(form_class):
    form_data = None
    if session.get("formdata") is not None:
        form_data = MultiDict(session.get("formdata"))
        session.pop("formdata")

    if form_data:
        form = form_class(form_data)
        form.validate()
    else:
        form = form_class()

    return form


def save_form_to_session(form_data):
    session["formdata"] = form_data
