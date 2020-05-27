from app import db

from app.models.base_mixin import BaseMixin


class DailyPlan(db.Model, BaseMixin):
    __tablename__ = "daily_plans"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    recipes = db.relationship(
        "Recipe",
        secondary="daily_plan_has_recipes",
        # order_by="daily_plan_has_recipes.added_at",
    )

    @staticmethod
    def load_by_date(date):
        date_plan = db.session.query(DailyPlan).filter(DailyPlan.date == date).first()
        return date_plan
