#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run by pyserver


from functools import wraps
import datetime

from flask import Blueprint
from flask import render_template as template, request, redirect
from flask import flash
from flask import current_app as application

from flask_login import login_user, logout_user, current_user

from flask_dance.contrib.google import google
from flask_dance.consumer import oauth_authorized


from app import models

from app.auth.forms import LoginForm, RegisterForm


auth_blueprint = Blueprint('auth', __name__, template_folder='templates/auth/')

PASSWORD_VERSION = 'bcrypt'


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if current_user.username != 'admin':
            return redirect('/wrongpage')
        return f(*args, **kwargs)
    return decorated_function


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def showLogin():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    form = LoginForm(request.form)
    if request.method == 'GET':
        return template('auth/login.tpl', form=form)
    elif request.method == 'POST':
        if not form.validate_on_submit():
            return template('auth/login.tpl', form=form)
        if doLogin(username=form.username.data, password=form.password.data.encode('utf-8')):
            return redirect('/dashboard')
        else:
            return template('auth/login.tpl', form=form)


@oauth_authorized.connect
def oauthLogin(blueprint, token):
    try:
        if blueprint.name == 'google':
            user_info = google.get("/oauth2/v2/userinfo").json()
            username = user_info['email']
            google_id = user_info['id']
    except Exception as e:
        application.logger.error(e)

    user = models.User.load(username, load_type="username")
    doLogin(user=user)
    if not user:
        user = models.User.load(google_id, load_type="google_id")
        doLogin(user=user)
    if not user:
        user = models.User()
        user.username = username
        user.password = None
        user.google_id = google_id

        try:
            user.first_name = user_info['given_name']
        except Exception:
            user.first_name = "-"

        try:
            user.last_name = user_info['family_name']
        except Exception:
            user.last_name = "-"

        doRegister(user)


def doLogin(username=None, password=None, from_register=False, user=None):
    if not user and username is not None:
        user = models.User.load(username, load_type="username")
    if user is not None and (user.google_id is not None or user.checkLogin(password)):
        login_user(user, remember=True)
        if application.config['APP_STATE'] == 'production':
            user.last_logged_in = datetime.datetime.now()
            try:
                user.login_count += 1
            except Exception:
                user.login_count = 1
            user.edit()
        if not from_register:
            flash('Byl jste úspěšně přihlášen.', 'success')
        return True
    else:
        flash('Přihlášení se nezdařilo.', 'error')
        return False


@auth_blueprint.route('/logout')
def doLogout():
    logout_user()
    flash('Byl jste úspěšně odhlášen.', 'info')
    return redirect('/login')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def showRegister():
    form = RegisterForm(request.form)
    if request.method == 'GET':
        return template('auth/register.tpl', form=form)
    elif request.method == 'POST':
        if not form.validate_on_submit():
            return template('auth/register.tpl', form=form)
        if not validateRegister(form.username.data):
            form.username.errors = ['Toto jméno nemůžete použít']
            return template('auth/register.tpl', form=form)

        user = models.User()
        form.populate_obj(user)
        # user.username = form.username.data
        # user.first_name = form.first_name.data
        # user.last_name = form.last_name.data
        # user.password = form.password.data
        user.pwdhash = user.getPassword(form.password.data.encode('utf-8'))
        user.password_version = PASSWORD_VERSION

        if doRegister(user):
            return redirect('/dashboard')
        else:
            return template('auth/register.tpl', form=form)


def doRegister(user):
    if user.save() is not None:
        doLogin(username=user.username, password=user.password.encode('utf-8'), from_register=True)
        flash('Byl jste úspěšně zaregistrován.', 'success')
        return True
    else:
        flash('Registrace neproběhla v pořádku', 'error')
        return False


@auth_blueprint.route('/registerValidate', methods=['POST'])
def validateRegister(username):
    """[summary]

    Tests for usename uniqueness

    Decorators:
        auth_blueprint.route

    Arguments:
        username {[type]} -- [description]

    Returns:
        bool -- [description]
    """
    if models.User.load(username, load_type="username") is not None:
        return False
    else:
        return True
