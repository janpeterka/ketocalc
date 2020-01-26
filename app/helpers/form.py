from werkzeug import MultiDict

from flask import session

from app.controllers.forms.diets import *
from app.controllers.forms.ingredients import *
from app.controllers.forms.feedback import *
from app.controllers.forms.login import *
from app.controllers.forms.password_recovery import *
from app.controllers.forms.register import *


def create_form(form_name):
    form_data = None
    if session.get("formdata") is not None:
        form_data = MultiDict(session.get("formdata"))
        session.pop("formdata")

    if form_data:
        klass = globals()[str(form_name)]
        form = klass(form_data)
        form.validate()
    else:
        klass = globals()[str(form_name)]
        form = klass()

    return form
