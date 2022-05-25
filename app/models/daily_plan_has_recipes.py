import datetime
import types
from app import db

from app.models.base_mixin import BaseMixin


class DailyPlanHasRecipes(db.Model, BaseMixin):
    __tablename__ = "daily_plan_has_recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipes_id = db.Column(db.ForeignKey("recipes.id"), nullable=False, index=True)
    daily_plans_id = db.Column(
        db.ForeignKey("daily_plans.id"), nullable=False, index=True
    )

    amount = db.Column(db.Float, nullable=False)
    order_index = db.Column(db.Integer)
    added_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)

    daily_plan = db.relationship(
        "DailyPlan",
        backref=db.backref(
            "daily_plan_recipes", cascade="all, delete, delete-orphan", viewonly=False
        ),
    )
    recipe = db.relationship(
        "Recipe",
        backref=db.backref(
            "recipe_daily_plans", cascade="all, delete, delete-orphan", viewonly=False
        ),
    )

    # @staticmethod
    # def load_by_daily_plan_and_order_index(daily_plan, order_index):
    #     pass

    @property
    def values(self):
        values = types.SimpleNamespace()
        metrics = ["calorie", "sugar", "fat", "protein"]
        for metric in metrics:
            total = getattr(self.recipe.totals, metric)
            if getattr(self, "amount", None) is not None:
                value = (total / self.recipe.totals.amount) * self.amount
            else:
                value = total
            setattr(values, metric, value)
        return values
