#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run by pyserver
from flask import Blueprint
from flask import render_template as template
from flask import abort
from flask import current_app as application

# from app.errors import bp as errors
from app.auth import admin_required

errors_blueprint = Blueprint('errors', __name__)


@errors_blueprint.route('/wrongpage')
def show_wrongpage():
    abort(405)


@errors_blueprint.route('/shutdown')
def shutdown():
    return template('errors/shutdown.tpl')


# REFACTOR only for testing
@errors_blueprint.route('/err404')
@admin_required
def show_error404():
    return template('errors/err404.tpl')


@errors_blueprint.route('/err405')
@admin_required
def show_error405():
    return template('errors/err405.tpl')


@errors_blueprint.route('/err500')
@admin_required
def show_error500():
    return template('errors/err500.tpl')


@errors_blueprint.app_errorhandler(404)
def error404(error):
    # Missing page
    application.logger.info(error)
    return template('errors/err404.tpl')


@errors_blueprint.errorhandler(405)
def error405(error=None):
    # Action not allowed
    application.logger.info(error)
    return template('errors/err405.tpl')


@errors_blueprint.errorhandler(500)
def error500(error):
    # Internal error
    application.logger.error(error)
    return template('errors/err500.tpl')
