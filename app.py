#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run by pyserver

from flask import Flask, render_template as template, request, redirect
from flask import jsonify
from flask import session

# Session manager
# from flask.sessions import SessionInterface
# from beaker.middleware import SessionMiddleware

# MySQL connector
import MySQLdb

# Hashing library
import hashlib

# Math library
import numpy
import sympy as sp
from sympy import solve_poly_inequality as solvei
from sympy import poly
import math


# towards the beginging of the file, soon after imports
app = Flask(__name__)


def temp_print(input):
    print(input)


class Diet(object):
    """  For loading from database """

    def __init__(self, dbID, name, sugar, fat, protein, small_size, big_size):
        super(Diet, self).__init__()
        self.id = dbID
        self.name = name
        self.sugar = sugar
        self.fat = fat
        self.protein = protein
        self.small_size = small_size
        self.big_size = big_size


class Recipe(object):
    """  For loading from database """

    def __init__(self, dbID, name, size):
        super(Recipe, self).__init__()
        self.id = dbID
        self.name = name
        self.size = size


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


# DATABASE related functions
def dbConnect():
    """Connects to database
    Returns:
        database connection
    """
    db = MySQLdb.connect(host='vlvlnl1grfzh34vj.chr7pe7iynqr.eu-west-1.rds.amazonaws.com', port=3306, user='qgqgujt50se6wg97', password='siod5gp2hnuus5dl', database='xlen3bfwr4nk4sr9', charset='utf8', init_command='SET NAMES UTF8')
    return db


# Recipes
def loadRecipe(recipeID):
    """Load recipe and ingredients

    Loads array with recipe and list of its ingredients IDs

    Arguments:
        recipeID {int} -- ID of recipe

    Returns:
        array[Recipe, Array[int]]
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM recipes WHERE id='{}';".format(recipeID))
    cursor.execute(query)
    response = cursor.fetchone()
    recipe = Recipe(response[0], response[1], response[2])

    query = ("SELECT recipes_has_ingredients.ingredients_id FROM recipes_has_ingredients WHERE recipes_has_ingredients.recipes_id='{}';".format(recipeID))
    cursor.execute(query)
    response = cursor.fetchall()

    ingredientIDs = []
    for i in range(len(response)):
        ingredientIDs.append(response[i][0])

    return [recipe, ingredientIDs]


def saveRecipe(recipe, ingredients, dietID):
    """Save recipe to database

    [description]

    Arguments:
        recipe {Recipe} -- recipe to be added
        ingredients {array[Ingredients]} -- array of ingredient in recipe
        dietID {int} -- id of diet for this recipe

    Returns:
        int -- ID of newly added recipe
    """

    db = dbConnect()
    cursor = db.cursor()

    query = ("INSERT INTO recipes(name, type) VALUES ('{}', '{}');".format(recipe.name, recipe.size))
    cursor.execute(query)
    last_id = db.insert_id()

    for ingredient in ingredients:
        query = ("INSERT INTO recipes_has_ingredients(recipes_id, ingredients_id, amount) VALUES({}, {}, {})".format(last_id, ingredient.id, ingredient.amount))
        cursor.execute(query)

    query = ("INSERT INTO diets_has_recipes(diets_id, recipes_id) VALUES ({}, {});".format(dietID, last_id))
    cursor.execute(query)

    db.commit()

    return last_id


def deleteRecipe(recipeID):
    """Delete recipe from database

    Arguments:
        recipeID {int} -- ID of recipe to be removed
    """
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
    """Loads all user's recipes

    Arguments:
        username {str} -- [description]

    Returns:
        array -- all user Recipes
    """
    recipes = []
    diets = loadUserDiets(username)
    for diet in diets:
        temp_recipes = loadDietRecipes(diet.id)
        for recipe in temp_recipes:
            recipes.append(recipe)

    return recipes


def loadRecipeDietID(recipeID):
    """get ID of diet for recipe

    used in allrecipes and showRecipe

    Arguments:
        recipeID {int} -- [description]

    Returns:
        int -- diet.id
    """
    db = dbConnect()
    cursor = db.cursor()
    query = ("SELECT diets_has_recipes.diets_id FROM diets_has_recipes WHERE recipes_id='{}';".format(recipeID))
    cursor.execute(query)
    response = cursor.fetchall()

    return response[0][0]


def loadDietRecipes(dietID):
    """Get all Recipes for Diet

    [description]

    Arguments:
        dietID {int} -- [description]

    Returns:
        array -- array of Recipes
    """
    db = dbConnect()
    cursor = db.cursor()
    query = ("SELECT diets_has_recipes.recipes_id FROM diets_has_recipes WHERE diets_id='{}';".format(dietID))
    cursor.execute(query)
    response = cursor.fetchall()

    recipes = []

    for i in range(len(response)):
        temp_recipe = loadRecipe(response[i][0])[0]    # get only recipe
        recipe = Recipe(temp_recipe.id, temp_recipe.name, temp_recipe.size)  # wip - je to potřeba?
        recipes.append(recipe)

    return recipes


# Diets
def loadDiet(dietID):
    """Get diet by ID

    [description]

    Arguments:
        dietID {int} -- [description]

    Returns:
        diet -- [description]
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM diets WHERE id='{}';".format(dietID))
    cursor.execute(query)
    response = cursor.fetchone()

    diet = Diet(response[0], response[1], response[2], response[3], response[4], response[5], response[6])

    return diet


def saveDiet(diet):
    """[summary]

    [description]

    Arguments:
        diet {Diet} -- [description]

    Returns:
        int -- [description]
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("INSERT INTO diets(name, sugar, fat, protein, small_size, big_size) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(diet.name, diet.sugar, diet.fat, diet.protein, diet.small_size, diet.big_size))
    cursor.execute(query)

    last_id = db.insert_id()
    query = ("INSERT INTO users_has_diets(users_id, diets_id) VALUES ('{}', '{}');".format(loadUser(diet.username).id, last_id))
    cursor.execute(query)

    db.commit()

    return last_id


def deleteDietCheck(dietID):
    """check if diet has recipes

    [description]

    Arguments:
        dietID {int} -- [description]

    Returns:
        bool -- [description]
    """
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
    """Deletes diet

    WIP: makes orphan recipes

    Arguments:
        dietID {int} -- [description]
    """
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
    """Load diets for user

    [description]

    Arguments:
        username {str} -- [description]

    Returns:
        array -- array of Diets
    """
    db = dbConnect()
    cursor = db.cursor()
    temp_query = ("SELECT users.id FROM users WHERE users.username = '{}';".format(username))
    cursor.execute(temp_query)
    user_id = cursor.fetchone()

    query = ("SELECT diets.id, diets.name, diets.sugar, diets.fat, diets.protein, diets.small_size, diets.big_size FROM diets JOIN users_has_diets ON diets.id=users_has_diets.diets_id WHERE users_has_diets.users_id= '{}' ;".format(user_id[0]))
    cursor.execute(query)
    response = cursor.fetchall()

    # convert to array of objects
    diets = []
    for i in range(len(response)):
        temp_diet = Diet(response[i][0], response[i][1], response[i][2], response[i][3], response[i][4], response[i][5], response[i][6],)
        diets.append(temp_diet)

    return diets


# Ingredients
def loadAllIngredients(username):
    """Get all Ingredients for user

    used in newRecipe

    Arguments:
        username {str} -- [description]

    Returns:
        array -- alphabetically sorted array of Ingredients
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM ingredients WHERE author='{}';".format(username))
    cursor.execute(query)
    response = cursor.fetchall()

    temp_ingredients = []
    for ingredient in response:
        temp_ingredient = Ingredient(ingredient[0], ingredient[1], ingredient[2], ingredient[3], ingredient[4])
        temp_ingredients.append(temp_ingredient)

    temp_ingredients.sort(key=lambda x: x.name)
    temp_ingredients = sorted(temp_ingredients, key=lambda x: x.name)

    return temp_ingredients


def loadIngredient(ingredientID):
    """[summary]

    [description]

    Arguments:
        ingredientID {int} -- [description]

    Returns:
        Ingredient -- [description]
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT * FROM ingredients WHERE id='{}';".format(int(ingredientID)))
    cursor.execute(query)
    response = cursor.fetchone()

    ingredient = Ingredient(response[0], response[1], response[2], response[3], response[4])

    return ingredient


def loadAmount(ingredientID, recipeID):
    """[summary]

    [description]

    Arguments:
        ingredientID {int} -- [description]
        recipeID {int} -- [description]

    Returns:
        int -- amount of Ingredinent in Recipe
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT amount FROM recipes_has_ingredients WHERE recipes_has_ingredients.ingredients_id = '{}' AND recipes_has_ingredients.recipes_id = '{}'".format(ingredientID, recipeID))
    cursor.execute(query)
    amount = cursor.fetchone()

    return amount


def saveIngredient(ingredient, username):
    """

    [description]

    Arguments:
        ingredient {Ingredient} -- [description]
        username {str} -- [description]

    Returns:
        int -- [description]
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("INSERT INTO ingredients(name, sugar, fat, protein, author) VALUES ('{}', '{}', '{}', '{}', '{}');".format(ingredient.name, ingredient.sugar, ingredient.fat, ingredient.protein, username))
    cursor.execute(query)
    last_id = db.insert_id()

    db.commit()

    return last_id


def deleteIngredientCheck(ingredientID):
    """[summary]

    [description]

    Arguments:
        ingredientID {int} -- [description]

    Returns:
        bool -- [description]
    """
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
    """[summary]

    WIP: leaves orphan ingredients

    Arguments:
        ingredientID {[type]} -- [description]
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("DELETE FROM recipes_has_ingredients WHERE recipes_has_ingredients.ingredients_id= {};".format(ingredientID))
    cursor.execute(query)
    query = ("DELETE FROM ingredients WHERE ingredients.id = {};".format(ingredientID))
    cursor.execute(query)
    db.commit()


# Users
def saveUser(username, password_hash, firstname, lastname):
    """[summary]

    [description]

    Arguments:
        username {str} -- [description]
        password_hash {str} -- [description]
        firstname {str} -- [description]
        lastname {str} -- [description]

    Returns:
        bool -- success
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("INSERT INTO users(username, pwdhash, firstName, lastName) VALUES ('{}', '{}', '{}', '{}');".format(username, password_hash, firstname, lastname))
    cursor.execute(query)

    db.commit()

    if cursor.rowcount == 1:
        return True
    else:
        return False


def loadUser(username):
    """[summary]

    [description]

    Arguments:
        username {str} -- [description]

    Returns:
        User or None -- [description]
    """
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

@app.before_request
def session_management():
    # make the session last indefinitely until it is cleared
    session.permanent = True


@app.route('/', methods=['GET'])
def main():
    if 'username' not in session:
        return redirect('/user')
    else:
        return redirect('login')


# LOGIN
@app.route('/login', methods=['GET'])
def login():
    if 'username' in session:
        return redirect('/user')
    else:
        return template('loginForm')


@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if check_login(username, password):
        session['username'] = username
        return redirect('/user')
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


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


@app.route('/register', methods=['GET'])
def register():
    return template('registerForm', username="", firstname="", lastname="", problem="")


@app.route('/register', methods=['POST'])
def do_register():
    username = request.form['username']
    # check uniquness of username

    temp_password = str(request.form['password'])
    temp_password_2 = str(request.form['againPassword'])

    password_hash = hashlib.sha256(temp_password.encode('utf-8')).hexdigest()
    firstname = request.form['firstname']

    lastname = request.form['lastname']

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

    if response:
        return redirect('/login')
    else:
        return template('failure', problem="Registrace neproběhla v pořádku")


@app.route('/registerValidate', methods=['POST'])
def validateRegister():
    username = request.form['username']
    if loadUser(username) is not None:
        return "False"
    else:
        return "True"


# USER PAGE
@app.route('/user')
def user():
    if 'username' not in session:
        return redirect('/login')
    diets = loadUserDiets(session['username'])
    user = loadUser(session['username'])
    return template('userPage', username=session['username'], diets=diets, firstname=user.firstname)


@app.route('/selectDietAJAX', methods=['POST'])
def selectDietAJAX():
    if 'username' not in session:
        return redirect('/login')
    dietID = request.form['selectDiet']
    recipes = loadDietRecipes(dietID)
    for i in range(len(recipes)):
        recipe = recipes[i]
        json_recipe = {'id': recipe.id, 'name': recipe.name}
        recipes[i] = json_recipe

    array_recipes = {'array': recipes, 'dietID': dietID}
    return jsonify(array_recipes)


# NEW DIET
@app.route('/newdiet', methods=['GET'])
def newDietShow():
    if 'username' not in session:
        return redirect('/login')
    return template('newDietPage', name="", sugar="", fat="", protein="", problem="")


@app.route('/newdiet', methods=['POST'])
def addDietAJAX():
    if 'username' not in session:
        return redirect('/login')
    diet = type('', (), {})()               # Magický trik, jak udělat prázdný objekt
    diet.name = request.form['name']
    diet.sugar = request.form['sugar']
    diet.fat = request.form['fat']
    diet.protein = request.form['protein']
    diet.small_size = request.form['small_size']
    diet.big_size = request.form['big_size']
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
    return redirect('/diet={}'.format(last_id))


# SHOW DIET PAGE
@app.route('/diet=<dietID>')
def showDiet(dietID):
    if 'username' not in session:
        return redirect('/login')

    diet = loadDiet(dietID)
    recipes = loadDietRecipes(diet.id)

    return template('dietPage', diet=diet, recipes=recipes)


@app.route('/diet=<dietID>/remove', methods=['POST'])
def removeDiet(dietID):
    if deleteDietCheck(dietID):  # wip
        deleteDiet(dietID)
        return redirect("/user")
    else:
        return template('failure', problem="Tato dieta má recepty, nelze smazat")


@app.route('/alldiets')
def allDiets():
    if 'username' not in session:
        return redirect('/login')

    diets = loadUserDiets(session['username'])
    return template('allDietsPage', diets=diets)


# NEW RECIPE PAGE
@app.route('/newrecipe')
def newRecipe():

    if 'username' not in session:
        return redirect('/login')

    diets = loadUserDiets(session['username'])
    ingredients = loadAllIngredients(session['username'])
    return template('newRecipePage', ingredients=ingredients, diets=diets, problem="")


@app.route('/addIngredientAJAX', methods=['POST'])
def addIngredienttoRecipeAJAX():
    if 'username' not in session:
        return redirect('/login')
    ingredient = loadIngredient(request.form["prerecipe__add-ingredient__form__select"])
    json_ingredient = {'id': ingredient.id, 'name': ingredient.name, 'sugar': ingredient.sugar, 'fat': ingredient.fat, 'protein': ingredient.protein}
    return jsonify(json_ingredient)


@app.route('/calcRecipeAJAX', methods=['POST'])
def calcRecipeAJAX():
    if 'username' not in session:
        return redirect('/login')

    ingredients = request.form['ingredients']
    if len(ingredients) == 0:
        # temp_print("No ingredients")
        return "False"
    ingredients = [word.strip() for word in ingredients.split(',')]

    # temp_print("ingredientIDs: {}".format(ingredients))

    dietID = request.form['select-diet']
    if dietID is None:
        # temp_print("No diet")
        return "False"

    mainIngredientID = request.form['main-ID']
    # temp solve problem with default WIP (problem with 3)
    if mainIngredientID == "":
        mainIngredientID = ingredients[0]

    ingredients.remove(mainIngredientID)
    # temp_print("ingredientIDs \main: {}".format(ingredients))

    # reaarange, so last ingredient is the main ingredient
    temp_ingredients = []
    for i in range(len(ingredients)):
        ingredient = loadIngredient(ingredients[i])
        temp_ingredients.append(ingredient)
    temp_ingredients.append(loadIngredient(mainIngredientID))

    ingredients.append(mainIngredientID)

    solution = calc(temp_ingredients, loadDiet(dietID))
    temp_print(solution.vars)
    if solution is None:
        temp_print("No solution")
        return "False"
    for i in range(len(ingredients)):
        ingredient = loadIngredient(ingredients[i])
        if solution.vars[i] < 0:
            temp_print("Solution < 0")
            return "False"
        json_ingredient = {'id': ingredient.id, 'name': ingredient.name, 'sugar': ingredient.sugar, 'fat': ingredient.fat, 'protein': ingredient.protein, 'amount': math.ceil(solution.vars[i] * 10000) / 100}  # wip
        ingredients[i] = json_ingredient

    if len(ingredients) <= 3:
        array_ingredients = {'ingredients': ingredients, 'dietID': dietID, }
    else:
        array_ingredients = {'ingredients': ingredients, 'dietID': dietID, 'mainIngredientID': mainIngredientID, 'mainIngredientMin': math.ceil(solution.min_sol * 10000) / 100, 'mainIngredientMax': math.ceil(solution.max_sol * 10000) / 100}
    return jsonify(array_ingredients)


@app.route('/recalcRecipeAJAX', methods=['POST'])
def recalcRecipeAJAX():
    # get data
    mainID = request.json['mainID']
    mainIngredient = loadIngredient(mainID)

    temp_ingredientsArray = request.json['ingredientsArray']
    temp_ingredients = [word.strip() for word in temp_ingredientsArray.split(',')]
    temp_ingredients.remove(mainID)
    ingredients = []
    for i in temp_ingredients:
        ingredients.append(loadIngredient(i))

    dietID = request.json['dietID']
    diet = loadDiet(dietID)

    slider = request.json['slider']
    slider = float(slider)

    # recalc
    a = numpy.array([
        [ingredients[0].protein, ingredients[1].protein, ingredients[2].protein],
        [ingredients[0].fat, ingredients[1].fat, ingredients[2].fat],
        [ingredients[0].sugar, ingredients[1].sugar, ingredients[2].sugar],
    ])
    b = numpy.array([
        (diet.protein * 10000 - mainIngredient.protein * math.ceil(slider * 100)) / 10000,
        (diet.fat * 10000 - mainIngredient.fat * math.ceil(slider * 100)) / 10000,
        (diet.sugar * 10000 - mainIngredient.sugar * math.ceil(slider * 100)) / 10000,
    ])
    results = numpy.linalg.solve(a, b)
    for i in range(len(results)):
        results[i] = math.ceil(results[i] * 10000) / 100
    x = {'id': temp_ingredients[0], 'amount': results[0]}
    y = {'id': temp_ingredients[1], 'amount': results[1]}
    z = {'id': temp_ingredients[2], 'amount': results[2]}
    totalProtein = loadIngredient(temp_ingredients[0]).protein * results[0] + loadIngredient(temp_ingredients[1]).protein * results[1] + loadIngredient(temp_ingredients[2]).protein * results[2] + loadIngredient(mainID).protein * slider
    totalSugar = loadIngredient(temp_ingredients[0]).sugar * results[0] + loadIngredient(temp_ingredients[1]).sugar * results[1] + loadIngredient(temp_ingredients[2]).sugar * results[2] + loadIngredient(mainID).sugar * slider
    totalFat = loadIngredient(temp_ingredients[0]).fat * results[0] + loadIngredient(temp_ingredients[1]).fat * results[1] + loadIngredient(temp_ingredients[2]).fat * results[2] + loadIngredient(mainID).fat * slider
    totals = {'protein': math.ceil(totalProtein) / 100, 'sugar': math.ceil(totalSugar) / 100, 'fat': math.ceil(totalFat) / 100}
    slider = {'id': mainID, 'amount': slider}
    solutionJSON = {'x': x, 'y': y, 'z': z, 'slider': slider, 'totals': totals}

    # give ids with amounts
    return jsonify(solutionJSON)


@app.route('/saveRecipeAJAX', methods=['POST'])
def addRecipeAJAX():
    if 'username' not in session:
        return redirect('/login')

    dietID = request.form['diet-ID']

    temp_ingredients = request.form['ingredients']
    temp_ingredients = [word.strip() for word in temp_ingredients.split(',')]

    temp_print(temp_ingredients)

    amounts = request.form['amounts']
    amounts = [word.strip() for word in amounts.split(',')]

    temp_print(amounts)

    ingredients = []
    for i in range(len(temp_ingredients)):
        ingredient = type('', (), {})()
        ingredient.id = temp_ingredients[i]
        ingredient.amount = amounts[i]
        ingredients.append(ingredient)

    recipe = type('', (), {})()
    recipe.name = request.form['recipe__right__form__name-input']
    recipe.size = request.form['recipe__right__form__size-select']
    last_id = saveRecipe(recipe, ingredients, dietID)
    return redirect('/recipe=' + str(last_id))


@app.route('/recipe=<recipeID>')
def showRecipe(recipeID):
    recipe = loadRecipe(recipeID)[0]
    diet = loadDiet(loadRecipeDietID(recipe.id))
    if recipe.size == "big":
        coef = diet.big_size / 100
    else:
        coef = diet.small_size / 100
    # temp_print(coef)

    ingredientIDs = loadRecipe(recipeID)[1]
    ingredients = []
    for ID in ingredientIDs:
        ingredients.append(loadIngredient(ID))
    for i in ingredients:
        i.amount = float(math.floor(loadAmount(i.id, recipeID)[0] * coef * 100000)) / 100000

    totals = type('', (), {})()
    totals.protein = 0
    totals.fat = 0
    totals.sugar = 0
    totals.amount = 0
    for i in ingredients:
        totals.protein += i.amount * i.protein
        totals.fat += i.amount * i.fat
        totals.sugar += i.amount * i.sugar
        totals.amount += i.amount

    # temp_print(totals.fat)
    totals.protein = math.floor(totals.protein) / 100
    totals.fat = math.floor(totals.fat) / 100
    totals.sugar = math.floor(totals.sugar) / 100
    totals.amount = math.floor(totals.amount)
    totals.eq = math.floor((totals.fat / (totals.protein + totals.sugar)) * 10) / 10
    return template('recipePage', recipe=recipe, ingredients=ingredients, totals=totals, diet=diet)


@app.route('/recipe=<recipeID>/remove', methods=['POST'])
def removeRecipe(recipeID):
    deleteRecipe(recipeID)
    return redirect('/user')


@app.route('/allrecipes')
def allrecipes():
    if 'username' not in session:
        return redirect('/login')
    recipes = loadUserRecipes(session['username'])
    for recipe in recipes:
        recipe.dietID = loadRecipeDietID(recipe.id)
        recipe.dietName = loadDiet(recipe.dietID).name

    return template("allRecipesPage", recipes=recipes)


# NEW INGREDIENT PAGE
@app.route('/newingredient', methods=['GET'])
def newingredient():
    if 'username' not in session:
        return redirect('/login')
    return template('newIngredientPage', name="", sugar="", fat="", protein="", problem="")


@app.route('/newIngredient', methods=['POST'])
def newIngredienttoRecipeAJAX():
    if 'username' not in session:
        return redirect('/login')

    ingredient = type('', (), {})()
    ingredient.name = request.form['name']
    ingredient.sugar = request.form['sugar']
    ingredient.fat = request.form['fat']
    ingredient.protein = request.form['protein']

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
    return redirect('/newingredient')


@app.route('/ingredient=<ingredientID>')
def showingredient(ingredientID):
    ingredient = loadIngredient(ingredientID)
    return template('ingredientPage', ingredient=ingredient)


@app.route('/ingredient=<ingredientID>/remove', methods=['POST'])
def removeIngredient(ingredientID):
    if deleteIngredientCheck(ingredientID):  # wip
        deleteIngredient(ingredientID)
        return redirect("/user")
    else:
        return template('failure', problem="Tato surovina je použita, nelze smazat")


@app.route('/allingredients')
def allingredients():
    if 'username' not in session:
        return redirect('/login')
    ingredients = loadAllIngredients(session['username'])
    return template("allIngredientsPage", ingredients=ingredients)


# CALCULATE RECIPE
def calc(ingredients, diet):
    if len(ingredients) == 0:
        return None
    elif len(ingredients) == 1:
        return None
    elif len(ingredients) == 2:
        a = numpy.array([[ingredients[0].sugar, ingredients[1].sugar], [ingredients[0].fat, ingredients[1].fat]])
        b = numpy.array([diet.sugar, diet.fat])
        x = numpy.linalg.solve(a, b)

        if x[0] * ingredients[0].protein + x[1] * ingredients[1].protein == diet.protein:
            solution = type('', (), {})()
            solution.vars = [x[0], x[1]]
            return solution
        else:
            return None
    elif len(ingredients) == 3:
        a = numpy.array([[ingredients[0].sugar, ingredients[1].sugar, ingredients[2].sugar],
                         [ingredients[0].fat, ingredients[1].fat, ingredients[2].fat],
                         [ingredients[0].protein, ingredients[1].protein, ingredients[2].protein]])
        b = numpy.array([diet.sugar, diet.fat, diet.protein])
        x = numpy.linalg.solve(a, b)
        solution = type('', (), {})()
        solution.vars = [x[0], x[1], x[2]]
        return solution

    elif len(ingredients) == 4:
        x, y, z = sp.symbols('x, y, z')
        e = sp.symbols('e')

        # set of linear equations
        f1 = ingredients[0].sugar * x + ingredients[1].sugar * y + ingredients[2].sugar * z + ingredients[3].sugar * e - diet.sugar
        f2 = ingredients[0].fat * x + ingredients[1].fat * y + ingredients[2].fat * z + ingredients[3].fat * e - diet.fat
        f3 = ingredients[0].protein * x + ingredients[1].protein * y + ingredients[2].protein * z + ingredients[3].protein * e - diet.protein

        # solve equations with args
        in1 = sp.solvers.solve((f1, f2, f3), (x, y, z))[x]
        in2 = sp.solvers.solve((f1, f2, f3), (x, y, z))[y]
        in3 = sp.solvers.solve((f1, f2, f3), (x, y, z))[z]

        # Faster way?? wip
        # solve for positive numbers
        result1 = solvei(poly(in1), ">=")
        temp_print(result1)
        result2 = solvei(poly(in2), ">=")
        temp_print(result2)
        result3 = solvei(poly(in3), ">=")
        temp_print(result3)

        interval = (result1[0].intersect(result2[0])).intersect(result3[0])
        if interval.right > 100:
            max_sol = 100
        else:
            max_sol = float(math.floor(interval.right * 10000) / 10000)

        if interval.left < 0:
            min_sol = 0
        else:
            min_sol = float(math.floor(interval.left * 10000) / 10000)

        if max_sol < min_sol:
            return None
        # max_sol = max for e (variable )
        sol = (min_sol + max_sol) / 2

        in1_dict = in1.as_coefficients_dict()
        x = in1_dict[e] * sol + in1_dict[1]

        in2_dict = in2.as_coefficients_dict()
        y = in2_dict[e] * sol + in2_dict[1]

        in3_dict = in3.as_coefficients_dict()
        z = in3_dict[e] * sol + in3_dict[1]

        x = float(math.floor(x * 100000) / 100000)
        y = float(math.floor(y * 100000) / 100000)
        z = float(math.floor(z * 100000) / 100000)

        if max_sol >= 0:
            solution = type('', (), {})()
            solution.vars = [x, y, z, sol]
            solution.sol = sol
            solution.min_sol = min_sol
            solution.max_sol = max_sol
            # return [x, y, z, f1, f2, f3, sol, min_sol, max_sol]
            return solution
        else:
            return None
    else:
        return None


# S'MORE
@app.route('/index.html')
def indexhtml():
    return redirect('/')


@app.route('/changelog')
def changelog():
    return template('changelog')


# ERROR
@app.errorhandler(404)
def error404(error):
    return 'Nothing here, sorry. (Err404)'


@app.errorhandler(500)
def error500(error):
    return 'Something went wrong! (Err500) <br>'


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == "__main__":
    # app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
    app.run(debug=True)
