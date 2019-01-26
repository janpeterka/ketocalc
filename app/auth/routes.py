#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run by pyserver
from functools import wraps
import datetime

from flask import render_template as template, request, redirect, Blueprint
from flask import flash

from flask_login import login_user, logout_user, current_user

from app import models

from app.auth.forms import LoginForm, RegisterForm

from app.data import template_data

auth_blueprint = Blueprint('auth', __name__, template_folder='templates/auth/')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.username != 'admin':
            return redirect('/wrongpage')
        return f(*args, **kwargs)
    return decorated_function


@auth_blueprint.app_context_processor
def inject_globals():
    return dict(icons=template_data.icons, texts=template_data.texts)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def showLogin():
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


def doLogin(username=None, password=None, from_register=False, user=None):
    if not user and username is not None:
        user = models.User.load(username)
    if user is not None and (user.google_id is not None or user.checkLogin(password)):
        login_user(user, remember=True)
        user.last_logged_in = datetime.datetime.now()
        user.save()
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
            print("Not validated")
            return template('auth/register.tpl', form=form)
        if not validateRegister(form.username.data):
            form.username.errors += ('Toto jméno nemůžete použít')
            return template('register.tpl', form=form)

        user = models.User()

        user.username = form.username.data
        user.firstName = form.first_name.data
        user.lastName = form.last_name.data
        user.password = form.password.data
        user.pwdhash = user.getPassword(form.password.data.encode('utf-8'))
        user.password_version = 'bcrypt'

        if doRegister(user):
            return redirect('/dashboard')
        else:
            return template('register.tpl', form=form)


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
    if models.User.load(username) is not None:
        return False
    else:
        return True
