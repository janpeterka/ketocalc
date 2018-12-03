# coding: utf-8
from sqlalchemy import CHAR, Column, Enum, Float, ForeignKey, INTEGER, String, Table, text
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

import math
import os

import bcrypt
import hashlib

import unidecode


engine = create_engine(os.environ.get('DB_STRING'), echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()
metadata = Base.metadata

global s

s = None


# not cool (#wip)
def startSession():
    global s
    s = Session()


def endSession():
    s.close()


if s is None:
    startSession()


t_diets_has_recipes = Table(
    'diets_has_recipes', metadata,
    Column('diet_id', ForeignKey('diets.id'), primary_key=True, nullable=False, index=True),
    Column('recipes_id', ForeignKey('recipes.id'), primary_key=True, nullable=False, index=True)
)


t_users_has_diets = Table(
    'users_has_diets', metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True, nullable=False, index=True),
    Column('diet_id', ForeignKey('diets.id'), primary_key=True, nullable=False, index=True)
)


class RecipesHasIngredient(Base):
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

    recipes_id = Column(ForeignKey('recipes.id'), primary_key=True, nullable=False, index=True)
    ingredients_id = Column(ForeignKey('ingredients.id'), primary_key=True, nullable=False, index=True)
    amount = Column(Float, nullable=False)

    ingredients = relationship('Ingredient')
    recipes = relationship('Recipe')


class Diet(Base):
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

    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=False)
    sugar = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    small_size = Column(Float, nullable=False)
    big_size = Column(Float, nullable=False)
    active = Column(TINYINT(1), nullable=False, server_default=text("'1'"))

    recipes = relationship('Recipe', secondary='diets_has_recipes', order_by='Recipe.name')
    author = relationship('User', secondary='users_has_diets', uselist=False)

    @staticmethod
    def load(diet_id):
        """Load Diet object by ID

        Arguments:
            diet_id {int} -- object ID in database

        Returns:
            Diet -- SQLAlchemy Diet object
        """
        diet = s.query(Diet).filter(Diet.id == diet_id).first()
        return diet

    def save(self):
        """Save new Diet object

        Returns:
            int -- id of saved object
        """
        s.add(self)
        s.commit()
        return self.id

    def edit(self):
        """Saves Diet object changes
        """
        s.commit()

    def remove(self):
        """Deletes Diet object
        """
        s.delete(self)
        s.commit()

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


class Ingredient(Base):
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

    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=False)
    calorie = Column(Float, nullable=False, server_default=text("'0'"))
    sugar = Column(Float, nullable=False, server_default=text("'0'"))
    fat = Column(Float, nullable=False, server_default=text("'0'"))
    protein = Column(Float, nullable=False, server_default=text("'0'"))
    author = Column(String(255), nullable=False)

    recipes = relationship('Recipe',
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
        ingredient = s.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
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
        ingredients = s.query(Ingredient).filter(Ingredient.author == username).all()
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
        rhi = s.query(RecipesHasIngredient).filter(RecipesHasIngredient.recipes_id == recipe_id).filter(RecipesHasIngredient.ingredients_id == self.id).first()
        return rhi.amount

    def save(self):
        """Saves new Ingredient object

        Returns:
            int -- database ID of new object
        """

        s.add(self)
        s.commit()
        return self.id

    def edit(self):
        """Saves Ingredient object changes
        """
        s.commit()

    def remove(self):
        """Deletes Ingredient object

        """
        s.delete(self)
        s.commit()

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
            bool -- 
        """
        if len(self.recipes) == 0:
            return False
        else:
            return True


class User(Base):
    """User class


    Extends:
        Base

    Variables:
        __tablename__ {str} -- [description]
        id {int} -- [description]
        username {string} -- [description]
        pwdhash {string} -- password hash (sha256 / bcrypt)
        firstName {string} -- [description]
        lastName {string} -- [description]
        password_version {string} -- password version (sha256 / bcrypt)
        diets {relationship} -- [description]
    """
    __tablename__ = 'users'

    id = Column(INTEGER, primary_key=True, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    pwdhash = Column(CHAR(64), nullable=False)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)
    password_version = Column(String(45), nullable=True)

    diets = relationship('Diet', secondary='users_has_diets', order_by='desc(Diet.active)')

    @staticmethod
    def load(user_id):
        """Load User

        Load User by ID or username

        Arguments:
            user_id {int / string} -- database ID or username

        Returns:
            User -- SQLAlchemy object
        """
        if type(user_id) is int:
            user = s.query(User).filter(User.id == user_id).first()
        else:
            user = s.query(User).filter(User.username == user_id).first()
        return user

    def save(self):
        """Saves user

        Returns:
            int -- new User db id
        """
        s.add(self)
        s.commit()
        return self.id

    def edit(self):
        """Edit user

        Returns:
            None --
        """
        s.commit()
        return None

    def remove(self):
        """Remove User

        Returns:
            None --
        """
        s.delete()
        s.commit()
        return None

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
                s.commit()
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


class Recipe(Base):
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

    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum('small', 'big'), nullable=False)

    diet = relationship('Diet', secondary='diets_has_recipes', uselist=False)
    ingredients = relationship("Ingredient",
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
        recipe = s.query(Recipe).filter(Recipe.id == recipe_id).first()
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
            list -- of Recipes
        """

        recipes = s.query(Recipe).filter(Recipe.ingredients.any(Ingredient.id == ingredient_id)).all()
        return recipes

    def save(self, ingredients):
        """Save recipe

        [description]

        Arguments:
            ingredients {list} -- list of Ingredients

        Returns:
            int -- Recipe id
        """
        s.add(self)
        s.flush()

        for i in ingredients:
            i.recipes_id = self.id
            s.add(i)

        s.commit()
        return self.id

    def remove(self):
        """Deletes Recipe

        Returns:
            None
        """
        # wip - to improve w/ orphan cascade
        ingredients = s.query(RecipesHasIngredient).filter(RecipesHasIngredient.recipes_id == self.id)
        for i in ingredients:
            s.delete(i)

        s.delete(self)
        s.commit()
        return None

    def edit(self):
        """Edit Recipe

        Returns:
            None
        """
        s.commit()
        return None

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
