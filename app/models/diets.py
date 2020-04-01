import datetime
from app import db

from app.models.base_mixin import BaseMixin


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

    user_id = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)

    recipes = db.relationship(
        "Recipe", secondary="diets_has_recipes", order_by="Recipe.name"
    )
    author = db.relationship("User", uselist=False, back_populates="diets")

    @property
    def is_used(self):
        if len(self.recipes) == 0:
            return False
        else:
            return True

    # TODO: only used for testing, probably want to remove (move to helper)
    @staticmethod
    def load_by_name(diet_name):
        diet = db.session.query(Diet).filter(Diet.name == diet_name).first()
        return diet
