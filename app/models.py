# coding: utf-8

import math
import datetime

import bcrypt
import hashlib

import unidecode

from flask import current_app as application

from flask_login import UserMixin

from app import db
from app.auth import login

from sqlalchemy.exc import DatabaseError


t_diets_has_recipes = db.Table(
    "diets_has_recipes",
    db.Column(
        "diet_id",
        db.ForeignKey("diets.id"),
        primary_key=True,
        nullable=False,
        index=True,
    ),
    db.Column(
        "recipes_id",
        db.ForeignKey("recipes.id"),
        primary_key=True,
        nullable=False,
        index=True,
    ),
)


t_users_has_diets = db.Table(
    "users_has_diets",
    db.Column(
        "user_id",
        db.ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
        index=True,
    ),
    db.Column(
        "diet_id",
        db.ForeignKey("diets.id"),
        primary_key=True,
        nullable=False,
        index=True,
    ),
)


# Custom methods for all my classes
class BaseMixin(object):
    def edit(self, **kw):
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error("Edit error: {}".format(e))
            return False

    def save(self, **kw):
        """Saves (new) object
        """
        try:
            db.session.add(self)
            db.session.commit()
            if self.id is not None:
                return True
            else:
                return False
        except DatabaseError as e:
            db.session.rollback()
            application.logger.error("Save error: {}".format(e))
            return False

    def remove(self, **kw):
        """Deletes object
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except DatabaseError as e:
            db.session.rollback()
            application.logger.error("Remove error: {}".format(e))
            return False

    def expire(self, **kw):
        """Dumps database changes
        """

        try:
            db.session.expire(self)
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error("Expire error: {}".format(e))
            return False

    @classmethod
    def refresh(self, **kw):
        try:
            db.session.refresh(self)
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error("Refresh error: {}".format(e))
            return False

    @property
    def json(self):
        attributes = []
        for attr in self.__dict__.keys():
            if not attr.startswith("_"):
                attributes.append(attr)

        return {attr: getattr(self, attr) for attr in attributes}


class Log(db.Model, BaseMixin):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    logger = db.Column(db.String(255))
    level = db.Column(db.String(255), index=True)
    msg = db.Column(db.Text)
    url = db.Column(db.String(255))
    remote_addr = db.Column(db.String(255))
    module = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    @staticmethod
    def load_by_level(level):
        logs = db.session.query(Log).filter(Log.level == level)
        return logs

    @staticmethod
    def load_all():
        logs = db.session.query(Log).order_by(Log.timestamp.desc())
        return logs

    @staticmethod
    def load_since(date="2019-01-01"):
        logs = (
            db.session.query(Log)
            .filter(Log.timestamp > date)
            .order_by(Log.timestamp.desc())
        )
        return logs


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

    __tablename__ = "recipes_has_ingredients"

    recipes_id = db.Column(
        db.ForeignKey("recipes.id"), primary_key=True, nullable=False, index=True
    )
    ingredients_id = db.Column(
        db.ForeignKey("ingredients.id"), primary_key=True, nullable=False, index=True
    )
    amount = db.Column(db.Float, nullable=False)

    ingredients = db.relationship("Ingredient")
    recipes = db.relationship("Recipe")


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

    __tablename__ = "diets"

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

    recipes = db.relationship(
        "Recipe", secondary="diets_has_recipes", order_by="Recipe.name"
    )
    author = db.relationship("User", secondary="users_has_diets", uselist=False)

    @staticmethod
    def load(diet_id):
        diet = db.session.query(Diet).filter(Diet.id == diet_id).first()
        return diet

    @staticmethod
    def load_by_name(diet_name):
        diet = db.session.query(Diet).filter(Diet.name == diet_name).first()
        return diet

    @property
    def is_used(self):
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

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    calorie = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    sugar = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    fat = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    protein = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    author = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)

    recipes = db.relationship(
        "Recipe",
        primaryjoin="and_(Ingredient.id == remote(RecipesHasIngredient.ingredients_id), foreign(Recipe.id) == RecipesHasIngredient.recipes_id)",
        viewonly=True,
        order_by="Recipe.name",
    )

    @staticmethod
    def load(ingredient_id):
        ingredient = (
            db.session.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        )
        return ingredient

    @staticmethod
    def load_by_name(ingredient_name):
        ingredient = (
            db.session.query(Ingredient)
            .filter(Ingredient.name == ingredient_name)
            .first()
        )
        return ingredient

    @staticmethod
    def load_all_by_author(username, ordered=True):
        """Load Ingredient objects by author

        used for loading all ingredients for user

        Arguments:
            username {string} -- [description]

        Keyword Arguments:
            ordered {bool} -- if ingredients ordered alphabetically (default: {True})

        Returns:
            list -- list of Ingredient objects
        """
        ingredients = (
            db.session.query(Ingredient).filter(Ingredient.author == username).all()
        )
        if ordered is True:
            ingredients.sort(
                key=lambda x: unidecode.unidecode(x.name.lower()), reverse=False
            )
        return ingredients

    def load_amount_by_recipe(self, recipe_id):
        """Load amount of Ingredient in Recipe

        Arguments:
            recipe_id {int} -- Recipe database ID

        Returns:
            int -- amount
        """
        rhi = (
            db.session.query(RecipesHasIngredient)
            .filter(RecipesHasIngredient.recipes_id == recipe_id)
            .filter(RecipesHasIngredient.ingredients_id == self.id)
            .first()
        )
        return rhi.amount

    @property
    def is_used(self):
        if len(self.recipes) == 0:
            return False
        else:
            return True

    def set_fixed(self, value=True, amount=0):
        self.fixed = value
        self.amount = amount
        return self

    def set_main(self, value=True):
        self.main = value
        return self


class User(db.Model, UserMixin, BaseMixin):
    """User class


    Extends:
        Base

    Variables:
        __tablename__ {str} -- DB table name
        id {int} -- user id
        username {string} -- username (email)
        pwdhash {string} -- password hash (sha256 / bcrypt)
        first_name {string} -- first name
        last_name {string} -- last name
        password_version {string} -- password version (sha256 / bcrypt)
        diets {relationship} -- diets of user
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    google_id = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    pwdhash = db.Column(db.CHAR(64), nullable=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    password_version = db.Column(db.String(45), nullable=True)

    created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    # last_updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)

    last_logged_in = db.Column(db.DateTime, nullable=True)
    login_count = db.Column(db.Integer, nullable=True, default=0)

    diets = db.relationship(
        "Diet", secondary="users_has_diets", order_by="desc(Diet.active)"
    )

    @staticmethod
    @login.user_loader
    def load(user_identifier, load_type="id"):
        """[summary]

        [description]

        Decorators:
            login.user_loader

        Arguments:
            user_identifier {[type]} -- [description]

        Keyword Arguments:
            load_type {str} -- [description] (default: {"id"})

        Returns:
            [type] -- [description]
        """
        if load_type == "id":
            user = db.session.query(User).filter(User.id == user_identifier).first()
        elif load_type == "username":
            user = (
                db.session.query(User).filter(User.username == user_identifier).first()
            )
        elif load_type == "google_id":
            user = (
                db.session.query(User).filter(User.google_id == user_identifier).first()
            )
        else:
            return None

        return user

    def set_password_hash(self, password):
        self.pwdhash = bcrypt.hashpw(password, bcrypt.gensalt())
        return self

    def check_login(self, password):
        """Verifies login data

        Verifies login data and changes hash function if necessary

        Arguments:
            password {string} -- plaintext password

        Returns:
            bool -- verification
        """
        db_password_hash = self.pwdhash.encode("utf-8")
        if self.password_version == "SHA256":
            if hashlib.sha256(password).hexdigest() == self.pwdhash:
                # changing from sha256 to bcrypt
                self.set_password_hash(password)
                self.password_version = "bcrypt"
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
        recipes = []
        for diet in self.diets:
            recipes.extend(diet.recipes)
        if ordered is True:
            recipes.sort(
                key=lambda x: unidecode.unidecode(x.name.lower()), reverse=False
            )
        return recipes

    @property
    def active_diets(self):
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

    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum("small", "big"), nullable=False)

    created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)

    view_count = db.Column(db.Integer, nullable=True, default=0)

    diet = db.relationship("Diet", secondary="diets_has_recipes", uselist=False)
    ingredients = db.relationship(
        "Ingredient",
        primaryjoin="and_(Recipe.id == remote(RecipesHasIngredient.recipes_id), foreign(Ingredient.id) == RecipesHasIngredient.ingredients_id)",
        viewonly=True,
        order_by="Ingredient.name",
    )

    @staticmethod
    def load(recipe_id):
        recipe = db.session.query(Recipe).filter(Recipe.id == recipe_id).first()

        if recipe.type == "big":
            coef = float(recipe.diet.big_size / 100)
        else:
            coef = float(recipe.diet.small_size / 100)

        for ingredient in recipe.ingredients:
            ingredient.amount = (
                float(
                    math.floor(
                        ingredient.load_amount_by_recipe(recipe.id) * coef * 100000
                    )
                )
                / 100000
            )

        return recipe

    def load_recipe_for_show(self):
        """Load Recipe for print

        Returns:
            json -- recipe, totals
        """
        if self.type == "big":
            coef = float(self.diet.big_size / 100)
        else:
            coef = float(self.diet.small_size / 100)

        for ingredient in self.ingredients:
            ingredient.amount = (
                float(
                    math.floor(
                        ingredient.load_amount_by_recipe(self.id) * coef * 100000
                    )
                )
                / 100000
            )

        totals = type("", (), {})()
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

        totals.ratio = (
            math.floor((totals.fat / (totals.protein + totals.sugar)) * 100) / 100
        )
        return {"recipe": self, "totals": totals}

    @staticmethod
    def load_by_ingredient(ingredient_id):
        recipes = (
            db.session.query(Recipe)
            .filter(Recipe.ingredients.any(Ingredient.id == ingredient_id))
            .all()
        )
        return recipes

    def save(self, ingredients):
        db.session.add(self)
        db.session.flush()

        for i in ingredients:
            i.recipes_id = self.id
            db.session.add(i)

        db.session.commit()
        return self.id

    def remove(self):
        # TODO - to improve w/ orphan cascade
        ingredients = db.session.query(RecipesHasIngredient).filter(
            RecipesHasIngredient.recipes_id == self.id
        )
        for i in ingredients:
            db.session.delete(i)

        db.session.delete(self)
        db.session.commit()
        return True

    @property
    def totals(self):

        totals = type("", (), {})()
        totals.calorie = 0
        totals.protein = 0
        totals.fat = 0
        totals.sugar = 0
        totals.amount = 0

        if self.type == "big":
            coef = float(self.diet.big_size / 100)
        else:
            coef = float(self.diet.small_size / 100)

        for ingredient in self.ingredients:
            ingredient.amount = (
                float(
                    math.floor(
                        ingredient.load_amount_by_recipe(self.id) * coef * 100000
                    )
                )
                / 100000
            )
            totals.calorie += ingredient.amount * ingredient.calorie
            totals.protein += ingredient.amount * ingredient.protein
            totals.fat += ingredient.amount * ingredient.fat
            totals.sugar += ingredient.amount * ingredient.sugar
            totals.amount += ingredient.amount

        totals.calorie = math.floor(totals.calorie) / 100
        totals.protein = math.floor(totals.protein) / 100
        totals.fat = math.floor(totals.fat) / 100
        totals.sugar = math.floor(totals.sugar) / 100
        totals.amount = math.floor(totals.amount)

        totals.ratio = (
            math.floor((totals.fat / (totals.protein + totals.sugar)) * 100) / 100
        )
        return totals

    @property
    def author(self):
        return self.diet.author
