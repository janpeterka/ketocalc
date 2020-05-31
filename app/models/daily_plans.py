from app import db

from app.models.base_mixin import BaseMixin


class DailyPlan(db.Model, BaseMixin):
    __tablename__ = "daily_plans"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)
    author = db.relationship("User", uselist=False, back_populates="daily_plans")

    recipes = db.relationship(
        "Recipe",
        primaryjoin="and_(DailyPlan.id == remote(DailyPlanHasRecipes.daily_plans_id), foreign(Recipe.id) == DailyPlanHasRecipes.recipes_id)",
        viewonly=True,
        order_by="Recipe.name",
    )

    @staticmethod
    def load_by_date(date, user_id):
        date_plan = (
            db.session.query(DailyPlan)
            .filter(DailyPlan.date == date)
            .filter(DailyPlan.user_id == user_id)
            .first()
        )
        return date_plan
