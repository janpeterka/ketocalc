#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run by pyserver
from flask import Blueprint
from flask import render_template as template
from flask import abort

from flask_login import login_required

from app.auth.routes import admin_required

# from app.errors import bp as errors

errors_blueprint = Blueprint('errors', __name__)


# ERROR
@errors_blueprint.route('/wrongpage')
def wrongPage():
    abort(405)


@errors_blueprint.route('/shutdown')
def shutdown():
    return template('errors/shutdown.tpl')


@errors_blueprint.route('/testing')
@login_required
@admin_required
def testingPage():
    tests = []
    # tests.append()
    return template('other/testing.tpl', tests=tests)


@errors_blueprint.route('/logging')
@login_required
@admin_required
def logPage():
    with open('app/static/error.log', 'r') as f:
        logs = f.readlines()

    return template('other/logs.tpl', logs=logs)


# @errors_blueprint.route('/terms')
# def showTerms():
#     return template('other/terms.tpl')


# @errors_blueprint.route('/privacy')
# def showPrivacy():
#     return template('other/privacy.tpl')


@errors_blueprint.route('/google3748bc0390347e56.html')
def googleVerification():
    return template('other/google3748bc0390347e56.html')


@errors_blueprint.app_errorhandler(404)
def error404(error):
    # Missing page
    return template('errors/err404.tpl')


@errors_blueprint.errorhandler(405)
def error405(error=None):
    # Action not allowed
    return template('errors/wrongPage.tpl')


@errors_blueprint.errorhandler(500)
def error500(error):
    # Internal error
    return template('errors/err500.tpl')
