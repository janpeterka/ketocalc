#!/usr/bin/env python
# -*- coding: utf-8 -*-


# run by pyserver


import bottle
# from bottle import view
from bottle import route, template
from bottle import error, redirect
from bottle import get, post, request
# from bottle import static_file


# Session manager
from beaker.middleware import SessionMiddleware

# MySQL connector
import MySQLdb

# Hashing library
import hashlib

# bottle.TEMPLATE_PATH = "~/Dropbox/Programming/PyServer/views/"
# bottle.TEMPLATE_PATH.insert(0, '/home/jan/Dropbox/Programming/KetoCalc')

bottle.TEMPLATE_PATH.insert(0, '/home/jan/Dropbox/Programming/KetoCalc/views')

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 600,
    'session.data_dir': './data',
    'session.auto': True
}


class Diet(object):
    """  """

    def __init__(self, dbID, name, sugar, fat, protein):
        super(Diet, self).__init__()
        self.id = dbID
        self.name = name
        self.sugar = sugar
        self.fat = fat
        self.protein = protein


app = SessionMiddleware(bottle.app(), session_opts)


# SESSION related functions
def getSession():
    session = bottle.request.environ.get('beaker.session')
    return session


# DATABASE related functions
def dbConnect():
    db = MySQLdb.connect(user='root', password='mainframe', database='keto_db')

    return db


# Recipes
def loadRecipe(recipeID):
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM recipes WHERE id=" + recipeID + ";")
    cursor.execute(query)
    response = cursor.fetchall()
    # db.commit()
    return response


def saveRecipe(recipe, ingredients):         # recipe as object(name), ingredients as objects (IDs + amounts)
    db = dbConnect()
    cursor = db.cursor()

    query = ("INSERT INTO recipes(name) VALUES ({});".format(recipe.name))
    cursor.execute(query)
    last_id = db.insert_id()
    for ingredient in ingredients:
        query = ("INSERT INTO recipes_has_ingredients(recipes_id, ingredients_id, amount) VALUES('{}', '{}', '{}')".format(last_id, ingredient.id, ingredient.amount))
        cursor.execute(query)

    db.commit()

    return


# def loadUserRecipes(username):
#     db = dbConnect()
#     cursor = db.cursor()

#     query = ("SELECT * FROM recipes JOIN WHERE id=" + recipeID + ";")
#     cursor.execute(query)
#     response = cursor.fetchall()
#     # db.commit()
#     return response

#     SELECT Orders.OrderID, Customers.CustomerName, Orders.OrderDate
# FROM Orders
# INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID;


# Diets
def loadDiet(dietID):
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM diets WHERE id=" + dietID + ";")
    cursor.execute(query)
    response = cursor.fetchall()

    return response


def saveDiet(diet):             # diet as object (name, sugar, fat, protein)
    db = dbConnect()
    cursor = db.cursor()

    query = ("INSERT INTO diets(name, sugar, fat, protein) VALUES ('{}', '{}', '{}', '{}');".format(diet.name, diet.sugar, diet.fat, diet.protein))
    cursor.execute(query)

    last_id = db.insert_id()
    query = ("INSERT INTO users_has_diets(users_id, diets_id) VALUES ('{}', '{}');".format(loadUser(diet.username)[0], last_id))
    cursor.execute(query)

    db.commit()

    return


def loadUserDiets(username):
    db = dbConnect()
    cursor = db.cursor()
    temp_query = ("SELECT users.id FROM users WHERE users.username = '{}';".format(username))
    cursor.execute(temp_query)
    user_id = cursor.fetchone()

    print(user_id[0])

    query = ("SELECT diets.id, diets.name, diets.sugar, diets.fat, diets.protein FROM diets JOIN users_has_diets ON diets.id=users_has_diets.diets_id JOIN users ON users_has_diets.users_id= '{}' ;".format(user_id[0]))
    cursor.execute(query)
    response = cursor.fetchall()

    # convert to array of objects
    diets = []
    for i in range(len(response)):
        temp_diet = Diet(response[i][0], response[i][1], response[i][2], response[i][3], response[i][4], )
        diets.append(temp_diet)

    print(diets)
    return diets

#   SELECT Orders.OrderID, Customers.CustomerName, Orders.OrderDate
#   FROM Orders
#   INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID;
    # pass


# Ingredients
def loadAllIngredients(username):
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM ingredients WHERE author='{}';".format(username))
    cursor.execute(query)
    response = cursor.fetchall()

    return response


def loadIngredient(ingredientID):
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM ingredients WHERE id=" + ingredientID + ";")
    cursor.execute(query)
    response = cursor.fetchone()

    return response


def saveIngredient(ingredient, username):  # ingredient as object (name, sugar, fat, protein)
    db = dbConnect()
    cursor = db.cursor()

    query = ("INSERT INTO ingredients(name, sugar, fat, protein, author) VALUES ('{}', '{}', '{}', '{}', '{}');".format(ingredient.name, ingredient.sugar, ingredient.fat, ingredient.protein, username))
    cursor.execute(query)

    db.commit()

    return


# Users
def saveUser(username, password_hash, firstname, lastname):
    db = dbConnect()
    cursor = db.cursor()

    query = ("INSERT INTO users(username, pwdhash, firstName, lastName) VALUES ('{}', '{}', '{}', '{}');".format(username, password_hash, firstname, lastname))
    cursor.execute(query)

    db.commit()

    # print("affected rows = {}".format(cursor.rowcount))

    return cursor.rowcount


def loadUser(username):
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM users WHERE username=" + "'" + username + "'" + ";")
    cursor.execute(query)

    response = cursor.fetchone()

    return response


# MAIN


@route('/')
def main():
    dbConnect()
    return template('index')


# LOGIN
@get('/login')
def login():
    session = getSession()
    if session.get('username') is not None:
        redirect('/user')
    else:
        return template('loginForm')


@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        # return "<p>Your login information was correct.</p>"
        session = getSession()
        session['username'] = username
        session.save()
        # print(session)
        redirect('/user')
    else:
        return "<p>Login failed.</p>"


def check_login(username, password):
    user = loadUser(username)
    if user is None:
        return False

    pwdhash = user[2]

    temp_password = password.encode('utf-8')
    password_hash = hashlib.sha256(temp_password).hexdigest()

    if password_hash == pwdhash:

        return True
    else:
        return False


@get('/register')
def register():
    # print(getSession())
    return template('registerForm')


@post('/register')
def do_register():
    username = request.forms.get('username')
    temp_password = str(request.forms.get('password')).encode('utf-8')
    password_hash = hashlib.sha256(temp_password).hexdigest()
    firstname = request.forms.get('firstname')
    lastname = request.forms.get('lastname')

    response = saveUser(username, password_hash, firstname, lastname)

    if response == 1:
        redirect('/login')
    else:
        return "Registrace neproběhla v pořádku"

# USER PAGE


@route('/user')
def user():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    username = session['username']
    # recipes = loadUserRecipes(username)
    recipes = []
    return template('userPage', username=username, recipes=recipes)


# NEW DIET
@route('/newdiet')
def newDietShow():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    return template('newDietPage')


@route('/addDietAJAX', method='POST')
def addDietAJAX():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    diet = type('', (), {})()               # Magický trik, jak udělat prázdný objekt
    diet.name = request.forms.get("name")
    diet.sugar = request.forms.get("sugar")
    diet.fat = request.forms.get("fat")
    diet.protein = request.forms.get("protein")
    diet.username = session['username']
    saveDiet(diet)
    redirect('/user')


# EDIT DIET PAGE
@route('/editdiet=<dietID>')
def editDietShow(dietID):
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    return template('')


# NEW RECIPE PAGE
@route('/newrecipe')
def newRecipe():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')

    diets = loadUserDiets(session['username'])
    ingredients = loadAllIngredients(session['username'])
    return template('newRecipePage', ingredients=ingredients, diets=diets)


@route('/addIngredientAJAX', method='POST')
def addIngredienttoRecipeAJAX():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    ingredient = loadIngredient(request.forms.get("ingredient"))
    json_ingredient = {'id': ingredient[0], 'name': ingredient[1], 'sugar': ingredient[2], 'fat': ingredient[3], 'protein': ingredient[4]}
    return json_ingredient


@route('/calcRecipeAJAX', method='POST')
def calcRecipeAJAX():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    return


# NEW INGREDIENT PAGE

@route('/newingredient')
def newingredient():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    return template('newIngredientPage')


@route('/newIngredientAJAX', method='POST')
def newIngredienttoRecipeAJAX():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    ingredient = type('', (), {})()
    ingredient.name = request.forms.get("name")
    ingredient.sugar = request.forms.get("sugar")
    ingredient.fat = request.forms.get("fat")
    ingredient.protein = request.forms.get("protein")
    saveIngredient(ingredient, session['username'])
    redirect('/success')


@route('/success')
def successPage():
    return '''
        Povedlo se! <br>
        <a href=/user>Přehled</a>
        '''
    pass

# CALCULATE RECIPE


# ERROR
@error(404)
def error404(error):
    return 'Nothing here, sorry. (Err404)'


@error(500)
def error500(error):
    return 'Something went wrong! (Err500)'


# application = bottle.default_app()
bottle.run(host='localhost', port=8080, debug=True, app=app)
