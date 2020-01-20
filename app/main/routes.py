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
