#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
from bottle import route, template
from bottle import error, redirect
from bottle import get, post, request
from bottle import static_file


# import pymysql
# import pymysql.cursors


# def connectDb():
#     connection = pymysql.connect(host='localhost',
#                                  user='root',
#                                  password='mainframe',
#                                  db='uirdr',
#                                  charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor)
#     return (connection)


# def selectAll():		# to edit
#     connection = connectDb()

#     try:
#         with connection.cursor() as cursor:
#             sql = "SELECT * from users"
#             # print("sending: " + sql)
#             cursor.execute(sql)
#             # print("sent: " + sql)
#             result = cursor.fetchall()  # vrací jen první položku databáze :(
#             # print(result)
#     finally:
#         connection.close()

#     return (result)


def check_login(username, password):
    if username == password:
        return True
    else:
        return False
# MAIN


@route('/')
def main():
    return 'Welcome home.'


@route('/index.html')  # NOT WORKING
def index():
    return static_file("index.html", root='/')


# LOGIN FORM

@get('/login')  # or @route('/login')
def login():
    return '''
        <form action="./login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''


@post('/login')  # or @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"


# UIRDR
@route('/kraje')
def showKraje():
    kraje = ""  # TODO get kraje from database
    message = ""
    for kraj in kraje:
        message += template('<span>{{kraj.name}}</span>', krajName=kraj.name)


@route('/kraj/<krajID>')
def showKraj(krajID):
    okresy = ""  # TODO get okresy from database by krajID
    message = ""
    message += template('<a href=/kraje>Zpět na kraje</a>')

    for okres in okresy:
        message += template('<a href=/okres/{{okres.id}}>okres.name</a>', okresId=okres.id)
    return message


@route('/okres/<okresID>')
def showOkres(okresID):
    obce = ""  # TODO get obce from database by okresID
    kraj = ""  # TODO get krajID by okresID
    message = ""
    message += template('<a href=/kraj/{{kraj.id}}>Zpět na kraj</a>', krajId=kraj.id)
    for obec in obce:
        message += template('<span>{{obec.name}}</span>', obecName=obec.name)
    return message


# ERROR


@error(404)
def error404(error):
    return 'Nothing here, sorry. (Err404)'


@error(500)
def error500(error):
    return 'Something went wrong! (Err500)'


application = bottle.default_app()
