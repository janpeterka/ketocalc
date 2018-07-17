# coding: utf-8
from sqlalchemy import CHAR, Column, Enum, Float, ForeignKey, INTEGER, String, Table, text
# from sqlalchemy import and_
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

import db_data as dbd


engine = create_engine(dbd.sqlalchemy_db_string, echo=False)  # change to False
Session = sessionmaker(bind=engine)

Base = declarative_base()
metadata = Base.metadata

s = Session()


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
    active = Column(TINYINT(1))

    recipes = relationship('Recipe', secondary='diets_has_recipes')
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

    def deleteCheck(self):
        if len(self.recipes) == 0:
            return True
        else:
            return False

    def remove(self):
        s.delete(self)
        s.commit()

    @property
    def json(self):
        return {'id': self.id, 'name': self.name, 'sugar': self.sugar, 'fat': self.fat,
                'protein': self.protein, 'small_size': self.small_size, 'big_size': self.big_size}


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
                           viewonly=True)

    def load(ingredient_id):
        ingredient = s.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        return ingredient

    def loadAllByUsername(username):
        ingredients = s.query(Ingredient).filter(Ingredient.author == username).all()
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

    def deleteCheck(self):
        if len(self.recipes) == 0:
            return True
        else:
            return False

    def remove(self):
        s.delete(self)
        s.commit()

    @property
    def json(self):
        return {'id': self.id, 'name': self.name, 'calorie': self.calorie, 'sugar': self.sugar, 'fat': self.fat, 'protein': self.protein}


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER, primary_key=True, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    pwdhash = Column(CHAR(64), nullable=False)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)

    diets = relationship('Diet', secondary='users_has_diets')

    def load(user_id):
        if type(user_id) is int:
            user = s.query(User).filter(User.id == user_id).first()
        else:
            user = s.query(User).filter(User.username == user_id).first()
        return user

    def save(self):
        s.add(self)
        s.flush()
        s.commit()
        return self.id

    def edit(self):
        s.commit()
        return True

    def remove(self):
        s.delete()
        s.commit()

    @property
    def recipes(self):
        recipes = []
        for diet in self.diets:
            recipes.extend(diet.recipes)
        return recipes


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum('small', 'big'), nullable=False)

    diet = relationship('Diet', secondary='diets_has_recipes', uselist=False)
    ingredients = relationship("Ingredient",
                               primaryjoin="and_(Recipe.id == remote(RecipesHasIngredient.recipes_id), foreign(Ingredient.id) == RecipesHasIngredient.ingredients_id)",
                               viewonly=True)

    def load(recipe_id):
        recipe = s.query(Recipe).filter(Recipe.id == recipe_id).first()
        if recipe is None:
            return None

        temp_ingredients = s.query(RecipesHasIngredient).filter(RecipesHasIngredient.recipes_id == recipe_id)

        ingredientIDs = []
        for i in temp_ingredients.all():
            ingredientIDs.append(i.ingredients_id)

        return recipe

    def save(self, ingredients):
        s.add(self)
        s.flush()

        for i in ingredients:
            i.recipes_id = self.id
            s.add(i)
            s.flush()

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
        return self.diet.author.username
