from flask import current_app as application
from flask import render_template as template
from flask import abort, make_response

from flask_classful import FlaskView

from app.auth import admin_required


class ErrorsView(FlaskView):
    def wrongpage(self):
        abort(405)

    def shutdown(self):
        return template("errors/shutdown.tpl")

    # REFACTOR only for testing
    @admin_required
    def err404(self):
        return template("errors/err404.tpl")

    @admin_required
    def err405(self):
        return template("errors/err405.tpl")

    @admin_required
    def err500(self):
        return template("errors/err500.tpl")


def error404(error):
    # Missing page
    application.logger.info(error)
    return make_response(template("errors/err404.tpl"), 404)


def error405(error=None):
    # Action not allowed
    application.logger.info(error)
    return make_response(template("errors/err405.tpl"), 405)


def error500(error):
    # Internal error
    application.logger.error(error)
    return make_response(template("errors/err500.tpl"), 500)
