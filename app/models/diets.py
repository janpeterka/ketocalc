import datetime
from app import db

from app.models.item_mixin import ItemMixin


class Diet(db.Model, ItemMixin):
    __tablename__ = "diets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    calorie = db.Column(db.Float, nullable=False)
    sugar = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)

    user_id = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)

    recipes = db.relationship(
        "Recipe", secondary="diets_has_recipes", order_by="Recipe.name"
    )
    author = db.relationship("User", uselist=False, back_populates="diets")

    @property
    def is_used(self) -> bool:
        return bool(self.recipes)

    @property
    def ratio(self) -> float:
        return round(float(self.fat / (self.sugar + self.protein)), 2)
