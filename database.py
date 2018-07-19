import MySQLdb
import db_data as db_data


def temp_print(input):
    print(input)


class Diet(object):
    """  For loading from database """

    def __init__(self, dbID, name, sugar, fat, protein, small_size, big_size, active, author):
        super(Diet, self).__init__()
        self.id = dbID
        self.name = name
        self.sugar = sugar
        self.fat = fat
        self.protein = protein
        self.small_size = small_size
        self.big_size = big_size
        self.author = author
        if active == 1:
            self.active = True
        else:
            self.active = False
        self.json = {'id': self.id, 'name': self.name, 'sugar': self.sugar, 'fat': self.fat,
                     'protein': self.protein, 'small_size': self.small_size, 'big_size': self.big_size}


class Recipe(object):
    """  For loading from database """

    def __init__(self, dbID, name, size):
        super(Recipe, self).__init__()
        self.id = dbID
        self.name = name
        self.size = size
        self.json = {'id': self.id, 'name': self.name, 'size': self.size}


class Ingredient(object):
    """  For loading from database """

    def __init__(self, dbID, name, calorie, sugar, fat, protein, author):
        super(Ingredient, self).__init__()
        self.id = dbID
        self.name = name
        self.calorie = calorie
        self.sugar = sugar
        self.fat = fat
        self.protein = protein
        self.amount = 0
        self.author = author
        self.json = {'id': self.id, 'name': self.name, 'calorie': self.calorie, 'sugar': self.sugar, 'fat': self.fat, 'protein': self.protein}


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

    query = ("""

        SELECT
            R.id, R.name, R.type, U.username
        FROM
            recipes AS R
            JOIN diets_has_recipes AS DR ON DR.recipes_id = R.id
            JOIN users_has_diets AS UR ON UR.diets_id = DR.diets_id
            JOIN users AS U ON U.id = UR.users_id
        WHERE
            R.id=%s;

        """)
    cursor.execute(query, (recipeID,))
    response = cursor.fetchone()
    if response is None:
        return None

    recipe = Recipe(response[0], response[1], response[2])
    author = response[3]

    query = ("""

        SELECT
            recipes_has_ingredients.ingredients_id
        FROM
            recipes_has_ingredients
        WHERE
            recipes_has_ingredients.recipes_id=%s;

        """)
    cursor.execute(query, (recipeID,))
    response = cursor.fetchall()

    ingredientIDs = []
    for i in range(len(response)):
        ingredientIDs.append(response[i][0])

    return [recipe, ingredientIDs, author]


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

    query = ("""

        INSERT INTO
            recipes(name, type)
        VALUES
            (%s, %s);

        """)
    cursor.execute(query, (recipe.name, recipe.size))
    last_id = db.insert_id()

    for ingredient in ingredients:
        query = ("""

            INSERT INTO
                recipes_has_ingredients(recipes_id, ingredients_id, amount)
            VALUES
                (%s, %s, %s);

            """)
        cursor.execute(query, (last_id, ingredient.id, ingredient.amount))

    query = ("""

        INSERT INTO
            diets_has_recipes(diets_id, recipes_id)
        VALUES
            (%s, %s);

        """)
    cursor.execute(query, (dietID, last_id))

    db.commit()

    return last_id


def deleteRecipe(recipeID):
    """Delete recipe from database

    Arguments:
        recipeID {int} -- ID of recipe to be removed
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("""

        DELETE FROM
            diets_has_recipes
        WHERE
            diets_has_recipes.recipes_id = %s;

        """)
    cursor.execute(query, (recipeID,))

    query = ("""

        DELETE FROM
            recipes_has_ingredients
        WHERE
            recipes_has_ingredients.recipes_id = %s;

        """)
    cursor.execute(query, (recipeID,))

    query = ("""

        DELETE FROM
            recipes
        WHERE
            recipes.id = %s;

        """)
    cursor.execute(query, (recipeID,))

    db.commit()


def editRecipe(recipe):
    db = dbConnect()
    cursor = db.cursor()

    query = ("""

        UPDATE
            recipes
        SET
            recipes.name = %s, recipes.type = %s
        WHERE
            recipes.id = %s;

        """)
    cursor.execute(query, (recipe.name, recipe.size, recipe.id))
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
    query = ("""

        SELECT
            DR.diets_id
        FROM
            diets_has_recipes AS DR
        WHERE
            DR.recipes_id = %s;

        """)
    cursor.execute(query, (recipeID,))
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
    query = ("""

        SELECT
            DR.recipes_id
        FROM
            diets_has_recipes AS DR
        WHERE
            DR.diets_id = %s;

        """)
    cursor.execute(query, (dietID,))
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

    query = ("""

        SELECT
            D.id,
            D.name,
            D.sugar,
            D.fat,
            D.protein,
            D.small_size,
            D.big_size,
            D.active,
            U.username
        FROM
            diets AS D
            JOIN users_has_diets AS UD ON UD.diets_id = D.id
            JOIN users AS U ON U.id = UD.users_id
        WHERE
            D.id=%s;

        """)
    cursor.execute(query, (dietID,))
    response = cursor.fetchone()
    if response is None:
        return None
    else:
        diet = Diet(response[0], response[1], response[2], response[3], response[4], response[5], response[6], response[7], response[8])
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

    query = ("""

        INSERT INTO
            diets(name, sugar, fat, protein, small_size, big_size, active)
        VALUES
            (%s, %s, %s, %s, %s, %s, 1);

        """)
    cursor.execute(query, (diet.name, diet.sugar, diet.fat, diet.protein, diet.small_size, diet.big_size))

    last_id = db.insert_id()
    query = ("""

        INSERT INTO
            users_has_diets(users_id, diets_id)
        VALUES
            (%s, %s);

        """)
    cursor.execute(query, (loadUser(diet.username).id, last_id))

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

    query = ("""

        SELECT
            DR.recipes_id
        FROM
            diets_has_recipes AS DR
        WHERE
            DR.diets_id = %s;

        """)
    cursor.execute(query, (dietID,))
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
    query = ("""

        DELETE 
            DR
        FROM
            diets_has_recipes AS DR
        WHERE
            DR.diets_id = %s;

        """)
    cursor.execute(query, (dietID,))

    query = ("""

        DELETE
            DR
        FROM
            users_has_diets AS UD
        WHERE
            UD.diets_id = %s;

        """)
    cursor.execute(query, (dietID,))

    query = ("""

        DELETE 
            D
        FROM
            diets AS D
        WHERE
            D.id = %s;

        """)
    cursor.execute(query, (dietID,))

    db.commit()


def disableDiet(dietID):  # wip
    db = dbConnect()
    cursor = db.cursor()

    query = ("""
        UPDATE
            diets AS D
        SET
            D.active = 0
        WHERE
            D.id = %s;
        """)
    cursor.execute(query, (dietID,))

    db.commit()


def enableDiet(dietID):
    db = dbConnect()
    cursor = db.cursor()

    query = ("""
        UPDATE
            diets AS D
        SET
            D.active = 1
        WHERE
            D.id = %s;
        """)
    cursor.execute(query, (dietID,))

    db.commit()


def editDiet(diet):                         # wip - proč je tam if:else?
    """[summary]

    [description]

    Arguments:
        diet {[type]} -- [description]
    """
    db = dbConnect()
    cursor = db.cursor()

    if hasattr(diet, 'protein'):
        query = ("""

            UPDATE
                diets AS D
            SET
                D.name = %s, D.protein = %s, D.fat = %s, D.sugar = %s, D.small_size = %s, D.big_size = %s
            WHERE
                D.id = %s;

            """)
        cursor.execute(query, (diet.name, diet.protein, diet.fat, diet.sugar, diet.small, diet.big, diet.id))
    else:
        query = ("""

            UPDATE
                diets AS D
            SET
                D.name = %s, D.small_size = %s, D.big_size = %s
            WHERE
                D.id = %s;

        """)
        cursor.execute(query, (diet.name, diet.small, diet.big, diet.id))
    db.commit()


def loadUserDiets(username, active=1):
    """Load diets for user ordered by name

    [description]

    Arguments:
        username {str} -- [description]

    Returns:
        array -- array of Diets
    """
    db = dbConnect()
    cursor = db.cursor()
    query = ("""
        SELECT
            D.id,
            D.name,
            D.sugar,
            D.fat,
            D.protein,
            D.small_size,
            D.big_size,
            D.active
        FROM
            users AS U
            JOIN users_has_diets AS UD ON UD.users_id = U.id
            JOIN diets AS D ON D.id = UD.diets_id AND IF(%s=1, D.active = 1, 1=1)
        WHERE
            U.username = %s
        ORDER BY
            D.active DESC,
            D.name ASC
            ;
        """)

    cursor.execute(query, (active, username))
    response = cursor.fetchall()

    # convert to array of objects
    diets = []
    for i in range(len(response)):
        temp_diet = Diet(response[i][0], response[i][1], response[i][2], response[i][3], response[i][4], response[i][5], response[i][6], response[i][7], username)
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

    query = ("""

        SELECT
            I.id,
            I.name,
            I.calorie,
            I.sugar,
            I.fat,
            I.protein,
            I.author
        FROM
            ingredients AS I
        WHERE
            I.author = %s;

        """)
    cursor.execute(query, (username,))
    response = cursor.fetchall()

    temp_ingredients = []
    for ingredient in response:
        temp_ingredient = Ingredient(ingredient[0], ingredient[1], ingredient[2], ingredient[3], ingredient[4], ingredient[5], ingredient[6])
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

    query = ("""

        SELECT
            I.id,
            I.name,
            I.calorie,
            I.sugar,
            I.fat,
            I.protein,
            I.author
        FROM
            ingredients AS I
        WHERE
            I.id = %s;

        """)
    cursor.execute(query, (int(ingredientID),))
    response = cursor.fetchone()
    if response is None:
        return None

    ingredient = Ingredient(response[0], response[1], response[2], response[3], response[4], response[5], response[6])

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

    query = ("""

        SELECT
            RI.ingredients_id
        FROM
            recipes_has_ingredients AS RI
        WHERE
            RI.recipes_id = %s;

        """)
    cursor.execute(query, (int(recipeID),))
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

    query = ("""

        SELECT
            amount
        FROM
            recipes_has_ingredients AS RI
        WHERE
            RI.ingredients_id = %s
            AND
            RI.recipes_id = %s

        """)
    cursor.execute(query, (ingredientID, recipeID))
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

    query = ("""

        INSERT INTO
            ingredients(name, calorie, sugar, fat, protein, author)
        VALUES
            (%s, %s, %s, %s, %s, %s);

        """)
    cursor.execute(query, (ingredient.name, ingredient.calorie, ingredient.sugar, ingredient.fat, ingredient.protein, username))
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

    query = ("""

        SELECT
            RI.recipes_id
        FROM
            recipes_has_ingredients AS RI
        WHERE
            RI.ingredients_id = %s;

        """)
    cursor.execute(query, (ingredientID,))
    response = cursor.fetchall()
    if len(response) == 0:
        return True
    else:
        return False


def deleteIngredient(ingredientID):
    """[summary]

    WIP: doesnt delete recipes - leaves destroyed recipes

    Arguments:
        ingredientID {[type]} -- [description]
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("""

        DELETE
            RI
        FROM
            recipes_has_ingredients AS RI
        WHERE
            RI.ingredients_id = %s

        """)
    cursor.execute(query, (ingredientID,))

    query = ("""
        DELETE
            I
        FROM
            ingredients AS I
        WHERE
            I.id = %s;

        """)
    cursor.execute(query, (ingredientID,))

    db.commit()


def editIngredient(ingredient):         # wip - why?
    """[summary]

    [description]

    Arguments:
        ingredient {[type]} -- [description]
    """
    db = dbConnect()
    cursor = db.cursor()

    if hasattr(ingredient, 'protein'):
        query = ("""

            UPDATE
                ingredients AS I
            SET
                I.name = %s, I.calorie = %s, I.protein = %s, I.fat = %s, I.sugar = %s
            WHERE
                I.id = %s;

            """)
        cursor.execute(query, (ingredient.name, ingredient.calorie, ingredient.protein, ingredient.fat, ingredient.sugar, ingredient.id))
    else:
        query = ("""

            UPDATE
                ingredients AS I
            SET
                I.name = %s, I.calorie = %s
            WHERE
                I.id = %s;

            """)
        cursor.execute(query, (ingredient.name, ingredient.calorie, ingredient.id))
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

    query = ("""

        INSERT INTO
            users(username, pwdhash, firstName, lastName)
        VALUES
            (%s, %s, %s, %s);

        """)
    cursor.execute(query, (username, password_hash, firstname, lastname))

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

    query = ("""

        SELECT
            id, username, pwdhash, firstname, lastname
        FROM
            users
        WHERE
            username = %s;

        """)
    cursor.execute(query, (username,))

    response = cursor.fetchone()

    if response is None:
        return None
    else:
        return User(response[0], response[1], response[2], response[3], response[4])


def loadUserById(userID):
    """[summary]

    [description]

    Arguments:
        username {str} -- [description]

    Returns:
        User or None -- [description]
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("""

        SELECT
            id, username, pwdhash, firstname, lastname
        FROM
            users
        WHERE
            id = %s;

        """)
    cursor.execute(query, (userID,))

    response = cursor.fetchone()

    if response is None:
        return None
    else:
        return User(response[0], response[1], response[2], response[3], response[4])


def editUser(user):
    """[summary]
    """
    db = dbConnect()
    cursor = db.cursor()
    
    query = ("""

        UPDATE
            users
        SET
            firstName = %s, lastName = %s
        WHERE
            id = %s;

        """)
    cursor.execute(query, (user.firstname, user.lastname, user.id))

    db.commit()

    if cursor.rowcount == 1:
        return True
    else:
        return False


def changeUserPassword(user):
    """[summary]
    """
    db = dbConnect()
    cursor = db.cursor()

    query = ("""

        UPDATE
            users
        SET
            pwdhash = %s
        WHERE
            id = %s;

        """)
    cursor.execute(query, (user.password, user.id))

    db.commit()

    if cursor.rowcount == 1:
        return True
    else:
        return False
