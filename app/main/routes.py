#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Math library
import math
import numpy

# Printing
# import pdfkit

# import requests
import json


from flask import Blueprint
from flask import render_template as template, request, redirect
from flask import jsonify
from flask import flash
from flask import abort

from flask import current_app as application

from flask_login import login_required, current_user


from app import models
from app.main import forms
from app.calc import calculations


main_blueprint = Blueprint('main', __name__)


# USER PAGE
@main_blueprint.route('/', methods=['GET', 'POST'])
@main_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def show_dashboard():
    user = models.User.load(current_user.id)
    if request.method == 'GET':
        if len(user.active_diets) > 0:
            selected_diet = user.active_diets[0]
        else:
            selected_diet = None
        return template('dashboard/dashboard.html.j2', diets=user.active_diets, selected_diet=selected_diet, first_name=user.first_name)
    elif request.method == 'POST':
        selected_diet = models.Diet.load(request.form['select_diet'])
        return template('dashboard/dashboard.html.j2', diets=user.active_diets, selected_diet=selected_diet, first_name=user.first_name)


# NEW DIET
@main_blueprint.route('/newdiet', methods=['GET', 'POST'])
@login_required
def show_new_diet():
    form = forms.NewDietForm()
    if request.method == 'GET':
        return template('diet/new.html.j2', form=form)
    elif request.method == 'POST':
        diet = models.Diet()
        form.populate_obj(diet)
        diet.active = 1
        diet.author = models.User.load(current_user.id)

        if not form.validate_on_submit():
            return template('diet/new.html.j2', form=form)

        if diet.save():
            flash('Nová dieta byla vytvořena', 'success')
            return redirect('/diet={}'.format(diet.id))
        else:
            flash('Nepodařilo se vytvořit dietu', 'error')
            return template('diet/new.html.j2', form=form)

    return template('diet/new.html.j2', form=form)


# SHOW DIET PAGE
@main_blueprint.route('/diet=<int:diet_id>')
@main_blueprint.route('/diet=<int:diet_id>/<page_type>', methods=['POST', 'GET'])
@login_required
def show_diet(diet_id, page_type=None):
    diet = models.Diet.load(diet_id)

    if diet is None:
        abort(404)
    elif diet.author.username != current_user.username:
        abort(405)

    if request.method == 'GET':
        if page_type == 'edit':
            return template('diet/edit.html.j2', diet=diet, recipes=diet.recipes, diets=diet.author.diets)
        else:
            return template('diet/show.html.j2', diet=diet, recipes=diet.recipes, diets=diet.author.diets)
    elif request.method == 'POST':
        if page_type == 'remove':
            # TODO enable deleting diet with all recipes
            if not diet.is_used:
                diet.remove()
                flash('Dieta byla smazána', 'success')
                return redirect('/alldiets')
            else:
                flash('Tato dieta má recepty, nelze smazat', 'error')
                return redirect('/diet={}'.format(diet_id))
        elif page_type == 'archive':
            diet.refresh()
            diet.active = not diet.active
            diet.edit()

            if diet.active:
                flash('Dieta byla aktivována', 'success')
            else:
                flash('Dieta byla archivována', 'success')

            return redirect('/diet={}'.format(diet_id))
        elif page_type == 'edit':
            diet.name = request.form['name']
            diet.id = diet_id
            diet.small_size = request.form['small_size']
            diet.big_size = request.form['big_size']

            if not diet.is_used:
                diet.protein = request.form['protein']
                diet.fat = request.form['fat']
                diet.sugar = request.form['sugar']

            diet.edit()
            flash('Dieta byla upravena.', 'success')
            return redirect('/diet={}'.format(diet_id))
        else:
            return abort(404)


@main_blueprint.route('/alldiets')
@login_required
def show_all_diets():
    """show all diets sorted (active first)

    active on top

    Decorators:
        application.route

    Returns:
        template -- [description]
    """
    diets = models.User.load(current_user.id).diets
    diets.sort(key=lambda x: (-x.active, x.name))

    return template('diet/all.html.j2', diets=diets)


# NEW RECIPE PAGE
@main_blueprint.route('/trialnewrecipe')
def show_trial_new_recipe():
    active_diets = models.User.load('ketocalc.jmp@gmail.com', load_type="username").active_diets
    ingredients = models.Ingredient.load_all_by_author('basic')
    return template('recipe/new.html.j2', ingredients=ingredients, diets=active_diets, is_trialrecipe=True)


@main_blueprint.route('/newrecipe')
@login_required
def show_new_recipe():
    active_diets = models.User.load(current_user.id).active_diets
    ingredients = models.Ingredient.load_all_by_author(current_user.username)
    return template('recipe/new.html.j2', ingredients=ingredients, diets=active_diets, is_trialrecipe=False)


@main_blueprint.route('/addIngredientAJAX', methods=['POST'])
def add_ingredient_to_recipe_AJAX():
    ingredient = models.Ingredient.load(request.json['ingredient_id'])
    template_data = template('recipe/_add_ingredient.html.j2', ingredient=ingredient)
    result = {'ingredient': ingredient.json, 'template_data': template_data}
    return jsonify(result)


@main_blueprint.route('/calcRecipeAJAX', methods=['POST'])
def calculate_recipe_AJAX():

    json_ingredients = request.json['ingredients']
    diet = models.Diet.load(request.json['dietID'])
    if 'trial' in request.json and request.json['trial'] == 'True':
        is_trialrecipe = True
    else:
        is_trialrecipe = False

    if diet is None:
        return 'False'

    ingredients = []
    for json_i in json_ingredients:
        ingredient = models.Ingredient.load(json_i['id'])
        if 'fixed' in json_i:
            ingredient.fixed = json_i['fixed']
        if 'main' in json_i:
            ingredient.main = json_i['main']
        if 'amount' in json_i:
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

        ing.calorie = round(ing.calorie * ing.amount, 2)
        ing.fat = round(ing.fat * ing.amount, 2)
        ing.sugar = round(ing.sugar * ing.amount, 2)
        ing.protein = round(ing.protein * ing.amount, 2)
        ing.amount = round(ing.amount * 100, 2)

        totals.sugar += ing.sugar
        totals.fat += ing.fat
        totals.protein += ing.protein
        totals.amount += ing.amount
        totals.calorie += ing.calorie

        json_ingredients.append(ing.json)

    totals.calorie = round(totals.calorie, 2)
    totals.sugar = round(totals.sugar, 2)
    totals.fat = round(totals.fat, 2)
    totals.protein = round(totals.protein, 2)
    totals.amount = round(totals.amount, 2)
    totals.ratio = round((totals.fat / (totals.protein + totals.sugar)), 2)

    template_data = template('recipe/_right_form.tpl', ingredients=ingredients, totals=totals, diet=diet, is_trialrecipe=is_trialrecipe)

    result = {'template_data': str(template_data), 'totals': json.dumps(totals.__dict__), 'ingredients': json_ingredients, 'diet': diet.json}

    # reset ingredients (so they are not changed in db)
    for ing in ingredients:
        ing.expire()

    return jsonify(result)


@main_blueprint.route('/recalcRecipeAJAX', methods=['POST'])
def recalcRecipeAJAX():
    # TODO need to rewrite -> use calcRecipeAJAX instead

    json_ingredients = request.json['ingredients']
    diet = models.Diet.load(request.json['dietID'])

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


@main_blueprint.route('/saveRecipeAJAX', methods=['POST'])
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


@main_blueprint.route('/recipe=<int:recipe_id>', methods=['GET'])
@main_blueprint.route('/recipe=<int:recipe_id>/<page_type>', methods=['POST', 'GET'])
@login_required
def show_recipe(recipe_id, page_type=None):
    recipe = models.Recipe.load(recipe_id)
    if recipe is None:
        return abort(404)

    if current_user.username != recipe.author.username:
        return redirect('/wrongpage')

    if request.method == 'GET':
        if page_type == 'print':
            return template('recipe/show.html.j2', recipe=recipe, totals=recipe.totals, is_print=True)
        elif page_type == 'edit':
            return template('recipe/edit.html.j2', recipe=recipe, totals=recipe.totals)
        else:
            if application.config['APP_STATE'] == 'production':
                if recipe.view_count is not None:
                    recipe.view_count += 1
                else:
                    recipe.view_count = 1
                recipe.edit()
            return template('recipe/show.html.j2', recipe=recipe, totals=recipe.totals, is_print=False)
    elif request.method == 'POST':
        if page_type == 'edit':
            recipe.name = request.form['name']
            recipe.type = request.form['size']
            recipe.edit()
            recipe.refresh()
            flash('Recept byl upraven.', 'success')
            return redirect('/recipe={}'.format(recipe_id))
        elif page_type == 'remove':
            recipe.remove()
            flash('Recept byl smazán.', 'success')
            return redirect('/')
        else:
            return abort(404)


@main_blueprint.route('/allrecipes')
@login_required
def show_all_recipes():
    user = models.User.load(current_user.id)
    return template('recipe/all.html.j2', diets=user.active_diets)


@main_blueprint.route('/printallrecipes')
@main_blueprint.route('/diet=<int:diet_id>/print')
@login_required
def print_recipes(diet_id=None):
    if diet_id is None:
        recipes = models.User.load(current_user.id).recipes
    else:
        recipes = models.Diet.load(diet_id).recipes

    for recipe in recipes:
        recipe_data = recipe.load_recipe_for_show()
        recipe.show_totals = recipe_data['totals']
    return template('recipe/print_all.html.j2', recipes=recipes)


# NEW INGREDIENT PAGE
@main_blueprint.route('/newingredient', methods=['GET', 'POST'])
@login_required
def show_new_ingredient():
    form = forms.NewIngredientForm()
    if request.method == 'GET':
        return template('ingredient/new.html.j2', form=form)
    elif request.method == 'POST':
        ingredient = models.Ingredient()
        form.populate_obj(ingredient)
        ingredient.author = current_user.username
        if not form.validate_on_submit():
            return template('ingredient/new.html.j2', form=form)

        if ingredient.save():
            flash('Nová surovina byla vytvořena', 'success')
            return redirect('/ingredient={}'.format(ingredient.id))
        else:
            flash('Nepodařilo se vytvořit surovinu', 'error')
            return template('ingredient/new.html.j2', form=form)


@main_blueprint.route('/ingredient=<int:ingredient_id>')
@main_blueprint.route('/ingredient=<int:ingredient_id>/<page_type>', methods=['POST', 'GET'])
@login_required
def show_ingredient(ingredient_id, page_type=None):
    ingredient = models.Ingredient.load(ingredient_id)
    if ingredient is None:
        abort(404)

    if current_user.username != ingredient.author:
        return redirect('/wrongpage')

    if request.method == 'GET':
        if page_type == 'edit':
            recipes = models.Recipe.load_by_ingredient(ingredient.id)
            return template('ingredient/edit.html.j2', ingredient=ingredient, recipes=recipes)
        if page_type is None:
            # TODO -> if multiple users user same ingredient, they see each other recipes. probably should load_by_ingredient_and_recipe_author
            recipes = models.Recipe.load_by_ingredient(ingredient.id)
            return template('ingredient/show.html.j2', ingredient=ingredient, recipes=recipes)
    elif request.method == 'POST':
        if page_type == 'edit':
            ingredient.id = ingredient_id
            ingredient.name = request.form['name']
            ingredient.calorie = request.form['calorie']
            if not ingredient.is_used:
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

        elif page_type == 'remove':
            if not ingredient.is_used:
                ingredient.remove()
                flash('Surovina byla smazána', 'success')
                return redirect('/')
            else:
                flash('Tato surovina je použita, nelze smazat', 'error')
                return redirect('/ingredient={}'.format(ingredient_id))


@main_blueprint.route('/allingredients')
@login_required
def show_all_ingredients():
    # basic_ingredients = models.Ingredient.load_all_by_author('default')
    ingredients = models.Ingredient.load_all_by_author(current_user.username)
    return template('ingredient/all.html.j2', ingredients=ingredients)


# USER PAGES
@main_blueprint.route('/user')
@main_blueprint.route('/user/<page_type>', methods=['POST', 'GET'])
@login_required
def show_user(page_type=None):
    try:
        user = models.User.load(current_user.id)
        if user is None:
            abort(404)
    except Exception:
        abort(500)

    if request.method == 'GET':
        if page_type == 'edit':
            return template('user/edit.html.j2', user=user)
        if page_type is None:
            return template('user/show.html.j2', user=user)
    elif request.method == 'POST':
        if page_type == 'edit':
            user.first_name = request.form['firstname']
            user.last_name = request.form['lastname']
            success = user.edit()
            if success is not None:
                flash('Uživatel byl upraven', 'success')
            else:
                flash('Nepovedlo se změnit uživatele', 'error')
            return template('user/show.html.j2', user=user)
        elif page_type == 'password_change':

            user.set_password_hash(request.form['password'].encode('utf-8'))
            user.password_version = 'bcrypt'

            if user.edit():
                flash('Heslo bylo změněno', 'success')
            else:
                flash('Nepovedlo se změnit heslo', 'error')
            return template('user/show.html.j2', user=user)
