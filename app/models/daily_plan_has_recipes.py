import datetime
from app import db


class DailyPlanHasRecipes(db.Model):
    __tablename__ = "daily_plan_has_recipes"

    recipes_id = db.Column(
        db.ForeignKey("recipes.id"), primary_key=True, nullable=False, index=True
    )
    daily_plans_id = db.Column(
        db.ForeignKey("daily_plans.id"), primary_key=True, nullable=False, index=True
    )

    amount = db.Column(db.Float, nullable=False)
    added_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)

    daily_plan = db.relationship("DailyPlan")
    recipes = db.relationship("Recipe")
