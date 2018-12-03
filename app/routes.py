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
# import flask_security

# import requests
# import json

from app import models, forms
from app import application
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

from functools import wraps
# Printing
# import pdfkit

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


# global data
@application.context_processor
def inject_globals():
    return dict(icons=template_data.icons)


# MAIN

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['username'] != 'admin':
            return redirect('/wrongpage')
        return f(*args, **kwargs)
    return decorated_function


@application.before_first_request
def session_setup():
    # make the session last indefinitely until it is cleared
    session.permanent = True


@application.before_request
def session_management():
    if application.config['APP_STATE'] == 'shutdown' and request.path not in ['/shutdown', '/static/style.css']:
        return redirect('/shutdown')
    elif request.path == '/shutdown' and application.config['APP_STATE'] != 'shutdown':
            return redirect('/')


@application.route('/', methods=['GET'])
def main():
    return redirect('/dashboard')


# LOGIN
@application.route('/login', methods=['GET', 'POST'])
def showLogin():
    form = forms.LoginForm(request.form)
    if request.method == 'GET':
        return template('login.tpl', form=form)
    elif request.method == 'POST':
        if not form.validate_on_submit():
            return template('login.tpl', form=form)
        if doLogin(form.username.data, form.password.data.encode('utf-8')):
            return redirect('/dashboard')
        else:
            return redirect('/login')


def doLogin(username, password, from_register=False):
    user = models.User.load(username)
    if user is not None and user.checkLogin(password):
        session['username'] = username
        session['user_id'] = user.id
        if not from_register:
            flash('Byl jste úspěšně přihlášen.', 'success')
            return True
    else:
        flash('Přihlášení se nezdařilo.', 'error')
        return False


@application.route('/logout')
def doLogout():
    session.pop('username', None)
    session.pop('user_id', None)
    flash('Byl jste úspěšně odhlášen.', 'info')
    return redirect('/login')


@application.route('/register', methods=['GET', 'POST'])
def showRegister():
    form = forms.RegisterForm(request.form)
    if request.method == 'GET':
        return template('register.tpl', form=form)
    elif request.method == 'POST':

        if not validateRegister(form.username.data):
            form.username.errors.append('Toto jméno nemůžete použít')
        if not form.validate_on_submit():
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
        doLogin(user.username, user.password.encode('utf-8'), True)
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


# USER PAGE
@application.route('/dashboard')
@login_required
def showDashboard():
    user = models.User.load(session['user_id'])
    return template('dashboard.tpl', diets=user.activeDiets, firstname=user.firstName)


@application.route('/selectDietAJAX', methods=['POST'])
@login_required
def selectDietAJAX():
    """returns recipes of diet

    Used on dashboard

    Decorators:
        application.route
        login_required

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
@application.route('/newdiet', methods=['GET', 'POST'])
@login_required
def showNewDiet():
    form = forms.NewDietForm()
    if request.method == 'GET':
        return template('newDiet.tpl', form=form)
    elif request.method == 'POST':
        diet = models.Diet()
        diet.name = form.name.data
        diet.sugar = form.sugar.data
        diet.fat = form.fat.data
        diet.protein = form.protein.data
        diet.small_size = form.small_size.data
        diet.big_size = form.big_size.data
        diet.active = 1
        diet.author = models.User.load(session['user_id'])

        if not form.validate_on_submit():
            return template('newDiet.tpl', form=form)

        if diet.save():
            flash('Nová dieta byla vytvořena', 'success')
            return redirect('/diet={}'.format(diet.id))
        else:
            flash('Nepodařilo se vytvořit dietu', 'error')
            return template('newDiet.tpl', form=form)

    return template('newDiet.tpl')


# SHOW DIET PAGE
@application.route('/diet=<int:diet_id>')
@application.route('/diet=<int:diet_id>/<page_type>', methods=['POST', 'GET'])
@login_required
def showDiet(diet_id, page_type=None):
    diet = models.Diet.load(diet_id)
    if diet is None:
        abort(404)
    if diet.author.username != session['username']:
        return redirect('/wrongpage')

    if page_type is None:
        return template('showDiet.tpl', diet=diet, recipes=diet.recipes, diets=diet.author.diets)
    elif page_type == 'remove' and request.method == 'POST':
        if not diet.used:  # wip
            diet.remove()
            flash('Dieta byla smazána', 'success')
            return redirect('/alldiets')
        else:
            flash('Tato dieta má recepty, nelze smazat', 'error')
            return redirect('/diet={}'.format(diet_id))
    elif page_type == 'archive' and request.method == 'POST':
        flash('Dieta byla archivována', 'info') if diet.active else flash('Dieta byla aktivována', 'info')
        diet.active = not diet.active
        diet.edit()

        return redirect('/diet={}'.format(diet_id))
    elif page_type == 'edit' and request.method == 'POST':
        diet.name = request.form['name']
        diet.id = diet_id
        diet.small_size = request.form['small_size']
        diet.big_size = request.form['big_size']

        if not diet.used:
            diet.protein = request.form['protein']
            diet.fat = request.form['fat']
            diet.sugar = request.form['sugar']

        diet.edit()
        flash('Dieta byla upravena.', 'success')
        return redirect('/diet={}'.format(diet_id))


# @application.route('/diet=<dietID>/export', methods=['POST'])
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


@application.route('/alldiets')
@login_required
def showAllDiets():
    """show all diets sorted (active first)

    active on top

    Decorators:
        application.route

    Returns:
        template -- [description]
    """
    diets = models.User.load(session['user_id']).diets
    diets.sort(key=lambda x: x.active, reverse=True)

    return template('allDiets.tpl', diets=diets)


# NEW RECIPE PAGE
@application.route('/trialnewrecipe')
def showTrialNewRecipe():
    ingredients = models.Ingredient.loadAllByAuthor('basic')
    trial_diet = models.Diet.load(2)  # wip
    return template('trialNewRecipe.tpl', ingredients=ingredients, diet=trial_diet)


@application.route('/newrecipe')
@login_required
def showNewRecipe():
    active_diets = models.User.load(session['user_id']).activeDiets
    ingredients = models.Ingredient.loadAllByAuthor(session['username'])
    return template('newRecipe.tpl', ingredients=ingredients, diets=active_diets)


@application.route('/addIngredientAJAX', methods=['POST'])
def addIngredienttoRecipeAJAX():
    ingredient = models.Ingredient.load(request.form['prerecipe__add-ingredient__form__select'])
    return jsonify(ingredient.json)


@application.route('/calcRecipeAJAX', methods=['POST'])
def calcRecipeAJAX(test_dataset=None):
    """[summary]

    [description]

    Decorators:
        application.route

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
        return 'False'

    ingredients = []
    for json_i in json_ingredients:
        ingredient = models.Ingredient.load(json_i['id'])
        ingredient.fixed = json_i['fixed']
        ingredient.main = json_i['main']
        ingredient.amount = float(json_i['amount']) / 100  # from grams per 100g
        ingredients.append(ingredient)

    ingredients = calc(ingredients, diet)

    if ingredients is None:
        return 'False'

    totals = {'calorie': 0, 'sugar': 0, 'fat': 0, 'protein': 0, 'amount': 0}

    json_ingredients = []
    for ing in ingredients:

        if ing.amount < 0:
            return 'False'

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


@application.route('/recalcRecipeAJAX', methods=['POST'])
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


@application.route('/saveRecipeAJAX', methods=['POST'])
@login_required
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
    flash('Recept byl uložen', 'success')
    return ('/recipe=' + str(last_id))


@application.route('/recipe=<int:recipe_id>', methods=['GET'])
@application.route('/recipe=<int:recipe_id>/<page_type>', methods=['POST', 'GET'])
@login_required
def showRecipe(recipe_id, page_type=None):
    try:
        recipe_data = models.Recipe.load(recipe_id).loadRecipeForShow()
    except AttributeError:
        return abort(404)

    if session['username'] != models.Recipe.load(recipe_id).author.username:
        return redirect('/wrongpage')

    if page_type is None:
        return template('showRecipe.tpl', recipe=recipe_data['recipe'], totals=recipe_data['totals'], show=True)
    elif page_type == 'print':
        return template('showRecipe.tpl', recipe=recipe_data['recipe'], totals=recipe_data['totals'], show=False)
    elif page_type == 'edit' and request.method == 'POST':
        recipe = recipe_data['recipe']
        recipe.name = request.form['name']
        recipe.type = request.form['size']
        recipe.edit()
        flash('Recept byl upraven.', 'success')
        return redirect('/recipe={}'.format(recipe_id))
    elif page_type == 'remove' and request.method == 'POST':
        recipe = recipe_data['recipe']
        recipe.remove()
        flash('Recept byl smazán.', 'success')
        return redirect('/')
    else:
        redirect('/wrongpage')


@application.route('/allrecipes')
@login_required
def showAllRecipes():
    user = models.User.load(session['user_id'])
    return template('allRecipes.tpl', diets=user.diets)


@application.route('/diet=<int:diet_id>/print')
@login_required
def printDietRecipes(diet_id):
    diet = models.Diet.load(diet_id)
    for recipe in diet.recipes:
        recipe_data = recipe.loadRecipeForShow()
        recipe.totals = recipe_data['totals']
    return template('printAllRecipes.tpl', recipes=diet.recipes)


@application.route('/printallrecipes')
@login_required
def printAllRecipes():
    recipes = models.User.load(session['user_id']).recipes
    for recipe in recipes:
        recipe_data = recipe.loadRecipeForShow()
        recipe.totals = recipe_data['totals']
    return template('printAllRecipes.tpl', recipes=recipes)


# NEW INGREDIENT PAGE
@application.route('/newingredient', methods=['GET', 'POST'])
@login_required
def showNewIngredient():
    form = forms.NewIngredientForm()
    if request.method == 'GET':
        return template('newIngredient.tpl', form=form)
    elif request.method == 'POST':
        ingredient = models.Ingredient()
        ingredient.name = form.name.data
        ingredient.calorie = form.calorie.data
        ingredient.sugar = form.sugar.data
        ingredient.fat = form.fat.data
        ingredient.protein = form.protein.data
        ingredient.author = session['username']
        if not form.validate_on_submit():
            return template('newIngredient.tpl', form=form)

        if ingredient.save():
            flash('Nová surovina byla vytvořena', 'success')
            return redirect('/ingredient={}'.format(ingredient.id))
        else:
            flash('Nepodařilo se vytvořit surovinu', 'error')
            return template('newIngredient.tpl', form=form)


@application.route('/ingredient=<int:ingredient_id>')
@application.route('/ingredient=<int:ingredient_id>/<page_type>', methods=['POST', 'GET'])
@login_required
def showIngredient(ingredient_id, page_type=None):
    ingredient = models.Ingredient.load(ingredient_id)
    if ingredient is None:
        abort(404)
    if session['username'] != ingredient.author:
        return redirect('/wrongpage')

    if page_type is None:
        recipes = models.Recipe.loadByIngredient(ingredient.id)
        return template('showIngredient.tpl', ingredient=ingredient, recipes=recipes)

    elif page_type == 'edit' and request.methods == 'POST':
        ingredient.name = request.form['name']
        ingredient.id = ingredient_id
        ingredient.calorie = request.form['calorie']
        if not ingredient.used:
            ingredient.protein = request.form['protein']
            ingredient.fat = request.form['fat']
            ingredient.sugar = request.form['sugar']
            ingredient.edit()
            flash('Surovina byla upravena.', 'success')
            return redirect('/ingredient={}'.format(ingredient_id))
        else:
            ingredient.edit()
            flash('Název a kalorická hodnota byly upraveny.', 'success')
            return redirect('/ingredient={}'.format(ingredient_id))

    elif page_type == 'remove' and request.methods == 'POST':
        if not ingredient.used:
            ingredient.remove()
            flash('Surovina byla smazána', 'success')
            return redirect('/')
        else:
            flash('Tato surovina je použita, nelze smazat', 'error')
            return redirect('/ingredient={}'.format(ingredient_id))


@application.route('/allingredients')
@login_required
def showAllIngredients():
    # basic_ingredients = models.Ingredient.loadAllByAuthor('default')
    ingredients = models.Ingredient.loadAllByAuthor(session['username'])
    return template('allIngredients.tpl', ingredients=ingredients)


@application.route('/user')
@application.route('/user/<page_type>', methods=['POST', 'GET'])
@login_required
def showUser(page_type=None):
    user = models.User.load(session['user_id'])
    if user is None:
        return redirect('/wrongpage')
    if page_type is None:
        return template('showUser.tpl', user=user)
    elif page_type == 'edit' and request.method == 'POST':
        user.firstName = request.form['firstname']
        user.lastName = request.form['lastname']
        success = user.edit()
        if success is not None:
            flash('Uživatel byl upraven', 'success')
        else:
            flash('Nepovedlo se změnit uživatele', 'error')
        return template('showUser.tpl', user=user)
    elif page_type == 'password_change' and request.method == 'POST':

        password = request.form['password'].encode('utf-8')
        user.pwdhash = hashlib.sha256(password).hexdigest()

        success = user.edit()
        if success is not None:
            flash('Heslo bylo změněno', 'success')
        else:
            flash('Nepovedlo se změnit heslo', 'error')
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
        result1 = solvei(poly(in1), '>=')
        result2 = solvei(poly(in2), '>=')
        result3 = solvei(poly(in3), '>=')

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


@application.route('/feedback', methods=['GET', 'POST'])
@login_required
def showFeedback():
    if request.method == 'GET':
        return template('feedback.tpl')
    elif request.method == 'POST':
        msg = Message('[ketocalc] [{}]'.format(request.form['type']), sender='ketocalc', recipients=['ketocalc.jmp@gmail.com'])
        msg.body = 'Message: {}\n'.format(request.form['message'])
        msg.body += 'Send by: {} [user: {}]'.format(request.form['sender'], session['username'])

        if 'file' not in request.files:
            mail.send(msg)
            flash('Vaše připomínka byla zaslána na vyšší místa.', 'success')
            return redirect('/')
        else:
            file = request.files['file']

        if file.filename == '':
            mail.send(msg)
            flash('Vaše připomínka byla zaslána na vyšší místa.', 'success')
            return redirect('/')
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            with application.open_resource(os.path.join(application.config['UPLOAD_FOLDER'], filename)) as fp:
                msg.attach('screenshot', 'image/{}'.format(filename.split('.')[1]), fp.read())

            mail.send(msg)
            flash('Vaše připomínka byla zaslána na vyšší místa.', 'success')
            return redirect('/')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# S'MORE
@application.route('/changelog')
@login_required
def showChangelog():
    return template('changelog.tpl')


@application.route('/help')
def showHelp():
    return template('help.tpl')


# ERROR
@application.route('/wrongpage')
def wrongPage():
    return template('wrongPage.tpl')


@application.route('/shutdown')
def shutdown():
    return template('shutdown.tpl')


@application.route('/testing')
@admin_required
def testingPage():
    tests = []
    tests.append()
    return template('testing.tpl', tests=tests)


@application.route('/google3748bc0390347e56.html')
def googleVerification():
    return template('google3748bc0390347e56.html')


@application.errorhandler(404)
def error404(error):
    # Missing page
    return template('err404.tpl')


@application.errorhandler(405)
def error405(error):
    # Action not allowed (AJAX)
    return template('wrongPage.tpl')


@application.errorhandler(500)
def error500(error):
    # Internal error
    return template('err500.tpl')


if __name__ == '__main__':
    aplication.run(debug=True)
