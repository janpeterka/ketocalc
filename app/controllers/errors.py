from flask import current_app as application
from flask import render_template as template
from flask import abort, make_response

from flask_classful import FlaskView

from app.auth import admin_required


class ErrorsView(FlaskView):
    @admin_required
    def raise_error(self):
        abort(500)

    def wrongpage(self):
        abort(405)

    def shutdown(self):
        return template("errors/shutdown.html.j2")

    # only for testing
    @admin_required
    def err404(self):
        return template("errors/err404.html.j2")

    @admin_required
    def err405(self):
        return template("errors/err405.html.j2")

    @admin_required
    def err500(self):
        return template("errors/err500.html.j2")


def error404(error):
    # Missing page
    # application.logger.info(str(error))
    return template("errors/err404.html.j2"), 404


def error405(error=None):
    # Action not allowed
    # application.logger.info(str(error))
    return make_response(template("errors/err405.html.j2"), 405)


def error500(error):
    # Internal error
    application.logger.error(str(error))
    return make_response(template("errors/err500.html.j2"), 500)
