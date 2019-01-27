#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run by pyserver

from flask import render_template as template, request, redirect
from flask import jsonify
from flask import flash
from flask import abort

from flask_mail import Message
from werkzeug import secure_filename

# import requests
# import json

from app import models

from app.main import forms
from app.main import bp as main_bp
from app import mail

from app.calc import calculations

# from utils import *

# Math library
import numpy
import math
import os

from flask_login import login_required, current_user
# Printing
# import pdfkit

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


# MAIN
@main_bp.route('/', methods=['GET'])
def main():
    return redirect('/dashboard')


# USER PAGE
@main_bp.route('/dashboard')
@login_required
def showDashboard():
    user = models.User.load(current_user.id)
    return template('dashboard.tpl', diets=user.activeDiets, firstname=user.firstName)


@main_bp.route('/selectDietAJAX', methods=['POST'])
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
@main_bp.route('/newdiet', methods=['GET', 'POST'])
@login_required
def showNewDiet():
    form = forms.NewDietForm()
    if request.method == 'GET':
        return template('diet/new.tpl', form=form)
    elif request.method == 'POST':
        diet = models.Diet()
        diet.name = form.name.data
        diet.calorie = form.calorie.data
        diet.sugar = form.sugar.data
        diet.fat = form.fat.data
        diet.protein = form.protein.data
        diet.small_size = form.small_size.data
        diet.big_size = form.big_size.data
        diet.active = 1
        diet.author = models.User.load(current_user.id)

        if not form.validate_on_submit():
            return template('diet/new.tpl', form=form)

        if diet.save():
            flash('Nová dieta byla vytvořena', 'success')
            return redirect('/diet={}'.format(diet.id))
        else:
            flash('Nepodařilo se vytvořit dietu', 'error')
            return template('diet/new.tpl', form=form)

    return template('diet/new.tpl')


# SHOW DIET PAGE
@main_bp.route('/diet=<int:diet_id>')
@main_bp.route('/diet=<int:diet_id>/<page_type>', methods=['POST', 'GET'])
@login_required
def showDiet(diet_id, page_type=None):
    diet = models.Diet.load(diet_id)
    if diet is None:
        abort(404)
    if diet.author.username != current_user.username:
        return redirect('/wrongpage')

    if page_type is None:
        return template('diet/show.tpl', diet=diet, recipes=diet.recipes, diets=diet.author.diets)
    elif page_type == 'remove' and request.method == 'POST':
        if not diet.used:  # wip
            diet.remove()
            flash('Dieta byla smazána', 'success')
            return redirect('/alldiets')
        else:
            flash('Tato dieta má recepty, nelze smazat', 'error')
            return redirect('/diet={}'.format(diet_id))
    elif page_type == 'archive' and request.method == 'POST':
        flash('Dieta byla archivována', 'success') if diet.active else flash('Dieta byla aktivována', 'success')
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


# @main_bp.route('/diet=<dietID>/export', methods=['POST'])
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


@main_bp.route('/alldiets')
@login_required
def showAllDiets():
    """show all diets sorted (active first)

    active on top

    Decorators:
        application.route

    Returns:
        template -- [description]
    """
    diets = models.User.load(current_user.id).diets
    diets.sort(key=lambda x: (-x.active, x.name))

    return template('diet/all.tpl', diets=diets)


# NEW RECIPE PAGE
@main_bp.route('/trialnewrecipe')
def showTrialNewRecipe():
    active_diets = models.User.load('ketocalc.jmp@gmail.com', load_type="username").activeDiets
    ingredients = models.Ingredient.loadAllByAuthor('basic')
    return template('recipe/new.tpl', ingredients=ingredients, diets=active_diets, trialrecipe=True)


@main_bp.route('/newrecipe')
@login_required
def showNewRecipe():
    active_diets = models.User.load(current_user.id).activeDiets
    ingredients = models.Ingredient.loadAllByAuthor(current_user.username)
    return template('recipe/new.tpl', ingredients=ingredients, diets=active_diets, trialrecipe=False)


@main_bp.route('/addIngredientAJAX', methods=['POST'])
def addIngredienttoRecipeAJAX():
    ingredient = models.Ingredient.load(request.json['ingredient_id'])
    template_data = template('recipe/addingredientAJAX.tpl', ingredient=ingredient)
    result = {'ingredient': ingredient.json, 'template_data': template_data}
    return jsonify(result)


@main_bp.route('/calcRecipeAJAX', methods=['POST'])
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
    # end testing

    if diet is None:
        return 'False'

    ingredients = []
    for json_i in json_ingredients:
        ingredient = models.Ingredient.load(json_i['id'])
        ingredient.fixed = json_i['fixed']
        ingredient.main = json_i['main']
        ingredient.amount = float(json_i['amount']) / 100  # from grams per 100g
        ingredients.append(ingredient)

    ingredients = calculations.calculateRecipe(ingredients, diet)

    if ingredients is None:
        return 'False'

    totals = type('', (), {})()
    totals.sugar = 0
    totals.fat = 0
    totals.protein = 0
    totals.amount = 0
    totals.calorie = 0

    json_ingredients = []
    for ing in ingredients:

        if ing.amount < 0:
            return 'False'

        if hasattr(ing, 'min'):
            json_ingredient = {'id': ing.id, 'calorie': math.floor(ing.calorie * ing.amount * 100) / 100, 'name': ing.name, 'sugar': math.floor(ing.sugar * ing.amount * 100) / 100, 'fat': math.floor(ing.fat * ing.amount * 100) / 100, 'protein': math.floor(ing.protein * ing.amount * 100) / 100, 'amount': math.floor(ing.amount * 10000) / 100, 'main': ing.main, 'fixed': ing.fixed, 'min': ing.min, 'max': ing.max}  # wip
            # json_ingredient = {'id': ing.id, }
        else:
            json_ingredient = {'id': ing.id, 'calorie': math.floor(ing.calorie * ing.amount * 100) / 100, 'name': ing.name, 'sugar': math.floor(ing.sugar * ing.amount * 100) / 100, 'fat': math.floor(ing.fat * ing.amount * 100) / 100, 'protein': math.floor(ing.protein * ing.amount * 100) / 100, 'amount': math.floor(ing.amount * 10000) / 100, 'main': ing.main, 'fixed': ing.fixed}  # wip
            # json_ingredient = {'id': ing.id, }

        json_ingredients.append(json_ingredient)

        ing.calorie = math.floor(ing.calorie * ing.amount * 100) / 100
        ing.fat = math.floor(ing.fat * ing.amount * 100) / 100
        ing.sugar = math.floor(ing.sugar * ing.amount * 100) / 100
        ing.protein = math.floor(ing.protein * ing.amount * 100) / 100
        ing.amount = math.floor(ing.amount * 10000) / 100

        totals.sugar += ing.sugar
        totals.fat += ing.fat
        totals.protein += ing.protein
        totals.amount += ing.amount
        totals.calorie += ing.calorie

        ing.expire()

    totals.calorie = math.floor(totals.calorie * 100) / 100
    totals.sugar = math.floor(totals.sugar * 100) / 100
    totals.fat = math.floor(totals.fat * 100) / 100
    totals.protein = math.floor(totals.protein * 100) / 100
    totals.amount = math.floor(totals.amount * 100) / 100

    totals.ratio = math.floor((totals.fat / (totals.protein + totals.sugar)) * 100) / 100

    if request.json['trial'] == 'True':
        template_data = template('recipe/newreciperightform.tpl', ingredients=ingredients, totals=totals, diet=diet, trialrecipe=True)
    else:
        template_data = template('recipe/newreciperightform.tpl', ingredients=ingredients, totals=totals, diet=diet, trialrecipe=False)

    result = {'template_data': str(template_data), 'ingredients': json_ingredients, 'diet': diet.json}

    return jsonify(result)


@main_bp.route('/recalcRecipeAJAX', methods=['POST'])
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


@main_bp.route('/saveRecipeAJAX', methods=['POST'])
@login_required
def saveRecipeAJAX():
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


@main_bp.route('/recipe=<int:recipe_id>', methods=['GET'])
@main_bp.route('/recipe=<int:recipe_id>/<page_type>', methods=['POST', 'GET'])
@login_required
def showRecipe(recipe_id, page_type=None):
    try:
        recipe = models.Recipe.load(recipe_id)
        recipe_data = recipe.loadRecipeForShow()
    except AttributeError:
        return abort(404)

    if current_user.username != recipe.author.username:
        return redirect('/wrongpage')

    if page_type is None:
        try:
            recipe.view_count += 1
        except Exception:
            recipe.view_count = 1
        return template('recipe/show.tpl', recipe=recipe_data['recipe'], totals=recipe_data['totals'], show=True)
    elif page_type == 'print':
        return template('recipe/show.tpl', recipe=recipe_data['recipe'], totals=recipe_data['totals'], show=False)
    elif page_type == 'edit' and request.method == 'POST':
        recipe = recipe_data['recipe']
        recipe.name = request.form['name']
        recipe.type = request.form['size']
        recipe.edit()
        recipe.refresh()
        flash('Recept byl upraven.', 'success')
        return redirect('/recipe={}'.format(recipe_id))
    elif page_type == 'remove' and request.method == 'POST':
        recipe = recipe_data['recipe']
        recipe.remove()
        flash('Recept byl smazán.', 'success')
        return redirect('/')
    else:
        redirect('/wrongpage')


@main_bp.route('/allrecipes')
@login_required
def showAllRecipes():
    user = models.User.load(current_user.id)
    return template('recipe/all.tpl', diets=user.activeDiets)


@main_bp.route('/diet=<int:diet_id>/print')
@login_required
def printDietRecipes(diet_id):
    diet = models.Diet.load(diet_id)
    for recipe in diet.recipes:
        recipe_data = recipe.loadRecipeForShow()
        recipe.totals = recipe_data['totals']
    return template('recipe/printAll.tpl', recipes=diet.recipes)


@main_bp.route('/printallrecipes')
@login_required
def printAllRecipes():
    recipes = models.User.load(current_user.id).recipes
    for recipe in recipes:
        recipe_data = recipe.loadRecipeForShow()
        recipe.totals = recipe_data['totals']
    return template('recipe/printAll.tpl', recipes=recipes)


# NEW INGREDIENT PAGE
@main_bp.route('/newingredient', methods=['GET', 'POST'])
@login_required
def showNewIngredient():
    form = forms.NewIngredientForm()
    if request.method == 'GET':
        return template('ingredient/new.tpl', form=form)
    elif request.method == 'POST':
        ingredient = models.Ingredient()
        ingredient.name = form.name.data
        ingredient.calorie = form.calorie.data
        ingredient.sugar = form.sugar.data
        ingredient.fat = form.fat.data
        ingredient.protein = form.protein.data
        ingredient.author = current_user.username
        if not form.validate_on_submit():
            return template('ingredient/new.tpl', form=form)

        if ingredient.save():
            flash('Nová surovina byla vytvořena', 'success')
            return redirect('/ingredient={}'.format(ingredient.id))
        else:
            flash('Nepodařilo se vytvořit surovinu', 'error')
            return template('ingredient/new.tpl', form=form)


@main_bp.route('/ingredient=<int:ingredient_id>')
@main_bp.route('/ingredient=<int:ingredient_id>/<page_type>', methods=['POST', 'GET'])
@login_required
def showIngredient(ingredient_id, page_type=None):
    ingredient = models.Ingredient.load(ingredient_id)
    if ingredient is None:
        abort(404)
    if current_user.username != ingredient.author:
        return redirect('/wrongpage')

    if page_type is None:
        recipes = models.Recipe.loadByIngredient(ingredient.id)
        return template('ingredient/show.tpl', ingredient=ingredient, recipes=recipes)

    elif page_type == 'edit' and request.method == 'POST':
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

    elif page_type == 'remove' and request.method == 'POST':
        if not ingredient.used:
            ingredient.remove()
            flash('Surovina byla smazána', 'success')
            return redirect('/')
        else:
            flash('Tato surovina je použita, nelze smazat', 'error')
            return redirect('/ingredient={}'.format(ingredient_id))


@main_bp.route('/allingredients')
@login_required
def showAllIngredients():
    # basic_ingredients = models.Ingredient.loadAllByAuthor('default')
    ingredients = models.Ingredient.loadAllByAuthor(current_user.username)
    return template('ingredient/all.tpl', ingredients=ingredients)


@main_bp.route('/user')
@main_bp.route('/user/<page_type>', methods=['POST', 'GET'])
@login_required
def showUser(page_type=None):
    user = models.User.load(current_user.id)
    if user is None:
        return redirect('/wrongpage')
    if page_type is None:
        return template('user/show.tpl', user=user)
    elif page_type == 'edit' and request.method == 'POST':
        user.firstName = request.form['firstname']
        user.lastName = request.form['lastname']
        success = user.edit()
        if success is not None:
            flash('Uživatel byl upraven', 'success')
        else:
            flash('Nepovedlo se změnit uživatele', 'error')
        return template('user/show.tpl', user=user)
    elif page_type == 'password_change' and request.method == 'POST':

        user.pwdhash = user.getPassword(request.form['password'].encode('utf-8'))
        user.password_version = 'bcrypt'

        success = user.edit()
        if success is True:
            flash('Heslo bylo změněno', 'success')
        else:
            flash('Nepovedlo se změnit heslo', 'error')
        return template('user/show.tpl', user=user)


@main_bp.route('/feedback', methods=['GET', 'POST'])
@login_required
def showFeedback():
    if request.method == 'GET':
        return template('feedback.tpl')
    elif request.method == 'POST':
        msg = Message('[ketocalc] [{}]'.format(request.form['type']), sender='ketocalc', recipients=['ketocalc.jmp@gmail.com'])
        msg.body = 'Message: {}\n'.format(request.form['message'])
        msg.body += 'Send by: {} [user: {}]'.format(request.form['sender'], current_user.username)

        if 'file' not in request.files:
            try:
                mail.send(msg)
                flash('Vaše připomínka byla zaslána na vyšší místa.', 'success')
                return redirect('/')
            except Exception as error:
                print(error)
                abort(500)
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
@main_bp.route('/changelog')
@login_required
def showChangelog():
    return template('changelog.tpl')


@main_bp.route('/help')
def showHelp():
    return template('help.tpl')


# if __name__ == '__main__':
#     aplication.run(debug=True)
