#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run by pyserver

from flask import render_template as template
from flask import abort

from flask_login import login_required

from app.auth.routes import admin_required

from app.errors import bp as errors


# ERROR
@errors.route('/wrongpage')
def wrongPage():
    abort(405)


@errors.route('/shutdown')
def shutdown():
    return template('errors/shutdown.tpl')


@errors.route('/testing')
@login_required
@admin_required
def testingPage():
    tests = []
    # tests.append()
    return template('other/testing.tpl', tests=tests)


@errors.route('/google3748bc0390347e56.html')
def googleVerification():
    return template('other/google3748bc0390347e56.html')


@errors.app_errorhandler(404)
def error404(error):
    # Missing page
    return template('errors/err404.tpl')


@errors.app_errorhandler(405)
def error405(error=None):
    # Action not allowed
    return template('errors/wrongPage.tpl')


@errors.app_errorhandler(500)
def error500(error):
    # Internal error
    return template('errors/err500.tpl')
