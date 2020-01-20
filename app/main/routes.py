#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Printing
# import pdfkit

# import json


from flask import Blueprint
from flask import render_template as template

from app.models.users import User
from app.models.ingredients import Ingredient


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
