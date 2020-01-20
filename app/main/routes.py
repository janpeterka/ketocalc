#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Printing
# import pdfkit

import json


from flask import Blueprint
from flask import render_template as template, request, redirect
from flask import jsonify
from flask import flash
from flask import abort

from flask import current_app as application

from flask_login import login_required, current_user


from app.models.users import User
from app.models.diets import Diet
from app.models.ingredients import Ingredient
from app.models.recipes import Recipe
from app.models.recipe_has_ingredient import RecipesHasIngredient

# from app.main import forms
from app.calc import calculations


main_blueprint = Blueprint("main", __name__)


# USER PAGE
@main_blueprint.route("/", methods=["GET", "POST"])
@main_blueprint.route("/dashboard", methods=["GET", "POST"])
@login_required
def show_dashboard():
    user = User.load(current_user.id)
    if request.method == "GET":
        if len(user.active_diets) > 0:
            selected_diet = user.active_diets[0]
        else:
            selected_diet = None
        return template(
            "dashboard/dashboard.html.j2",
            diets=user.active_diets,
            selected_diet=selected_diet,
            first_name=user.first_name,
        )
    elif request.method == "POST":
        selected_diet = Diet.load(request.form["select_diet"])
        return template(
            "dashboard/dashboard.html.j2",
            diets=user.active_diets,
            selected_diet=selected_diet,
            first_name=user.first_name,
        )


# NEW RECIPE PAGE
@main_blueprint.route("/trialnewrecipe")
def show_trial_new_recipe():
    active_diets = User.load(
        "ketocalc.jmp@gmail.com", load_type="username"
    ).active_diets
    ingredients = Ingredient.load_all_by_author("basic")
    return template(
        "recipe/new.html.j2",
        ingredients=ingredients,
        diets=active_diets,
        is_trialrecipe=True,
    )


@main_blueprint.route("/newrecipe")
@login_required
def show_new_recipe():
    active_diets = User.load(current_user.id).active_diets
    ingredients = Ingredient.load_all_by_author(current_user.username)
    return template(
        "recipe/new.html.j2",
        ingredients=ingredients,
        diets=active_diets,
        is_trialrecipe=False,
    )


@main_blueprint.route("/addIngredientAJAX", methods=["POST"])
def add_ingredient_to_recipe_AJAX():
    ingredient = Ingredient.load(request.json["ingredient_id"])
    template_data = template("recipe/_add_ingredient.html.j2", ingredient=ingredient)
    result = {"ingredient": ingredient.json, "template_data": template_data}
    return jsonify(result)


@main_blueprint.route("/calcRecipeAJAX", methods=["POST"])
def calculate_recipe_AJAX():

    json_ingredients = request.json["ingredients"]
    diet = Diet.load(request.json["dietID"])
    if "trial" in request.json and request.json["trial"] == "True":
        is_trialrecipe = True
    else:
        is_trialrecipe = False

    if diet is None:
        return "False"

    ingredients = []
    for json_i in json_ingredients:
        ingredient = Ingredient.load(json_i["id"])
        ingredient.fill_from_json(json_i)
        ingredients.append(ingredient)

    result = calculations.calculate_recipe(ingredients, diet)
    if result is None:
        return "False"

    ingredients = result["ingredients"]
    totals = result["totals"]

    json_ingredients = []
    for ing in ingredients:
        if ing.amount < 0:
            return "False"

        ing.calorie = round(ing.calorie * ing.amount, 2)
        ing.fat = round(ing.fat, 2)
        ing.sugar = round(ing.sugar, 2)
        ing.protein = round(ing.protein, 2)
        ing.amount = round(ing.amount * 100, 2)

        json_ingredients.append(ing.json)

    totals.calorie = round(totals.calorie, 2)
    totals.sugar = round(totals.sugar, 2)
    totals.fat = round(totals.fat, 2)
    totals.protein = round(totals.protein, 2)
    totals.amount = round(totals.amount, 2)
    totals.ratio = round((totals.fat / (totals.protein + totals.sugar)), 2)

    template_data = template(
        "recipe/_right_form.html.j2",
        ingredients=ingredients,
        totals=totals,
        diet=diet,
        is_trialrecipe=is_trialrecipe,
    )

    result = {
        "template_data": str(template_data),
        "totals": json.dumps(totals.__dict__),
        "ingredients": json_ingredients,
        "diet": diet.json,
    }

    # reset ingredients (so they are not changed in db)
    for ing in ingredients:
        ing.expire()

    return jsonify(result)


@main_blueprint.route("/saveRecipeAJAX", methods=["POST"])
@login_required
def saveRecipeAJAX():
    temp_ingredients = request.json["ingredients"]
    diet_id = request.json["dietID"]

    ingredients = []
    for temp_i in temp_ingredients:
        rhi = RecipesHasIngredient()
        rhi.ingredients_id = temp_i["id"]
        rhi.amount = temp_i["amount"]
        ingredients.append(rhi)

    recipe = Recipe()
    recipe.name = request.json["name"]
    recipe.type = request.json["size"]
    recipe.diet = Diet.load(diet_id)

    last_id = recipe.save(ingredients)
    flash("Recept byl uložen", "success")
    return "/recipe=" + str(last_id)


@main_blueprint.route("/recipe=<int:recipe_id>", methods=["GET"])
@main_blueprint.route("/recipe=<int:recipe_id>/<page_type>", methods=["POST", "GET"])
@login_required
def show_recipe(recipe_id, page_type=None):
    recipe = Recipe.load(recipe_id)
    if recipe is None:
        return abort(404)

    if current_user.username != recipe.author.username:
        return redirect("/wrongpage")

    if request.method == "GET":
        if page_type == "print":
            return template(
                "recipe/show.html.j2",
                recipe=recipe,
                totals=recipe.totals,
                is_print=True,
            )
        elif page_type == "edit":
            return template("recipe/edit.html.j2", recipe=recipe, totals=recipe.totals)
        else:
            if application.config["APP_STATE"] == "production":
                if recipe.view_count is not None:
                    recipe.view_count += 1
                else:
                    recipe.view_count = 1
                recipe.edit()
            return template(
                "recipe/show.html.j2",
                recipe=recipe,
                totals=recipe.totals,
                is_print=False,
            )
    elif request.method == "POST":
        if page_type == "edit":
            recipe.name = request.form["name"]
            recipe.type = request.form["size"]
            recipe.edit()
            recipe.refresh()
            flash("Recept byl upraven.", "success")
            return redirect("/recipe={}".format(recipe_id))
        elif page_type == "remove":
            recipe.remove()
            flash("Recept byl smazán.", "success")
            return redirect("/")
        else:
            return abort(404)


@main_blueprint.route("/allrecipes")
@login_required
def show_all_recipes():
    user = User.load(current_user.id)
    return template("recipe/all.html.j2", diets=user.active_diets)


@main_blueprint.route("/printallrecipes")
@main_blueprint.route("/diet=<int:diet_id>/print")
@login_required
def print_recipes(diet_id=None):
    if diet_id is None:
        recipes = User.load(current_user.id).recipes
    else:
        recipes = Diet.load(diet_id).recipes

    for recipe in recipes:
        recipe_data = recipe.load_recipe_for_show()
        recipe.show_totals = recipe_data["totals"]
    return template("recipe/print_all.html.j2", recipes=recipes)


# USER PAGES
@main_blueprint.route("/user")
@main_blueprint.route("/user/<page_type>", methods=["POST", "GET"])
@login_required
def show_user(page_type=None):
    user = User.load(current_user.id)
    if user is None:
        abort(404)

    if request.method == "GET":
        if page_type == "edit":
            return template("user/edit.html.j2", user=user)
        if page_type is None:
            return template("user/show.html.j2", user=user)
    elif request.method == "POST":
        if page_type == "edit":
            user.first_name = request.form["firstname"]
            user.last_name = request.form["lastname"]
            success = user.edit()
            if success is not None:
                flash("Uživatel byl upraven", "success")
            else:
                flash("Nepovedlo se změnit uživatele", "error")
            return template("user/show.html.j2", user=user)
        elif page_type == "password_change":

            user.set_password_hash(request.form["password"].encode("utf-8"))
            user.password_version = "bcrypt"

            if user.edit():
                flash("Heslo bylo změněno", "success")
            else:
                flash("Nepovedlo se změnit heslo", "error")
            return template("user/show.html.j2", user=user)
