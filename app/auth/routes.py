#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run by pyserver
from functools import wraps

from flask import render_template as template, request, redirect
from flask import flash

from flask_login import login_user, logout_user, current_user

from app import models
from app import application, login

from app.auth.forms import LoginForm, RegisterForm


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.username != 'admin':
            return redirect('/wrongpage')
        return f(*args, **kwargs)
    return decorated_function


@application.route('/login', methods=['GET', 'POST'])
@login.unauthorized_handler
def showLogin():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return template('auth/login.tpl', form=form)
    elif request.method == 'POST':
        if not form.validate_on_submit():
            return template('auth/login.tpl', form=form)
        if doLogin(form.username.data, form.password.data.encode('utf-8')):
            return redirect('/dashboard')
        else:
            return template('auth/login.tpl', form=form)


def doLogin(username, password, from_register=False):
    user = models.User.load(username)
    if user is not None and user.checkLogin(password):
        login_user(user, remember=True)
        if not from_register:
            flash('Byl jste úspěšně přihlášen.', 'success')
        return True
    else:
        flash('Přihlášení se nezdařilo.', 'error')
        return False


@application.route('/logout')
def doLogout():
    logout_user()
    flash('Byl jste úspěšně odhlášen.', 'info')
    return redirect('/login')


@application.route('/register', methods=['GET', 'POST'])
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
            return template('auth/register.tpl', form=form)

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
            return template('auth/register.tpl', form=form)


def doRegister(user):
    if user.save() is not None:
        doLogin(user.username, user.password.encode('utf-8'), from_register=True)
        flash('Byl jste úspěšně zaregistrován.', 'success')
        return True
    else:
        flash('Registrace neproběhla v pořádku', 'error')
        return False


@application.route('/registerValidate', methods=['POST'])
def validateRegister(username):
    if models.User.load(username) is not None:
        return False
    else:
        return True
