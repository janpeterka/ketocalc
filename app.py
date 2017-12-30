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

# Math library
import numpy
import math

from sys import argv

# dev var - LOCAL / DEPLOY
# APP_MODE = "LOCAL"
APP_MODE = "DEPLOY"

# bottle.TEMPLATE_PATH = "~/Dropbox/Programming/PyServer/views/"
# bottle.TEMPLATE_PATH.insert(0, '/home/jan/Dropbox/Programming/KetoCalc')

bottle.TEMPLATE_PATH.insert(0, '/home/jan/Dropbox/Programming/ketoCalc/views')
bottle.TEMPLATE_PATH.insert(0, './views')

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 60000,
    'session.data_dir': './data',
    'session.auto': True
}

beaker_app = SessionMiddleware(bottle.app(), session_opts)


def temp_print(input):
    print(input)


class Diet(object):
    """  For loading from database """

    def __init__(self, dbID, name, sugar, fat, protein):
        super(Diet, self).__init__()
        self.id = dbID
        self.name = name
        self.sugar = sugar
        self.fat = fat
        self.protein = protein


class Recipe(object):
    """  For loading from database """

    def __init__(self, dbID, name):
        super(Recipe, self).__init__()
        self.id = dbID
        self.name = name


class Ingredient(object):
    """  For loading from database """

    def __init__(self, dbID, name, sugar, fat, protein):
        super(Ingredient, self).__init__()
        self.id = dbID
        self.name = name
        self.sugar = sugar
        self.fat = fat
        self.protein = protein
        self.amount = 0


class User(object):
    """ For loading from database """

    def __init__(self, tid, username, pwdhash, firstname, lastname):
        super(User, self).__init__()
        self.id = tid
        self.username = username
        self.pwdhash = pwdhash
        self.firstname = firstname
        self.lastname = lastname


# SESSION related functions
def getSession():
    session = bottle.request.environ.get('beaker.session')
    return session


# DATABASE related functions
def dbConnect():
    db = MySQLdb.connect(host='cvktne7b4wbj4ks1.chr7pe7iynqr.eu-west-1.rds.amazonaws.com', port=3306, user='sbn13vkg4k895di1', password='ot7aivfxw37d9tbr', database='nobexi41fwyb1088', charset='utf8', init_command='SET NAMES UTF8')
    return db


# Recipes
def loadRecipe(recipeID):
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM recipes WHERE id='{}';".format(recipeID))
    cursor.execute(query)
    response = cursor.fetchone()
    recipe = Recipe(response[0], response[1])

    query = ("SELECT recipes_has_ingredients.ingredients_id FROM recipes_has_ingredients WHERE recipes_has_ingredients.recipes_id='{}';".format(recipeID))
    cursor.execute(query)
    response = cursor.fetchall()

    ingredientIDs = []
    for i in range(len(response)):
        ingrID = response[i][0]
        ingredientIDs.append(ingrID)

    return [recipe, ingredientIDs]
    """ recipe (Recipe: id, name); ingredientIDs (Array: ingredientID (Int))"""


def saveRecipe(recipe, ingredients, dietID):
    """ recipe (Object: name), ingredients (Array of ingredient (Object: id, amount), dietID (Int)"""

    db = dbConnect()
    cursor = db.cursor()

    """ Save to recipe table """
    query = ("INSERT INTO recipes(name) VALUES ('{}');".format(recipe.name))
    cursor.execute(query)
    last_id = db.insert_id()

    """ Save to recipe/ingredient table"""
    for ingredient in ingredients:
        query = ("INSERT INTO recipes_has_ingredients(recipes_id, ingredients_id, amount) VALUES({}, {}, {})".format(last_id, ingredient.id, ingredient.amount))
        cursor.execute(query)

    """ save to diet/recipe table"""
    query = ("INSERT INTO diets_has_recipes(diets_id, recipes_id) VALUES ({}, {});".format(dietID, last_id))
    cursor.execute(query)

    db.commit()

    return last_id


def deleteRecipe(recipeID):
    db = dbConnect()
    cursor = db.cursor()

    query = ("DELETE FROM diets_has_recipes WHERE diets_has_recipes.recipes_id = {};".format(recipeID))
    cursor.execute(query)

    query = ("DELETE FROM recipes_has_ingredients WHERE recipes_has_ingredients.recipes_id = {};".format(recipeID))
    cursor.execute(query)

    query = ("DELETE FROM recipes WHERE recipes.id = {};".format(recipeID))
    cursor.execute(query)

    db.commit()


def loadUserRecipes(username):
    recipes = []
    diets = loadUserDiets(username)
    for diet in diets:
        temp_recipes = loadDietRecipes(diet.id)
        for recipe in temp_recipes:
            recipes.append(recipe)

    return recipes


def loadRecipeDietID(recipeID):
    db = dbConnect()
    cursor = db.cursor()
    query = ("SELECT diets_has_recipes.diets_id FROM diets_has_recipes WHERE recipes_id='{}';".format(recipeID))
    cursor.execute(query)
    response = cursor.fetchall()

    return response[0][0]


def loadDietRecipes(dietID):
    db = dbConnect()
    cursor = db.cursor()
    query = ("SELECT diets_has_recipes.recipes_id FROM diets_has_recipes WHERE diets_id='{}';".format(dietID))
    cursor.execute(query)
    response = cursor.fetchall()

    recipes = []

    for i in range(len(response)):
        temp_recipe = loadRecipe(response[i][0])[0]    # get only recipe
        recipe = Recipe(temp_recipe.id, temp_recipe.name)
        recipes.append(recipe)

    return recipes
    """ recipe (Recipe: id, name)"""


# Diets
def loadDiet(dietID):
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM diets WHERE id='{}';".format(dietID))
    cursor.execute(query)
    response = cursor.fetchone()

    diet = Diet(response[0], response[1], response[2], response[3], response[4])

    return diet
    """ diet (Diet: id, name, sugar, fat, protein) """


def saveDiet(diet):             # diet as object (name, sugar, fat, protein)
    db = dbConnect()
    cursor = db.cursor()

    query = ("INSERT INTO diets(name, sugar, fat, protein) VALUES ('{}', '{}', '{}', '{}');".format(diet.name, diet.sugar, diet.fat, diet.protein))
    cursor.execute(query)

    last_id = db.insert_id()
    query = ("INSERT INTO users_has_diets(users_id, diets_id) VALUES ('{}', '{}');".format(loadUser(diet.username).id, last_id))
    cursor.execute(query)

    db.commit()

    return last_id


def deleteDietCheck(dietID):
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT diets_has_recipes.recipes_id FROM diets_has_recipes WHERE diets_has_recipes.diets_id = {};".format(dietID))
    cursor.execute(query)
    response = cursor.fetchall()
    if len(response) == 0:
        return True
    else:
        return False


def deleteDiet(dietID):
    db = dbConnect()
    cursor = db.cursor()

    # recipes in diet are not accessible, but not deleted
    query = ("DELETE FROM diets_has_recipes WHERE diets_has_recipes.diets_id = {};".format(dietID))
    cursor.execute(query)

    query = ("DELETE FROM users_has_diets WHERE users_has_diets.diets_id = {};".format(dietID))
    cursor.execute(query)

    query = ("DELETE FROM diets WHERE diets.id = {};".format(dietID))
    cursor.execute(query)

    db.commit()


def loadUserDiets(username):
    db = dbConnect()
    cursor = db.cursor()
    temp_query = ("SELECT users.id FROM users WHERE users.username = '{}';".format(username))
    cursor.execute(temp_query)
    user_id = cursor.fetchone()

    query = ("SELECT diets.id, diets.name, diets.sugar, diets.fat, diets.protein FROM diets JOIN users_has_diets ON diets.id=users_has_diets.diets_id WHERE users_has_diets.users_id= '{}' ;".format(user_id[0]))
    cursor.execute(query)
    response = cursor.fetchall()

    # convert to array of objects
    diets = []
    for i in range(len(response)):
        temp_diet = Diet(response[i][0], response[i][1], response[i][2], response[i][3], response[i][4], )
        diets.append(temp_diet)

    return diets


# Ingredients
def loadAllIngredients(username):
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM ingredients WHERE author='{}';".format(username))
    cursor.execute(query)
    response = cursor.fetchall()

    # ingredients = []
    # for i in response:
    #     ingredient = Ingredient(i[0], i[1], i[2], i[3], i[4])
    #     ingredients.append(ingredient)

    temp_ingredients = []
    for ingredient in response:
        temp_ingredient = Ingredient(ingredient[0], ingredient[1], ingredient[2], ingredient[3], ingredient[4])
        temp_ingredients.append(temp_ingredient)

    temp_ingredients.sort(key=lambda x: x.name)
    temp_ingredients = sorted(temp_ingredients, key=lambda x: x.name)

    return temp_ingredients


def loadIngredient(ingredientID):
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM ingredients WHERE id='{}';".format(int(ingredientID)))
    cursor.execute(query)
    response = cursor.fetchone()

    ingredient = Ingredient(response[0], response[1], response[2], response[3], response[4])

    return ingredient


def loadAmount(ingredientID, recipeID):
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT amount FROM recipes_has_ingredients WHERE recipes_has_ingredients.ingredients_id = '{}' AND recipes_has_ingredients.recipes_id = '{}'".format(ingredientID, recipeID))
    cursor.execute(query)
    response = cursor.fetchone()

    return response


def saveIngredient(ingredient, username):  # ingredient as object (name, sugar, fat, protein)
    db = dbConnect()
    cursor = db.cursor()

    query = ("INSERT INTO ingredients(name, sugar, fat, protein, author) VALUES ('{}', '{}', '{}', '{}', '{}');".format(ingredient.name, ingredient.sugar, ingredient.fat, ingredient.protein, username))
    cursor.execute(query)
    last_id = db.insert_id()

    db.commit()

    return last_id


def deleteIngredientCheck(ingredientID):
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT recipes_has_ingredients.recipes_id FROM recipes_has_ingredients WHERE recipes_has_ingredients.ingredients_id = {};".format(ingredientID))
    cursor.execute(query)
    response = cursor.fetchall()
    if len(response) == 0:
        return True
    else:
        return False


def deleteIngredient(ingredientID):
    db = dbConnect()
    cursor = db.cursor()

    query = ("DELETE FROM recipes_has_ingredients WHERE recipes_has_ingredients.ingredients_id= {};".format(ingredientID))
    cursor.execute(query)
    query = ("DELETE FROM ingredients WHERE ingredients.id = {};".format(ingredientID))
    cursor.execute(query)
    db.commit()


# Users
def saveUser(username, password_hash, firstname, lastname):
    db = dbConnect()
    cursor = db.cursor()

    query = ("INSERT INTO users(username, pwdhash, firstName, lastName) VALUES ('{}', '{}', '{}', '{}');".format(username, password_hash, firstname, lastname))
    cursor.execute(query)

    db.commit()

    return cursor.rowcount


def loadUser(username):
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM users WHERE username='{}';".format(username))
    cursor.execute(query)

    response = cursor.fetchone()

    if response is None:
        return None
    else:
        return User(response[0], response[1], response[2], response[3], response[4])


# MAIN

@route('/')
def main():
    if getSession().get('username') is not None:
        redirect('/user')
    else:
        redirect('login')


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
    username = request.forms.username
    password = request.forms.password
    if check_login(username, password):
        # return "<p>Your login information was correct.</p>"
        session = getSession()
        session['username'] = username
        session.save()
        redirect('/user')
    else:
        return False


def check_login(username, password):
    user = loadUser(username)
    if user is None:
        return False

    pwdhash = user.pwdhash

    temp_password = password.encode('utf-8')
    password_hash = hashlib.sha256(temp_password).hexdigest()

    if password_hash == pwdhash:
        return True
    else:
        return False


@route('/logout')
def logout():
    session = getSession()
    session['username'] = None
    session.save()
    redirect('/login')


@get('/register')
def register():
    return template('registerForm', username="", firstname="", lastname="", problem="")


@post('/register')
def do_register():
    username = request.forms.username
    # check uniquness of username

    temp_password = str(request.forms.password)
    temp_password_2 = str(request.forms.againPassword)

    password_hash = hashlib.sha256(temp_password).hexdigest()
    firstname = request.forms.firstname

    lastname = request.forms.lastname

    problem = ""

    if len(lastname) == 0:
        problem = "Příjmení je příliš krátké"
    if len(firstname) == 0:
        problem = "Jméno je příliš krátké"
    if len(temp_password) < 8:
        problem = "Heslo je příliš krátké"
    if temp_password_2 != temp_password:
        problem = "Hesla jsou rozdílná!"
    if loadUser(username) is not None:
        problem = "Uživatelské jméno nelze použít"

    if problem != "":
        return template('registerForm', username=username, firstname=firstname, lastname=lastname, problem=problem)

    response = saveUser(username, password_hash, firstname, lastname)

    if response == 1:
        redirect('/login')
    else:
        return template('failure', problem="Registrace neproběhla v pořádku")


@post('/registerValidate')
def validateRegister():
    username = request.forms.username
    if loadUser(username) is not None:
        return "False"
    else:
        return "True"

# USER PAGE


@route('/user')
def user():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    diets = loadUserDiets(session['username'])
    user = loadUser(session['username'])
    return template('userPage', username=session['username'], diets=diets, firstname=user.firstname)


@route('/selectDietAJAX', method='POST')
def selectDietAJAX():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    dietID = request.forms.selectDiet
    recipes = loadDietRecipes(dietID)

    for i in range(len(recipes)):
        recipe = recipes[i]
        json_recipe = {'id': recipe.id, 'name': recipe.name}
        recipes[i] = json_recipe

    array_recipes = {'array': recipes, 'dietID': dietID}
    return array_recipes


# NEW DIET
@get('/newdiet')
def newDietShow():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    return template('newDietPage', name="", sugar="", fat="", protein="", problem="")


@post('/newdiet')
def addDietAJAX():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    diet = type('', (), {})()               # Magický trik, jak udělat prázdný objekt
    diet.name = request.forms.name
    diet.sugar = request.forms.sugar
    diet.fat = request.forms.fat
    diet.protein = request.forms.protein

    problem = ""

    if len(diet.protein) == 0:
        problem = "Vyplňte množství bílkoviny"
    if len(diet.fat) == 0:
        problem = "Vyplňte množství tuku"
    if len(diet.sugar) == 0:
        problem = "Vyplňte množství sacharidů"
    if len(diet.name) == 0:
        problem = "Vyplňte název"

    if problem != "":
        return template('newDietPage', name=diet.name, sugar=diet.sugar, fat=diet.fat, protein=diet.protein, problem=problem)

    diet.username = session['username']
    last_id = saveDiet(diet)
    redirect('/diet={}'.format(last_id))


# SHOW DIET PAGE
@route('/diet=<dietID>')
def showDiet(dietID):
    session = getSession()
    if session.get('username') is None:
        redirect('/login')

    diet = loadDiet(dietID)
    recipes = loadDietRecipes(diet.id)

    return template('dietPage', diet=diet, recipes=recipes)


@route('/diet=<dietID>/remove', method='POST')
def removeDiet(dietID):
    if deleteDietCheck(dietID):  # wip
        deleteDiet(dietID)
        redirect("/user")
    else:
        return template('failure', problem="Tato dieta má recepty, nelze smazat")


@route('/alldiets')
def allDiets():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')

    diets = loadUserDiets(session['username'])
    return template('allDietsPage', diets=diets)


# NEW RECIPE PAGE
@route('/newrecipe')
def newRecipe():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')

    diets = loadUserDiets(session['username'])
    ingredients = loadAllIngredients(session['username'])
    return template('newRecipePage', ingredients=ingredients, diets=diets, problem="")


@route('/addIngredientAJAX', method='POST')
def addIngredienttoRecipeAJAX():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    ingredient = loadIngredient(request.forms.ingredient)
    json_ingredient = {'id': ingredient.id, 'name': ingredient.name, 'sugar': ingredient.sugar, 'fat': ingredient.fat, 'protein': ingredient.protein}
    return json_ingredient


@route('/calcRecipeAJAX', method='POST')
def calcRecipeAJAX():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')

    ingredients = request.forms.ingredientsArray
    ingredients = [word.strip() for word in ingredients.split(',')]

    dietID = request.forms.recipeDiet

    temp_ingredients = []
    for i in range(len(ingredients)):
        ingredient = loadIngredient(ingredients[i])
        temp_ingredients.append(ingredient)

    amounts = calc(temp_ingredients, loadDiet(dietID))

    for i in range(len(ingredients)):
        ingredient = loadIngredient(ingredients[i])
        json_ingredient = {'id': ingredient.id, 'name': ingredient.name, 'sugar': ingredient.sugar, 'fat': ingredient.fat, 'protein': ingredient.protein, 'amount': math.ceil(amounts[i] * 100) / 100}
        ingredients[i] = json_ingredient

    array_ingredients = {'array': ingredients, 'dietID': dietID}
    return array_ingredients


@route('/saveRecipeAJAX', method='POST')
def addRecipeAJAX():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')

    dietID = request.forms.selectedDietID

    temp_ingredients = request.forms.ingredientsArray2
    temp_ingredients = [word.strip() for word in temp_ingredients.split(',')]

    amounts = request.forms.ingredientsAmount2
    amounts = [word.strip() for word in amounts.split(',')]

    ingredients = []
    for i in range(len(temp_ingredients)):
        ingredient = type('', (), {})()
        ingredient.id = temp_ingredients[i]
        ingredient.amount = amounts[i]
        ingredients.append(ingredient)

    recipe = type('', (), {})()
    recipe.name = request.forms.recipeName
    last_id = saveRecipe(recipe, ingredients, dietID)
    redirect('/recipe=' + str(last_id))


@route('/recipe=<recipeID>')
def showRecipe(recipeID):
    recipe = loadRecipe(recipeID)[0]
    ingredientIDs = loadRecipe(recipeID)[1]
    ingredients = []
    for ID in ingredientIDs:
        ingredients.append(loadIngredient(ID))
    for i in ingredients:
        i.amount = float(loadAmount(i.id, recipeID)[0])

    return template('recipePage', recipe=recipe, ingredients=ingredients)


@route('/recipe=<recipeID>/remove', method='POST')
def removeRecipe(recipeID):
    deleteRecipe(recipeID)
    redirect('/user')


@route('/allrecipes')
def allrecipes():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    recipes = loadUserRecipes(session['username'])
    for recipe in recipes:
        recipe.dietID = loadRecipeDietID(recipe.id)
        recipe.dietName = loadDiet(recipe.dietID).name

    return template("allRecipesPage", recipes=recipes)


# NEW INGREDIENT PAGE
@get('/newingredient')
def newingredient():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    return template('newIngredientPage', name="", sugar="", fat="", protein="", problem="")


@post('/newIngredient')
def newIngredienttoRecipeAJAX():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')

    ingredient = type('', (), {})()
    ingredient.name = request.forms.name
    ingredient.sugar = request.forms.sugar
    ingredient.fat = request.forms.fat
    ingredient.protein = request.forms.protein

    problem = ""
    if len(ingredient.protein) == 0:
        problem = "Zadejte množství bílkoviny"
    if len(ingredient.fat) == 0:
        problem = "Zadejte množství tuku"
    if len(ingredient.sugar) == 0:
        problem = "Zadejte množství sacharidů"
    if len(ingredient.name) == 0:
        problem = "Zadejte název suroviny"

    if problem != "":
        return template('newIngredientPage', name=ingredient.name, sugar=ingredient.sugar, fat=ingredient.fat, protein=ingredient.protein, problem=problem)

    saveIngredient(ingredient, session['username'])
    redirect('/newrecipe')


@route('/ingredient=<ingredientID>')
def showingredient(ingredientID):
    ingredient = loadIngredient(ingredientID)
    return template('ingredientPage', ingredient=ingredient)


@route('/ingredient=<ingredientID>/remove', method='POST')
def removeIngredient(ingredientID):
    if deleteIngredientCheck(ingredientID):  # wip
        deleteIngredient(ingredientID)
        redirect("/user")
    else:
        return template('failure', problem="Tato surovina je použita, nelze smazat")


@route('/allingredients')
def allingredients():
    session = getSession()
    if session.get('username') is None:
        redirect('/login')
    ingredients = loadAllIngredients(session['username'])
    return template("allIngredientsPage", ingredients=ingredients)
# CALCULATE RECIPE


# Calc for 3 ingredients
def calc(ingredients, diet):
    # if len(ingredients) == 0:  # wip
    #     return None
    # if len(ingredients) == 1:  # wip
    #     return [1, 2]
    # if len(ingredients) == 2:  # wip
    #     return [1, 2, 3]
    if len(ingredients) == 3:  # wip
        a = numpy.array([[ingredients[0].sugar, ingredients[1].sugar, ingredients[2].sugar],
                         [ingredients[0].fat, ingredients[1].fat, ingredients[2].fat],
                         [ingredients[0].protein, ingredients[1].protein, ingredients[2].protein]])
        b = numpy.array([diet.sugar, diet.fat, diet.protein])
        x = numpy.linalg.solve(a, b)
        return [x[0], x[1], x[2]]
    else:
        temp_array = []
        for i in range(len(ingredients)):
            temp_array.append(1)
        return temp_array


# S'MORE
@route('/index.html')
def indexhtml():
    redirect('/')


@route('/changelog')
def changelog():
    return template('changelog')


# ERROR
@error(404)
def error404(error):
    return 'Nothing here, sorry. (Err404)'


@error(500)
def error500(error):
    return 'Something went wrong! (Err500) <br>' + str(error)


# application = bottle.default_app()
# bottle.run(app=app)

if APP_MODE == "LOCAL":
    bottle.run(host='127.0.0.1', port=8080, app=beaker_app)
elif APP_MODE == "DEPLOY":
    bottle.run(host='0.0.0.0', port=argv[1], app=beaker_app)
