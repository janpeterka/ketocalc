#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run by pyserver

from flask import render_template as template, request, redirect
from flask import jsonify
from flask import session
from flask import flash
from flask import abort

from flask_mail import Message
from werkzeug import secure_filename

from app import models
from app import app
from .data import template_data
from utils import *

# Hashing library
import hashlib

# Math library
import numpy
import sympy as sp
from sympy import solve_poly_inequality as solvei
from sympy import poly
import math
import os

# Printing
# import pdfkit

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


# global data
@app.context_processor
def inject_globals():
    return dict(icons=template_data.icons)


# MAIN

@app.before_first_request
def session_setup():
    # make the session last indefinitely until it is cleared
    session.permanent = True


@app.before_request
def session_management():
    # if request.path == '/trialnewrecipe' and 'username' in session:
    #     return redirect('/newrecipe')

    if request.path not in ['/register', '/registerValidate', '/login', '/static/style.css', '/trialnewrecipe', '/addIngredientAJAX', '/calcRecipeAJAX']:
        if 'username' not in session:
            return redirect('/login')


@app.route('/', methods=['GET'])
def main():
    return redirect('/dashboard')


# LOGIN
@app.route('/login', methods=['GET'])
def showLogin():
    return template('login.tpl')


@app.route('/login', methods=['POST'])
def doLogin():
    username = request.form['username']
    password = request.form['password']
    if checkLogin(username, password):
        session['username'] = username
        user = models.User.load(username)
        session['user_id'] = user.id
        # models.startSession()
        flash("Byl jste úspěšně přihlášen.")
        return redirect('/')
    else:
        flash("Přihlášení se nezdařilo.")
        return redirect('/login')


def checkLogin(username, password):
    """Validates credentials against db

    [description]

    Arguments:
        username {str}
        password {str}

    Returns:
        bool -- [description]
    """
    user = models.User.load(username)

    if user is None:
        return False
    db_password_hash = user.pwdhash
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if password_hash == db_password_hash:
        return True
    else:
        return False


@app.route('/logout')
def doLogout():
    session.pop('username', None)
    flash("Byl jste úspěšně odhlášen.")
    # models.endSession()
    return redirect('/login')


@app.route('/register', methods=['GET'])
def showRegister():
    return template('register.tpl', username="", firstname="", lastname="")


@app.route('/register', methods=['POST'])
def doRegister():
    temp_password = str(request.form['password'])
    temp_password_2 = str(request.form['againPassword'])

    user = models.User()
    user.username = request.form['username']
    user.firstName = request.form['firstname']
    user.lastName = request.form['lastname']
    user.pwdhash = hashlib.sha256(temp_password.encode('utf-8')).hexdigest()

    if len(user.lastName) == 0:
        flash("Není vyplněné jméno")
        return redirect(request.url)
    if len(user.firstName) == 0:
        flash("Není vyplněné příjmení")
        return redirect(request.url)
    if len(temp_password) < 8:
        flash("Heslo je příliš krátké")
        return redirect(request.url)
    if temp_password_2 != temp_password:
        flash("Hesla jsou rozdílná!")
        return redirect(request.url)
    if models.User.load(user.username) is not None:
        # Username used
        flash("Něco je špatně")
        return redirect(request.url)

    success = user.save()

    if success is not None:
        flash("Byl jste úspěšně zaregistrován.")
        return redirect('/login')
    else:
        flash("Registrace neproběhla v pořádku")
        return redirect('/register')


@app.route('/registerValidate', methods=['POST'])
def validateRegister():
    """validates if username is taken
    
    [description]
    
    Decorators:
        app.route
    """
    username = request.form['username']
    if models.User.load(username) is not None:
        return "False"
    else:
        return "True"


# USER PAGE
@app.route('/dashboard')
def showDashboard():
    user = models.User.load(session['username'])
    return template('dashboard.tpl', username=user.username, diets=user.activeDiets, firstname=user.firstName)


@app.route('/selectDietAJAX', methods=['POST'])
def selectDietAJAX():
    """returns recipes of diet

    Used on dashboard

    Decorators:
        app.route

    Returns:
        [type] -- [description]
    """
    diet = models.Diet.load(request.form['selectDiet'])

    json_recipes = []
    for recipe in diet.recipes:
        json_recipes.append(recipe.json)

    array_recipes = {'array': json_recipes, 'dietID': diet.id}
    return jsonify(array_recipes)


# NEW DIET
@app.route('/newdiet', methods=['GET'])
def showNewDiet():
    return template('newDiet.tpl')


@app.route('/newdiet', methods=['POST'])
def addDietAJAX():
    diet = models.Diet()
    diet.name = request.form['name']
    diet.sugar = request.form['sugar']
    diet.fat = request.form['fat']
    diet.protein = request.form['protein']
    diet.small_size = request.form['small_size']
    diet.big_size = request.form['big_size']
    diet.active = 1

    if len(diet.protein) == 0:
        flash("Vyplňte množství bílkoviny")
        return redirect(request.url)
    if len(diet.fat) == 0:
        flash("Vyplňte množství tuku")
        return redirect(request.url)
    if len(diet.sugar) == 0:
        flash("Vyplňte množství sacharidů")
        return redirect(request.url)
    if len(diet.name) == 0:
        flash("Vyplňte název")
        return redirect(request.url)

    diet.author = models.User.load(session['username'])
    diet.save()
    flash("Dieta byla vytvořena.")
    return redirect('/diet={}'.format(diet.id))


# SHOW DIET PAGE
@app.route('/diet=<diet_id>')
def showDiet(diet_id):
    diet = models.Diet.load(diet_id)

    if diet is None:
        abort(404)
    if diet.author.username != session['username']:
        return redirect('/wrongpage')

    return template('showDiet.tpl', diet=diet, recipes=diet.recipes, diets=diet.author.diets)


@app.route('/diet=<diet_id>/remove', methods=['POST'])
def removeDiet(diet_id):
    diet = models.Diet.load(diet_id)

    if diet.author.username != session['username']:
        return redirect('/wrongpage')

    if not diet.used:  # wip
        diet.remove()
        flash("Dieta byla smazána")
        return redirect("/alldiets")
    else:
        flash("Tato dieta má recepty, nelze smazat")
        return redirect('/diet={}'.format(diet_id))


@app.route('/diet=<diet_id>/archive', methods=['POST'])
def archiveDiet(diet_id):
    diet = models.Diet.load(diet_id)

    if diet.author.username != session['username']:
        return redirect('/wrongpage')

    if diet.active:
        flash("Dieta byla archivována")
    else:
        flash("Dieta byla aktivována")

    diet.active = not diet.active
    diet.edit()

    return redirect('/diet={}'.format(diet_id))


# @app.route('/diet=<dietID>/export', methods=['POST'])
# def exportDiet(dietID):
#     recipes = loadDietRecipes(dietID)
#     newDietID = int(request.form['diet'])
#     newDiet = loadDiet(newDietID)
#     for recipe in recipes:
#         ingredients = recipe.ingredients
#         solution = calc(ingredients, newDiet)
#         if solution is None:
#             continue
#         else:
#             for i in range(len(ingredients)):
#                 ingredients[i].amount = math.floor(solution.vars[i] * 10000) / 100
#             recipe.name = "{} {}".format(recipe.name, newDiet.name)
#             saveRecipe(recipe, ingredients, newDietID)
#     return redirect('/diet={}'.format(newDietID))


@app.route('/diet=<diet_id>/edit', methods=['POST'])
def editDietAJAX(diet_id):
    diet = models.Diet.load(diet_id)

    if diet.author.username != session['username']:
        return redirect('/wrongpage')

    diet.name = request.form['name']
    diet.id = diet_id
    diet.small_size = request.form['small_size']
    diet.big_size = request.form['big_size']

    if not diet.used:
        diet.protein = request.form['protein']
        diet.fat = request.form['fat']
        diet.sugar = request.form['sugar']

    diet.edit()
    flash("Dieta byla upravena.")
    return redirect('/diet={}'.format(diet_id))


@app.route('/alldiets')
def showAllDiets():
    """show all diets sorted

    active on top

    Decorators:
        app.route

    Returns:
        template -- [description]
    """
    diets = models.User.load(session['username']).diets
    diets.sort(key=lambda x: x.active, reverse=True)  # sort active first

    return template('allDiets.tpl', diets=diets)


# NEW RECIPE PAGE
@app.route('/trialnewrecipe')
def showTrialNewRecipe():
    ingredients = models.Ingredient.loadAllByUsername('basic')
    trial_diet = models.Diet.load(2)  # wip
    return template('trialNewRecipe.tpl', ingredients=ingredients, diet=trial_diet)


@app.route('/newrecipe')
def showNewRecipe():
    active_diets = models.User.load(session['username']).activeDiets
    ingredients = models.Ingredient.loadAllByUsername(session['username'])
    return template('newRecipe.tpl', ingredients=ingredients, diets=active_diets)


@app.route('/addIngredientAJAX', methods=['POST'])
def addIngredienttoRecipeAJAX():
    ingredient = models.Ingredient.load(request.form["prerecipe__add-ingredient__form__select"])
    return jsonify(ingredient.json)


@app.route('/calcRecipeAJAX', methods=['POST'])
def calcRecipeAJAX(test_dataset=None):
    """[summary]

    [description]

    Decorators:
        app.route

    Keyword Arguments:
        test_ingredients {array} -- array of json ingredients (default: {None})

    Returns:
        [type] -- [description]
    """
    # testing
    if test_dataset is None:
        json_ingredients = request.json['ingredients']
        diet = models.Diet.load(request.json['dietID'])
    else:
        json_ingredients = test_dataset['ingredients']
        diet = models.Diet.load(test_dataset['diet_id'])

    if diet is None:
        return "False"

    ingredients = []
    for json_i in json_ingredients:
        ingredient = models.Ingredient.load(json_i['id'])
        ingredient.fixed = json_i['fixed']
        ingredient.main = json_i['main']
        ingredient.amount = float(json_i['amount']) / 100  # from grams per 100g
        ingredients.append(ingredient)

    ingredients = calc(ingredients, diet)

    if ingredients is None:
        return "False"

    totals = {'calorie': 0, 'sugar': 0, 'fat': 0, 'protein': 0, 'amount': 0}

    json_ingredients = []
    for ing in ingredients:

        if ing.amount < 0:
            return "False"

        if hasattr(ing, 'min'):
            json_ingredient = {'id': ing.id, 'calorie': math.floor(ing.calorie * ing.amount * 100) / 100, 'name': ing.name, 'sugar': math.floor(ing.sugar * ing.amount * 100) / 100, 'fat': math.floor(ing.fat * ing.amount * 100) / 100, 'protein': math.floor(ing.protein * ing.amount * 100) / 100, 'amount': math.floor(ing.amount * 10000) / 100, 'main': ing.main, 'fixed': ing.fixed, 'min': ing.min, 'max': ing.max}  # wip
        else:
            json_ingredient = {'id': ing.id, 'calorie': math.floor(ing.calorie * ing.amount * 100) / 100, 'name': ing.name, 'sugar': math.floor(ing.sugar * ing.amount * 100) / 100, 'fat': math.floor(ing.fat * ing.amount * 100) / 100, 'protein': math.floor(ing.protein * ing.amount * 100) / 100, 'amount': math.floor(ing.amount * 10000) / 100, 'main': ing.main, 'fixed': ing.fixed}  # wip

        json_ingredients.append(json_ingredient)

        totals['calorie'] += json_ingredient['calorie']
        totals['sugar'] += json_ingredient['sugar']
        totals['fat'] += json_ingredient['fat']
        totals['protein'] += json_ingredient['protein']
        totals['amount'] += json_ingredient['amount']

    totals['calorie'] = math.floor(totals['calorie'] * 100) / 100
    totals['sugar'] = math.floor(totals['sugar'] * 100) / 100
    totals['fat'] = math.floor(totals['fat'] * 100) / 100
    totals['protein'] = math.floor(totals['protein'] * 100) / 100
    totals['amount'] = math.floor(totals['amount'] * 100) / 100

    totals['ratio'] = math.floor((totals['fat'] / (totals['protein'] + totals['sugar'])) * 100) / 100

    result = {'ingredients': json_ingredients, 'diet': diet.json, 'totals': totals}

    return jsonify(result)


@app.route('/recalcRecipeAJAX', methods=['POST'])
def recalcRecipeAJAX(test_dataset=None):
    # need to rewrite #wip

    # get data
    if test_dataset is None:
        json_ingredients = request.json['ingredients']
        diet = models.Diet.load(request.json['dietID'])
    else:
        json_ingredients = test_dataset['ingredients']
        diet = models.Diet.load(test_dataset['diet_id'])

    ingredients = []
    for json_ingredient in json_ingredients:
        ingredient = models.Ingredient.load(json_ingredient['id'])
        ingredient.fixed = json_ingredient['fixed']
        ingredient.main = json_ingredient['main']
        ingredient.amount = float(json_ingredient['amount']) / 100
        ingredients.append(ingredient)

    # remove main
    for i in range(len(ingredients)):
        if ingredients[i].main:
            mainIngredient = ingredients[i]
            ingredients.pop(i)
            break

    # count fixed values and remove from array (wip use calc instead - code duplicity)
    fixedSugar = 0
    fixedProtein = 0
    fixedFat = 0
    fixedIngredients = []
    fixedCalorie = 0
    fixedAmount = 0
    for i in range(len(ingredients)):
        if ingredients[i].fixed:
            fixedIngredients.append(ingredients[i])
            fixedSugar += ingredients[i].sugar * ingredients[i].amount
            fixedProtein += ingredients[i].protein * ingredients[i].amount
            fixedFat += ingredients[i].fat * ingredients[i].amount
            fixedAmount += ingredients[i].amount
            fixedCalorie += ingredients[i].calorie * ingredients[i].amount

    for ing in fixedIngredients:
        ingredients.remove(ing)

    slider = request.json['slider']
    slider = float(slider)

    # recalc
    a = numpy.array([
        [ingredients[0].protein, ingredients[1].protein, ingredients[2].protein],
        [ingredients[0].fat, ingredients[1].fat, ingredients[2].fat],
        [ingredients[0].sugar, ingredients[1].sugar, ingredients[2].sugar],
    ])
    b = numpy.array([
        (diet.protein * 10000 - mainIngredient.protein * math.floor(slider * 100) - fixedProtein) / 10000,
        (diet.fat * 10000 - mainIngredient.fat * math.floor(slider * 100) - fixedFat) / 10000,
        (diet.sugar * 10000 - mainIngredient.sugar * math.floor(slider * 100) - fixedSugar) / 10000,
    ])
    results = numpy.linalg.solve(a, b)
    for i in range(len(results)):
        results[i] = math.floor(results[i] * 10000) / 100
    x = {'id': ingredients[0].id, 'amount': results[0]}
    y = {'id': ingredients[1].id, 'amount': results[1]}
    z = {'id': ingredients[2].id, 'amount': results[2]}
    results = [x, y, z]
    count = 0
    for ing in json_ingredients:
        if ing['main'] is True:
            ing['amount'] = slider
        elif ing['fixed'] is True:
            pass
        else:
            ing['amount'] = math.floor(results[count]['amount'] * 100) / 100
            count += 1

    totals = {'calorie': 0, 'protein': 0, 'sugar': 0, 'fat': 0, 'amount': 0, 'ratio': 0}

    # calc ingredient nutritients
    for ing in json_ingredients:
        base_ing = models.Ingredient.load(int(ing['id']))

        ing['calorie'] = math.floor(base_ing.calorie * ing['amount']) / 100
        ing['sugar'] = math.floor(base_ing.sugar * ing['amount']) / 100
        ing['fat'] = math.floor(base_ing.fat * ing['amount']) / 100
        ing['protein'] = math.floor(base_ing.protein * ing['amount']) / 100

        totals['calorie'] += ing['calorie']
        totals['sugar'] += ing['sugar']
        totals['fat'] += ing['fat']
        totals['protein'] += ing['protein']
        totals['amount'] += ing['amount']

    totals['ratio'] = math.floor((totals['fat'] / (totals['protein'] + totals['sugar'])) * 100) / 100

    totals['calorie'] = math.floor(totals['calorie'] * 100) / 100
    totals['sugar'] = math.floor(totals['sugar'] * 100) / 100
    totals['fat'] = math.floor(totals['fat'] * 100) / 100
    totals['protein'] = math.floor(totals['protein'] * 100) / 100
    totals['amount'] = math.floor(totals['amount'] * 100) / 100
    totals['ratio'] = math.floor(totals['ratio'] * 100) / 100

    solutionJSON = {'ingredients': json_ingredients, 'totals': totals}

    # return ingredients with amounts + totals
    return jsonify(solutionJSON)


@app.route('/saveRecipeAJAX', methods=['POST'])
def addRecipeAJAX():
    temp_ingredients = request.json['ingredients']
    diet_id = request.json['dietID']

    ingredients = []
    for temp_i in temp_ingredients:
        rhi = models.RecipesHasIngredient()
        rhi.ingredients_id = temp_i['id']
        rhi.amount = temp_i['amount']
        ingredients.append(rhi)

    recipe = models.Recipe()
    recipe.name = request.json['name']
    recipe.type = request.json['size']
    recipe.diet = models.Diet.load(diet_id)

    last_id = recipe.save(ingredients)
    flash("Recept byl uložen")
    return ('/recipe=' + str(last_id))


@app.route('/recipe=<recipe_id>')
def showRecipe(recipe_id):
    recipe_data = models.Recipe.load(recipe_id).loadRecipeForShow()
    return template('showRecipe.tpl', recipe=recipe_data['recipe'], totals=recipe_data['totals'])


@app.route('/recipe=<recipe_id>/print')
def printRecipe(recipe_id):
    recipe_data = models.Recipe.load(recipe_id).loadRecipeForShow()
    return template('printRecipe.tpl', recipe=recipe_data['recipe'], totals=recipe_data['totals'])


@app.route('/recipe=<recipe_id>/remove', methods=['POST'])
def removeRecipeAJAX(recipe_id):
    if session['username'] != models.Recipe.load(recipe_id).author.username:
        return redirect('/wrongpage')

    recipe = models.Recipe.load(recipe_id)
    recipe.remove()
    flash("Recept byl smazán.")
    return redirect('/')


@app.route('/recipe=<recipe_id>/edit', methods=['POST'])
def editRecipeAJAX(recipe_id):
    if session['username'] != models.Recipe.load(recipe_id).author.username:
        return redirect('/wrongpage')

    recipe = models.Recipe.load(recipe_id)
    recipe.name = request.form['name']
    recipe.type = request.form['size']
    recipe.edit()
    flash("Recept byl upraven.")
    return redirect('/recipe={}'.format(recipe_id))


@app.route('/allrecipes')
def showAllRecipes():
    user = models.User.load(session['username'])
    return template("allRecipes.tpl", diets=user.diets)


@app.route('/diet=<diet_id>/print')
def printDietRecipes(diet_id):
    diet = models.Diet.load(diet_id)

    for recipe in diet.recipes:
        recipe_data = recipe.loadRecipeForShow()
        recipe = recipe_data['recipe']
        recipe.totals = recipe_data['totals']
    return template("printAllRecipes.tpl", recipes=diet.recipes)


@app.route('/printallrecipes')
def printAllRecipes():
    recipes = models.User.load(session['username']).recipes

    for recipe in recipes:
        recipe = recipe.loadRecipeForShow['recipe']
        recipe.totals = recipe.loadRecipeForShow['totals']

    return template("printAllRecipes.tpl", recipes=recipes)


# NEW INGREDIENT PAGE
@app.route('/newingredient', methods=['GET'])
def showNewIngredient():
    return template('newIngredient.tpl')


@app.route('/newingredient', methods=['POST'])
def addNewIngredientAJAX():
    ingredient = models.Ingredient()
    ingredient.name = request.form['name']
    ingredient.calorie = request.form['calorie']
    ingredient.sugar = request.form['sugar']
    ingredient.fat = request.form['fat']
    ingredient.protein = request.form['protein']
    ingredient.author = session['username']

    if len(ingredient.protein) == 0:
        flash("Zadejte množství bílkoviny")
        return redirect(request.url)
    if len(ingredient.calorie) == 0:
        flash("Zadejte kalorie")
        return redirect(request.url)
    if len(ingredient.fat) == 0:
        flash("Zadejte množství tuku")
        return redirect(request.url)
    if len(ingredient.sugar) == 0:
        flash("Zadejte množství sacharidů")
        return redirect(request.url)
    if len(ingredient.name) == 0:
        flash("Zadejte název suroviny")
        return redirect(request.url)

    ingredient.save()
    flash("Nová surovina byla vytvořena")
    return redirect('/newingredient')


@app.route('/ingredient=<ingredient_id>')
def showIngredient(ingredient_id):
    ingredient = models.Ingredient.load(ingredient_id)

    if ingredient is None:
        abort(404)
    if session['username'] != ingredient.author:
        return redirect('/wrongpage')

    return template('showIngredient.tpl', ingredient=ingredient)


@app.route('/ingredient=<ingredient_id>/remove', methods=['POST'])
def removeIngredientAJAX(ingredient_id):
    ingredient = models.Ingredient.load(ingredient_id)

    if session['username'] != ingredient.author:
        return redirect('/wrongpage')

    if not ingredient.used:
        ingredient.remove()
        flash("Surovina byla smazána")
        return redirect("/")
    else:
        flash("Tato surovina je použita, nelze smazat")
        return redirect('/ingredient={}'.format(ingredient_id))


@app.route('/ingredient=<ingredient_id>/edit', methods=['POST'])
def editIngredientAJAX(ingredient_id):
    ingredient = models.Ingredient.load(ingredient_id)

    if session['username'] != ingredient.author:
        return redirect('/wrongpage')

    ingredient.name = request.form['name']
    ingredient.id = ingredient_id
    ingredient.calorie = request.form['calorie']
    if not ingredient.used:
        ingredient.protein = request.form['protein']
        ingredient.fat = request.form['fat']
        ingredient.sugar = request.form['sugar']
        ingredient.edit()
        flash("Surovina byla upravena.")
        return redirect('/ingredient={}'.format(ingredient_id))
    else:
        ingredient.edit()
        flash("Název a kalorická hodnota byly upraveny.")
        return redirect('/ingredient={}'.format(ingredient_id))


@app.route('/allingredients')
def showAllIngredients():
    # basic_ingredients = models.Ingredient.loadAllByUsername('default')
    ingredients = models.Ingredient.loadAllByUsername(session['username'])
    return template("allIngredients.tpl", ingredients=ingredients)


@app.route('/user')
def showUser():
    user = models.User.load(session['username'])
    return template('showUser.tpl', user=user)


@app.route('/user/edit', methods=['POST'])
def editUserAJAX():
    user = models.User.load(session['username'])
    user.firstName = request.form['firstname']
    user.lastName = request.form['lastname']
    success = user.edit()
    if success is not None:
        flash("Uživatel byl upraven")
    else:
        flash("Nepovedlo se změnit uživatele")
    return template('showUser.tpl', user=user)


@app.route('/user/password_change', methods=['POST'])
def changeUserAJAX():
    user = models.User.load(session['username'])

    if user is None:
        return redirect('/wrongpage')

    password = request.form['password'].encode('utf-8')
    user.pwdhash = hashlib.sha256(password).hexdigest()

    success = user.edit()
    if success is not None:
        flash("Heslo bylo změněno")
    else:
        flash("Nepovedlo se změnit heslo")
    return template('showUser.tpl', user=user)


# CALCULATE RECIPE
def calc(ingredients, diet):
    """
    [summary]

    [description]

    Arguments:
        ingredients {array} -- array of Ingredients
        diet {Diet} -- Diet

    Returns:
        [type] -- solution object
        3 - ingredients {array} -- array of Ingredients (w/ amounts - 2 decimals)
        4 - ingredients {array} (last-main ing has min, max)
    """
    # remove fixed
    fixedSugar = 0
    fixedProtein = 0
    fixedFat = 0

    fixedIngredients = []
    for i in range(len(ingredients)):
        if ingredients[i].fixed is True:
            fixedSugar += ingredients[i].amount * ingredients[i].sugar
            fixedProtein += ingredients[i].amount * ingredients[i].protein
            fixedFat += ingredients[i].amount * ingredients[i].fat
            fixedIngredients.append(ingredients[i])

    for ing in fixedIngredients:
        ingredients.remove(ing)

    # changes diets accordingly
    diet.fat -= fixedFat
    diet.sugar -= fixedSugar
    diet.protein -= fixedProtein

    # sort for main ingredient + reaarange, so last ingredient is the main ingredient (better handling)
    mainIngredient = ingredients[0]
    for i in range(len(ingredients)):
        if ingredients[i].main is True:
            mainIngredient = ingredients[i]
            ingredients.pop(i)
            ingredients.append(mainIngredient)
            break

    # calculate
    if len(ingredients) == 0:
        return None
    elif len(ingredients) == 1:
        return None
    elif len(ingredients) == 2:
        return None
    elif len(ingredients) == 3:
        a = numpy.array([[ingredients[0].sugar, ingredients[1].sugar, ingredients[2].sugar],
                         [ingredients[0].fat, ingredients[1].fat, ingredients[2].fat],
                         [ingredients[0].protein, ingredients[1].protein, ingredients[2].protein]])
        b = numpy.array([diet.sugar, diet.fat, diet.protein])
        x = numpy.linalg.solve(a, b)

        ingredients[0].amount = x[0]
        ingredients[1].amount = x[1]
        ingredients[2].amount = x[2]

        for ing in fixedIngredients:
            ingredients.append(ing)

        diet.fat += fixedFat
        diet.sugar += fixedSugar
        diet.protein += fixedProtein

        return ingredients

    elif len(ingredients) == 4:
        x, y, z = sp.symbols('x, y, z')
        e = sp.symbols('e')

        # set of linear equations
        f1 = ingredients[0].sugar * x + ingredients[1].sugar * y + ingredients[2].sugar * z + ingredients[3].sugar * e - (diet.sugar)
        f2 = ingredients[0].fat * x + ingredients[1].fat * y + ingredients[2].fat * z + ingredients[3].fat * e - (diet.fat)
        f3 = ingredients[0].protein * x + ingredients[1].protein * y + ingredients[2].protein * z + ingredients[3].protein * e - (diet.protein)

        # solve equations with args
        in1 = sp.solvers.solve((f1, f2, f3), (x, y, z))[x]
        in2 = sp.solvers.solve((f1, f2, f3), (x, y, z))[y]
        in3 = sp.solvers.solve((f1, f2, f3), (x, y, z))[z]

        # Faster way?? wip
        # solve for positive numbers
        result1 = solvei(poly(in1), ">=")
        result2 = solvei(poly(in2), ">=")
        result3 = solvei(poly(in3), ">=")

        interval = (result1[0].intersect(result2[0])).intersect(result3[0])
        if interval.is_EmptySet:
            return None

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
        # max_sol = max for e (variable)
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

        if x < 0 or y < 0 or z < 0:
            return None

        ingredients[0].amount = x
        ingredients[1].amount = y
        ingredients[2].amount = z
        ingredients[3].amount = sol
        ingredients[3].min = min_sol
        ingredients[3].max = max_sol

        # return fixed ingredients #wip - for other branches
        for ing in fixedIngredients:
            ingredients.append(ing)

        # return diet to normal for commit #wip - for other branches
        diet.fat += fixedFat
        diet.sugar += fixedSugar
        diet.protein += fixedProtein

        return ingredients

    # 5 ingredients #wip
    elif len(ingredients) == 5:
        # x, y, z = sp.symbols('x, y, z')
        # e, f = sp.symbols('e, f')
        #
        # # set of linear equations
        # f1 = ingredients[0].sugar * x + ingredients[1].sugar * y + ingredients[2].sugar * z + ingredients[3].sugar * e + ingredients[4].sugar * f - diet.sugar
        # f2 = ingredients[0].fat * x + ingredients[1].fat * y + ingredients[2].fat * z + ingredients[3].fat * e + ingredients[4].fat * f - diet.fat
        # f3 = ingredients[0].protein * x + ingredients[1].protein * y + ingredients[2].protein * z + ingredients[3].protein * e + ingredients[4].protein * f - diet.protein
        #
        # # solve equations with args
        # in1 = sp.solvers.solve((f1, f2, f3), (x, y, z))[x]
        # in2 = sp.solvers.solve((f1, f2, f3), (x, y, z))[y]
        # in3 = sp.solvers.solve((f1, f2, f3), (x, y, z))[z]

        # Faster way?? wip
        # solve for positive numbers
        # result1 = solvei(poly(in1), ">=")
        # result2 = solvei(poly(in2), ">=")
        # result3 = solvei(poly(in3), ">=")

        # interval = (result1[0].intersect(result2[0])).intersect(result3[0])
        # if interval.right > 100:
        #     max_sol = 100
        # else:
        #     max_sol = float(math.floor(interval.right * 10000) / 10000)

        # if interval.left < 0:
        #     min_sol = 0
        # else:
        #     min_sol = float(math.floor(interval.left * 10000) / 10000)

        # if max_sol < min_sol:
        #     return None
        # # max_sol = max for e (variable )
        # sol = (min_sol + max_sol) / 2

        # in1_dict = in1.as_coefficients_dict()
        # x = in1_dict[e] * sol + in1_dict[1]

        # in2_dict = in2.as_coefficients_dict()
        # y = in2_dict[e] * sol + in2_dict[1]

        # in3_dict = in3.as_coefficients_dict()
        # z = in3_dict[e] * sol + in3_dict[1]

        # x = float(math.floor(x * 100000) / 100000)
        # y = float(math.floor(y * 100000) / 100000)
        # z = float(math.floor(z * 100000) / 100000)

        # if max_sol >= 0:
        #     solution = type('', (), {})()
        #     solution.vars = [x, y, z, sol]
        #     solution.sol = sol
        #     solution.min_sol = min_sol
        #     solution.max_sol = max_sol
        #     return solution
        # else:
        return None
    else:
        return None


@app.route('/feedback', methods=['GET'])
def showFeedback():
    return template('feedback.tpl')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/feedback', methods=['POST'])
def sendFeedback():
    msg = Message('[ketocalc] [{}]'.format(request.form['type']), sender='ketocalc', recipients=['ketocalc.jmp@gmail.com'])
    msg.body = "Message: {}\n".format(request.form['message'])
    msg.body += "Send by: {} [user: {}]".format(request.form['sender'], session['username'])

    if 'file' not in request.files:
        mail.send(msg)
        flash("Vaše připomínka byla zaslána na vyšší místa.")
        return redirect('/')
    else:
        file = request.files['file']

    if file.filename == '':
        mail.send(msg)
        flash("Vaše připomínka byla zaslána na vyšší místa.")
        return redirect('/')
    elif file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        with app.open_resource(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as fp:
            msg.attach("screenshot", "image/{}".format(filename.split(".")[1]), fp.read())

        mail.send(msg)
        flash("Vaše připomínka byla zaslána na vyšší místa.")
        return redirect('/')


# S'MORE
@app.route('/index.html')
def indexhtml():
    return redirect('/')


@app.route('/changelog')
def showChangelog():
    return template('changelog.tpl')


@app.route('/help')
def showHelp():
    return template('help.tpl')


# ERROR
@app.route('/wrongpage')
def wrongPage():
    return template('wrongPage.tpl')


@app.route('/shutdown')
def shutdown():
    return template('shutdown.tpl')


@app.route('/testing')
def testingPage():
    if session['username'] != 'admin':
        redirect('/wrongpage')
    return template('testing.tpl', data=app.config['TEST_VAR'])


@app.route('/google3748bc0390347e56.html')
def googleVerification():
    return template('google3748bc0390347e56.html')


@app.errorhandler(404)
def error404(error):
    # Missing page
    return template('err404.tpl')


@app.errorhandler(405)
def error405(error):
    # Action not allowed (AJAX)
    return template('wrongPage.tpl')


@app.errorhandler(500)
def error500(error):
    # Internal error
    return template('err500.tpl')





if __name__ == "__main__":
    app.run(debug=True)
