import MySQLdb
import db_data as db_data


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

    def __init__(self, dbID, name, calorie, sugar, fat, protein):
        super(Ingredient, self).__init__()
        self.id = dbID
        self.name = name
        self.calorie = calorie
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
    db = MySQLdb.connect(host=db_data.host, port=3306, user=db_data.user, password=db_data.password, database=db_data.database, charset='utf8', init_command='SET NAMES UTF8')
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


def editRecipe(recipe):
    db = dbConnect()
    cursor = db.cursor()

    query = ("UPDATE recipes SET recipes.name = '{}', recipes.type = '{}' WHERE recipes.id = {};".format(recipe.name, recipe.size, recipe.id))
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
    if response is None:
        return None
    else:
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


def editDiet(diet):
    """[summary]

    [description]

    Arguments:
        diet {[type]} -- [description]
    """
    db = dbConnect()
    cursor = db.cursor()

    if hasattr(diet, 'protein'):
        query = ("UPDATE diets SET diets.name = '{}', diets.protein = '{}', diets.fat = '{}', diets.sugar = '{}', diets.small_size = '{}', diets.big_size = '{}' WHERE diets.id = {};".format(diet.name, diet.protein, diet.fat, diet.sugar, diet.small, diet.big, diet.id))
        cursor.execute(query)
    else:
        query = ("UPDATE diets SET diets.name = '{}', diets.small_size = '{}', diets.big_size = '{}' WHERE diets.id = {};".format(diet.name, diet.small, diet.big, diet.id))
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
        temp_ingredient = Ingredient(ingredient[0], ingredient[1], ingredient[2], ingredient[3], ingredient[4], ingredient[5])
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

    ingredient = Ingredient(response[0], response[1], response[2], response[3], response[4], response[5])

    return ingredient


def loadRecipeIngredients(recipeID):
    """load all ingredients for recipe

    [description]

    Arguments:
        recipeID {int} -- [description]

    Returns:
        array -- of Ingredients
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("SELECT recipes_has_ingredients.ingredients_id FROM recipes_has_ingredients WHERE recipes_has_ingredients.recipes_id='{}';".format(int(recipeID)))
    cursor.execute(query)
    response = cursor.fetchall()

    ingredients = []
    for item in response:
        ingredient = loadIngredient(item[0])
        ingredients.append(ingredient)

    return ingredients


def loadAmount(ingredientID, recipeID):
    """[summary]

    [description]recipes_has_ingredients

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

    query = ("INSERT INTO ingredients(name, calorie, sugar, fat, protein, author) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(ingredient.name, ingredient.calorie, ingredient.sugar, ingredient.fat, ingredient.protein, username))
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


def editIngredient(ingredient):
    """[summary]

    [description]

    Arguments:
        ingredient {[type]} -- [description]
    """
    db = dbConnect()
    cursor = db.cursor()

    if hasattr(ingredient, 'protein'):
        query = ("UPDATE ingredients SET ingredients.name = '{}', ingredients.calorie = '{}', ingredients.protein = '{}', ingredients.fat = '{}', ingredients.sugar = '{}' WHERE ingredients.id = {};".format(ingredient.name, ingredient.calorie, ingredient.protein, ingredient.fat, ingredient.sugar, ingredient.id))
        cursor.execute(query)
    else:
        query = ("UPDATE ingredients SET ingredients.name = '{}', ingredients.calorie = '{}' WHERE ingredients.id = {};".format(ingredient.name, ingredient.calorie, ingredient.id))
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
# 