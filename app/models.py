# coding: utf-8

from app import db
from app.auth import login

import math
import datetime

import bcrypt
import hashlib

import unidecode

from flask_login import UserMixin

t_diets_has_recipes = db.Table(
    'diets_has_recipes',
    db.Column('diet_id', db.ForeignKey('diets.id'), primary_key=True, nullable=False, index=True),
    db.Column('recipes_id', db.ForeignKey('recipes.id'), primary_key=True, nullable=False, index=True)
)


t_users_has_diets = db.Table(
    'users_has_diets',
    db.Column('user_id', db.ForeignKey('users.id'), primary_key=True, nullable=False, index=True),
    db.Column('diet_id', db.ForeignKey('diets.id'), primary_key=True, nullable=False, index=True)
)


# Custom methods for all my classes
class BaseMixin(object):

    def edit(self, **kw):
        """Edits object

        Saves object changes
        """
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("Edit error: {}".format(e))
            return False

    def save(self, **kw):
        """Saves new object

        Returns:
            int -- database ID of new object
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            print("Save error: {}".format(e))
            return False

    def remove(self, **kw):
        """Deletes object
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print("Remove error: {}".format(e))
            return False

    def expire(self, **kw):
        """Dumps database changes

        [description]
        """

        try:
            db.session.expire(self)
            return True
        except Exception as e:
            print("Expire error: {}".format(e))
            return False

    @classmethod
    def refresh(self, **kw):
        """Refreshes object

        Expires changes and loads object

        Arguments:
            **kw {[type]} -- [description]

        Returns:
            bool -- [description]
        """
        # obj = cls(**kw)

        try:
            db.session.refresh(self)
            return True
        except Exception as e:
            print("Refresh error: {}".format(e))
            return False


class RecipesHasIngredient(db.Model):
    """Recipe-Ingredient connection class

    Extends:
        Base

    Variables:
        __tablename__ {str} -- [description]
        recipes_id {int} -- [description]
        ingredients_id {int} -- [description]
        amount {int} -- [description]
        ingredients {relationship} -- [description]
        recipes {relationship} -- [description]
    """
    __tablename__ = 'recipes_has_ingredients'

    recipes_id = db.Column(db.ForeignKey('recipes.id'), primary_key=True, nullable=False, index=True)
    ingredients_id = db.Column(db.ForeignKey('ingredients.id'), primary_key=True, nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)

    ingredients = db.relationship('Ingredient')
    recipes = db.relationship('Recipe')


class Diet(db.Model, BaseMixin):
    """Diet object

    Extends:
        Base

    Variables:
        __tablename__ {str} -- [description]
        id {int} -- [description]
        name {string} -- [description]
        sugar {int} -- sugar amount
        fat {int} -- fat amount
        protein {int} -- protein amount
        small_size {int} -- small size in %
        big_size {int} -- big size in %
        active {int} -- int 0 / 1 - works as boolean
        recipes {relationship} -- [description]
        author {relationship} -- [description]
    """
    __tablename__ = 'diets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    calorie = db.Column(db.Float, nullable=False)
    sugar = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    small_size = db.Column(db.Float, nullable=False)
    big_size = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)

    recipes = db.relationship('Recipe', secondary='diets_has_recipes', order_by='Recipe.name')
    author = db.relationship('User', secondary='users_has_diets', uselist=False)

    @staticmethod
    def load(diet_id):
        """Load Diet object by ID

        Arguments:
            diet_id {int} -- object ID in database

        Returns:
            Diet -- SQLAlchemy Diet object
        """
        diet = db.session.query(Diet).filter(Diet.id == diet_id).first()
        return diet

    @property
    def json(self):
        """returns Diet object as JSON

        Returns:
            json -- Diet data
        """
        return {'id': self.id, 'name': self.name, 'sugar': self.sugar, 'fat': self.fat,
                'protein': self.protein, 'small_size': self.small_size, 'big_size': self.big_size}

    @property
    def used(self):
        """Is Diet used in Recipe?

        Returns:
            bool --
        """
        if len(self.recipes) == 0:
            return False
        else:
            return True


class Ingredient(db.Model, BaseMixin):
    """Ingredient class

    [description]

    Extends:
        Base

    Variables:
        __tablename__ {str} -- [description]
        id {int} -- [description]
        name {string} -- [description]
        calorie {int} -- [description]
        sugar {int} -- [description]
        fat {int} -- [description]
        protein {int} -- [description]
        author {string} -- [description]
        recipes {relationship} -- [description]
    """
    __tablename__ = 'ingredients'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    calorie = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    sugar = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    fat = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    protein = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    author = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)

    recipes = db.relationship('Recipe',
                              primaryjoin="and_(Ingredient.id == remote(RecipesHasIngredient.ingredients_id), foreign(Recipe.id) == RecipesHasIngredient.recipes_id)",
                              viewonly=True, order_by='Recipe.name')

    @staticmethod
    def load(ingredient_id):
        """Load Ingredient object by ID

        SQLAlchemy class

        Arguments:
            ingredient_id {int} -- object ID in database

        Returns:
            Ingredient -- SQLAlchemy Ingredient object
        """
        ingredient = db.session.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        return ingredient

    @staticmethod
    def loadAllByAuthor(username, ordered=True):
        """Load Ingredient objects by author

        used for loading all ingredients for user

        Arguments:
            username {string} -- [description]

        Keyword Arguments:
            ordered {bool} -- if ingredients ordered alphabetically (default: {True})

        Returns:
            list -- list of Ingredient objects
        """
        ingredients = db.session.query(Ingredient).filter(Ingredient.author == username).all()
        if ordered:
            ingredients.sort(key=lambda x: unidecode.unidecode(x.name.lower()), reverse=False)
        return ingredients

    def loadAmount(self, recipe_id):
        """Load amount of Ingredient in Recipe

        Arguments:
            recipe_id {int} -- Recipe database ID

        Returns:
            int -- amount
        """
        rhi = db.session.query(RecipesHasIngredient).filter(RecipesHasIngredient.recipes_id == recipe_id).filter(RecipesHasIngredient.ingredients_id == self.id).first()
        return rhi.amount

    @property
    def json(self):
        """returns Diet object as JSON

        Returns:
            json -- Diet data
        """
        return {'id': self.id, 'name': self.name, 'calorie': self.calorie, 'sugar': self.sugar, 'fat': self.fat, 'protein': self.protein}

    @property
    def used(self):
        """Is Ingredient used in Recipe?

        Returns:
            bool -- Ingredient used in Recipe
        """
        if len(self.recipes) == 0:
            return False
        else:
            return True


class User(db.Model, UserMixin, BaseMixin):
    """User class


    Extends:
        Base

    Variables:
        __tablename__ {str} -- DB table name
        id {int} -- user id
        username {string} -- username (email)
        pwdhash {string} -- password hash (sha256 / bcrypt)
        firstName {string} -- first name
        lastName {string} -- last name
        password_version {string} -- password version (sha256 / bcrypt)
        diets {relationship} -- diets of user
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    google_id = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    pwdhash = db.Column(db.CHAR(64), nullable=True)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    password_version = db.Column(db.String(45), nullable=True)

    created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    # last_updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)

    last_logged_in = db.Column(db.DateTime, nullable=True)
    login_count = db.Column(db.Integer, nullable=True, default=0)

    diets = db.relationship('Diet', secondary='users_has_diets', order_by='desc(Diet.active)')

    @staticmethod
    def load(user_id, load_type="id"):
        """Load User

        Load User by ID or username

        Arguments:
            user_id {int / string} -- database ID or username

        Returns:
            User -- SQLAlchemy object
        """
        if load_type == "id":
            user = db.session.query(User).filter(User.id == user_id).first()
        elif load_type == "username":
            user = db.session.query(User).filter(User.username == user_id).first()
        elif load_type == "google_id":
            user = db.session.query(User).filter(User.google_id == user_id).first()
        else:
            return None

        return user

    @login.user_loader
    def load_user(user_id):
        return db.session.query(User).filter(User.id == user_id).first()

    def getPassword(self, password):
        """Creates hash from password

        Uses bcrypt hash function

        Arguments:
            password {string} -- plaintext password

        Returns:
            string -- hashed password
        """
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def checkLogin(self, password):
        """Verifies login data

        Verifies login data and changes hash function if necessary

        Arguments:
            password {string} -- plaintext password

        Returns:
            bool -- verification
        """
        db_password_hash = self.pwdhash.encode('utf-8')
        if self.password_version == 'SHA256':

            if hashlib.sha256(password).hexdigest() == self.pwdhash:
                # changing from sha256 to bcrypt
                self.pwdhash = self.getPassword(password)
                self.password_version = 'bcrypt'
                self.edit()
                return True
            else:
                return False
        else:
            if bcrypt.checkpw(password, db_password_hash):
                return True
            else:
                return False

    @property
    def recipes(self, ordered=True):
        """User's Recipes

        Keyword Arguments:
            ordered {bool} -- is ordered alphabetically? (default: {True})

        Returns:
            list -- list of Recipe objects
        """
        recipes = []
        for diet in self.diets:
            recipes.extend(diet.recipes)
        if ordered:
            recipes.sort(key=lambda x: unidecode.unidecode(x.name.lower()), reverse=False)
        return recipes

    @property
    def activeDiets(self):
        """User's active Diets

        Returns:
            list -- list of active diets
        """
        active_diets = []
        for diet in self.diets:
            if diet.active == 1:
                active_diets.append(diet)
        return active_diets


class Recipe(db.Model, BaseMixin):
    """[summary]

    [description]

    Extends:
        Base

    Variables:
        __tablename__ {str} -- [description]
        id {int} -- [description]
        name {string} -- [description]
        type {string} -- [description]
        diet {relationship} -- [description]
        ingredients {relationship} -- [description]
    """
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum('small', 'big'), nullable=False)

    created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)

    view_count = db.Column(db.Integer, nullable=True, default=0)

    diet = db.relationship('Diet', secondary='diets_has_recipes', uselist=False)
    ingredients = db.relationship("Ingredient",
                                  primaryjoin="and_(Recipe.id == remote(RecipesHasIngredient.recipes_id), foreign(Ingredient.id) == RecipesHasIngredient.ingredients_id)",
                                  viewonly=True, order_by='Ingredient.name')

    @staticmethod
    def load(recipe_id):
        """Load Recipe by id

        Arguments:
            recipe_id {int} -- recipe id

        Returns:
            Recipe -- Recipe object
        """
        recipe = db.session.query(Recipe).filter(Recipe.id == recipe_id).first()

        if recipe.type == "big":
            coef = float(recipe.diet.big_size / 100)
        else:
            coef = float(recipe.diet.small_size / 100)

        for ingredient in recipe.ingredients:
            ingredient.amount = float(math.floor(ingredient.loadAmount(recipe.id) * coef * 100000)) / 100000

        return recipe

    def loadRecipeForShow(self):
        """Load Recipe for print

        Returns:
            json -- recipe, totals
        """
        if self.type == "big":
            coef = float(self.diet.big_size / 100)
        else:
            coef = float(self.diet.small_size / 100)

        for ingredient in self.ingredients:
            ingredient.amount = float(math.floor(ingredient.loadAmount(self.id) * coef * 100000)) / 100000

        totals = type('', (), {})()
        totals.calorie = 0
        totals.protein = 0
        totals.fat = 0
        totals.sugar = 0
        totals.amount = 0

        for i in self.ingredients:
            totals.calorie += i.amount * i.calorie
            totals.protein += i.amount * i.protein
            totals.fat += i.amount * i.fat
            totals.sugar += i.amount * i.sugar
            totals.amount += i.amount

        totals.calorie = math.floor(totals.calorie) / 100
        totals.protein = math.floor(totals.protein) / 100
        totals.fat = math.floor(totals.fat) / 100
        totals.sugar = math.floor(totals.sugar) / 100
        totals.amount = math.floor(totals.amount)

        totals.ratio = math.floor((totals.fat / (totals.protein + totals.sugar)) * 100) / 100
        return {'recipe': self, 'totals': totals}

    @staticmethod
    def loadByIngredient(ingredient_id):
        """Load all recipes by ingredient

        Arguments:
            ingredient_id {int} -- Ingredient id

        Returns:
            list -- list of Recipes
        """

        recipes = db.session.query(Recipe).filter(Recipe.ingredients.any(Ingredient.id == ingredient_id)).all()
        return recipes

    def save(self, ingredients):
        """Save recipe

        [description]

        Arguments:
            ingredients {list} -- list of Ingredients

        Returns:
            int -- Recipe id
        """
        db.session.add(self)
        db.session.flush()

        for i in ingredients:
            i.recipes_id = self.id
            db.session.add(i)

        db.session.commit()
        return self.id

    def remove(self):
        """Deletes Recipe

        Returns:
            None
        """
        # wip - to improve w/ orphan cascade
        ingredients = db.session.query(RecipesHasIngredient).filter(RecipesHasIngredient.recipes_id == self.id)
        for i in ingredients:
            db.session.delete(i)

        db.session.delete(self)
        db.session.commit()
        return True

    @property
    def totals(self):
        # if self.type == "big":
            # coef = float(self.diet.big_size / 100)
        # else:
            # coef = float(self.diet.small_size / 100)

        # for ingredient in self.ingredients:
            # ingredient.amount = float(math.floor(ingredient.loadAmount(self.id) * coef * 100000)) / 100000

        totals = type('', (), {})()
        totals.calorie = 0
        totals.protein = 0
        totals.fat = 0
        totals.sugar = 0
        totals.amount = 0

        for i in self.ingredients:
            totals.calorie += i.amount * i.calorie
            totals.protein += i.amount * i.protein
            totals.fat += i.amount * i.fat
            totals.sugar += i.amount * i.sugar
            totals.amount += i.amount

        totals.calorie = math.floor(totals.calorie) / 100
        totals.protein = math.floor(totals.protein) / 100
        totals.fat = math.floor(totals.fat) / 100
        totals.sugar = math.floor(totals.sugar) / 100
        totals.amount = math.floor(totals.amount)

        totals.ratio = math.floor((totals.fat / (totals.protein + totals.sugar)) * 100) / 100
        return totals

    @property
    def json(self):
        """Returns JSON of Recipe

        Returns:
            json
        """
        return {'id': self.id, 'name': self.name, 'size': self.type}

    @property
    def author(self):
        """[summary]

        Returns User who created diet, in which this recipe is

        Returns:
            User -- User object
        """
        return self.diet.author
