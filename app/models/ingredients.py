import datetime

from unidecode import unidecode

from sqlalchemy import and_
from sqlalchemy.ext.hybrid import hybrid_property

from flask_login import current_user

from app import db

from app.models.item_mixin import ItemMixin
from app.models.recipes_has_ingredients import RecipeHasIngredients


class Ingredient(db.Model, ItemMixin):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    calorie = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    sugar = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    fat = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    protein = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    author = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, onupdate=datetime.datetime.now)

    is_shared = db.Column(db.Boolean)
    is_approved = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(255), default="user")

    recipes = db.relationship(
        "Recipe",
        primaryjoin="and_(Ingredient.id == remote(RecipeHasIngredients.ingredients_id), foreign(Recipe.id) == RecipeHasIngredients.recipes_id)",
        viewonly=True,
        order_by="Recipe.name",
    )

    # LOADERS

    @staticmethod
    def load_all_by_author(author, ordered=True):
        if type(author) == str:
            author_name = author
        elif hasattr(author, "username"):
            author_name = author.username
        else:
            raise AttributeError(
                "Wrong type for 'author', expected `str` or object having attribute `username`"
            )

        ingredients = Ingredient.query.filter_by(author=author_name).all()
        if ordered:
            ingredients.sort(key=lambda x: unidecode(x.name.lower()), reverse=False)
        return ingredients

    @staticmethod
    def load_all_shared(renamed=False, ordered=True):
        ingredients = Ingredient.query.filter(
            and_(Ingredient.is_shared, Ingredient.is_approved)
        ).all()

        if ordered:
            ingredients.sort(key=lambda x: unidecode(x.name.lower()), reverse=False)

        if renamed:
            for ingredient in ingredients:
                ingredient.name = ingredient.name + " (sdílené)"

        return ingredients

    @staticmethod
    def load_all_unapproved():
        ingredients = Ingredient.query.filter(
            and_(Ingredient.is_shared, Ingredient.is_approved.is_(False))
        ).all()
        ingredients.sort(key=lambda x: unidecode(x.name.lower()), reverse=False)
        return ingredients

    def load_amount_by_recipe(self, recipe_id):
        rhi = RecipeHasIngredients.query.filter_by(
            recipes_id=recipe_id, ingredients_id=self.id
        ).first()
        return rhi.amount

    def fill_from_json(self, json_ing):
        if "fixed" in json_ing:
            self.fixed = json_ing["fixed"]
        if "main" in json_ing:
            self.main = json_ing["main"]

        if "amount" in json_ing:
            self.amount = float(json_ing["amount"]) / 100  # from grams per 100g

        if "min" in json_ing and len(json_ing["min"]) > 0:
            self.min = float(json_ing["min"])

        if "max" in json_ing and len(json_ing["max"]) > 0:
            self.max = float(json_ing["max"])

    def duplicate(self):
        new_ingredient = Ingredient()

        new_ingredient.name = self.name
        new_ingredient.calorie = self.calorie
        new_ingredient.sugar = self.sugar
        new_ingredient.fat = self.fat
        new_ingredient.protein = self.protein
        new_ingredient.author = current_user.username

        # check if same doesn't already exist
        if new_ingredient.has_same:
            same_ingredient = new_ingredient.first_same
            del new_ingredient
            return same_ingredient
        else:
            return new_ingredient

    def is_author(self, user) -> bool:
        return self.author_user == user

    # SIMILAR INGREDIENTS

    def load_with_same_name(self):
        ingredients = (
            Ingredient.query.filter_by(name=self.name)
            .filter(Ingredient.is_current_user_author)
            .all()
        )
        return ingredients

    @property
    def has_with_same_name(self) -> list:
        return len(self.load_with_same_name()) > 0

    @property
    def with_same_name(self) -> list:
        return self.load_with_same_name()

    @property
    def first_with_same_name(self) -> list:
        return self.with_same_name[0] if self.with_same_name else None

    def load_similar(self, delta=0.05):
        from sqlalchemy.sql import func

        ingredients = (
            Ingredient.query.filter(
                and_(
                    func.abs(Ingredient.sugar - self.sugar) <= delta,
                    func.abs(Ingredient.protein - self.protein) <= delta,
                    func.abs(Ingredient.fat - self.fat) <= delta,
                )
            )
            .filter(Ingredient.is_current_user_author)
            .all()
        )
        return ingredients

    @property
    def similar(self) -> list:
        return self.load_similar()

    @property
    def has_similar(self) -> bool:
        return len(self.similar) > 0

    @property
    def first_similar(self):
        return self.similar[0] if self.similar else None

    @property
    def same(self) -> list:
        # TODO: z nějakého důvodu u některých surovin nefunguje s nulou (u některých ano).
        return self.load_similar(delta=0.000001)

    @property
    def first_same(self):
        return self.same[0] if self.same else None

    @property
    def has_same(self) -> bool:
        return len(self.same) > 0

    # PERMISSIONS

    def can_add(self, user) -> bool:
        return self.is_author(user) or self.is_public

    @property
    def can_current_user_add(self) -> bool:
        return self.can_add(current_user)

    def can_copy(self, user) -> bool:
        return (
            user.is_authenticated
            and not self.is_author(user)
            and (self.is_public or self.has_public_recipe)
        )

    @property
    def can_current_user_copy(self) -> bool:
        return self.can_copy(current_user)

    # PROPERTIES

    @property
    def author_user(self):
        from app.models.users import User

        user = User.load(self.author, load_type="username")
        return user

    @hybrid_property
    def is_current_user_author(self) -> bool:
        return self.author == current_user.username

    @property
    def is_used(self) -> bool:
        return True if self.recipes else False

    @property
    def has_public_recipe(self) -> bool:
        for recipe in self.recipes:
            if recipe.is_public:
                return True
        return False

    # TESTING
    # TODO: only used for testing, should be moved to tests
    def set_fixed(self, value=True, amount=0):
        self.fixed = value
        self.amount = amount
        return self

    def set_main(self, value=True):
        self.main = value
        return self
