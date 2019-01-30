import numpy
import sympy as sp
from sympy import solve_poly_inequality as solvei
from sympy import poly
import math

from flask import Blueprint

calc_blueprint = Blueprint('calc', __name__)


# CALCULATE RECIPE
def calculateRecipe(ingredients, diet):
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
    fixedIngredients = []
    for i in range(len(ingredients)):
        if ingredients[i].fixed is True:

            diet.sugar -= ingredients[i].amount * ingredients[i].sugar
            diet.protein -= ingredients[i].amount * ingredients[i].protein
            diet.fat -= ingredients[i].amount * ingredients[i].fat

            fixedIngredients.append(ingredients[i])

    for ing in fixedIngredients:
        ingredients.remove(ing)

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
        # Teoreticky je možné
        return None
    elif len(ingredients) == 2:
        # Teoreticky je možné
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

    for ing in fixedIngredients:
        ingredients.append(ing)

    diet.expire()
    return ingredients
