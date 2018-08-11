# coding: utf-8
from sqlalchemy import CHAR, Column, Enum, Float, ForeignKey, INTEGER, String, Table, text
# from sqlalchemy import desc
# from sqlalchemy import and_
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

# from .data import db_data as dbd

import math
import os

import bcrypt
import hashlib


engine = create_engine(os.environ.get('DB_STRING'), echo=False)  # change to False
Session = sessionmaker(bind=engine)

Base = declarative_base()
metadata = Base.metadata

global s


# not cool (#wip)
def startSession():
    global s
    s = Session()


def endSession():
    s.close()


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
    __tablename__ = 'recipes_has_ingredients'

    recipes_id = Column(ForeignKey('recipes.id'), primary_key=True, nullable=False, index=True)
    ingredients_id = Column(ForeignKey('ingredients.id'), primary_key=True, nullable=False, index=True)
    amount = Column(Float, nullable=False)

    ingredients = relationship('Ingredient')
    recipes = relationship('Recipe')


class Diet(Base):
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

    def load(diet_id):
        diet = s.query(Diet).filter(Diet.id == diet_id).first()
        return diet

    def save(self):
        s.add(self)
        s.commit()
        return self.id

    def edit(self):
        s.commit()

    def remove(self):
        s.delete(self)
        s.commit()

    @property
    def json(self):
        return {'id': self.id, 'name': self.name, 'sugar': self.sugar, 'fat': self.fat,
                'protein': self.protein, 'small_size': self.small_size, 'big_size': self.big_size}

    @property
    def used(self):
        if len(self.recipes) == 0:
            return False
        else:
            return True


class Ingredient(Base):
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

    def load(ingredient_id):
        ingredient = s.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        return ingredient

    def loadAllByUsername(username, ordered=True):
        ingredients = s.query(Ingredient).filter(Ingredient.author == username).all()
        if ordered:
            ingredients.sort(key=lambda x: x.name, reverse=False)
        return ingredients

    def loadAmount(self, recipe_id):
        rhi = s.query(RecipesHasIngredient).filter(RecipesHasIngredient.recipes_id == recipe_id).filter(RecipesHasIngredient.ingredients_id == self.id).first()
        return rhi.amount

    def save(self):
        s.add(self)
        s.commit()
        return self.id

    def edit(self):
        s.commit()

    def remove(self):
        s.delete(self)
        s.commit()

    @property
    def json(self):
        return {'id': self.id, 'name': self.name, 'calorie': self.calorie, 'sugar': self.sugar, 'fat': self.fat, 'protein': self.protein}

    @property
    def used(self):
        if len(self.recipes) == 0:
            return False
        else:
            return True


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER, primary_key=True, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    pwdhash = Column(CHAR(64), nullable=False)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)
    password_version = Column(String(45), nullable=True)

    diets = relationship('Diet', secondary='users_has_diets', order_by='desc(Diet.active)')

    def load(user_id):
        if type(user_id) is int:
            user = s.query(User).filter(User.id == user_id).first()
        else:
            user = s.query(User).filter(User.username == user_id).first()
        return user

    def save(self):
        s.add(self)
        s.commit()
        return self.id

    def edit(self):
        s.commit()
        return True

    def remove(self):
        s.delete()
        s.commit()

    def getPassword(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def checkLogin(self, password):
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
        recipes = []
        for diet in self.diets:
            recipes.extend(diet.recipes)
        if ordered:
            recipes.sort(key=lambda x: x.name, reverse=False)
        return recipes

    @property
    def activeDiets(self):
        active_diets = []
        for diet in self.diets:
            if diet.active == 1:
                active_diets.append(diet)
        return active_diets


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum('small', 'big'), nullable=False)

    diet = relationship('Diet', secondary='diets_has_recipes', uselist=False)
    ingredients = relationship("Ingredient",
                               primaryjoin="and_(Recipe.id == remote(RecipesHasIngredient.recipes_id), foreign(Ingredient.id) == RecipesHasIngredient.ingredients_id)",
                               viewonly=True, order_by='Ingredient.name')

    def load(recipe_id):
        recipe = s.query(Recipe).filter(Recipe.id == recipe_id).first()
        return recipe

    def loadRecipeForShow(self):
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

    def save(self, ingredients):
        s.add(self)
        s.flush()

        for i in ingredients:
            i.recipes_id = self.id
            s.add(i)

        s.commit()
        return self.id

    def remove(self):
        # wip - to improve w/ orphan cascade
        ingredients = s.query(RecipesHasIngredient).filter(RecipesHasIngredient.recipes_id == self.id)
        for i in ingredients:
            s.delete(i)

        s.delete(self)
        s.commit()

    def edit(self):
        s.commit()

    @property
    def json(self):
        return {'id': self.id, 'name': self.name, 'size': self.type}

    @property
    def author(self):
        return self.diet.author
