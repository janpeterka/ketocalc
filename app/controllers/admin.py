from app.auth import admin_required

from app.models.recipes import Recipe
from app.models.users import User
from app.models.daily_plans import DailyPlan
from app.models.ingredients import Ingredient
from app.models.files import ImageFile
from app.models.request_log import RequestLog


from app.controllers.extended_flask_view import ExtendedFlaskView


class AdminView(ExtendedFlaskView):
    template_folder = "admin"
    decorators = [admin_required]

    def index(self):
        from app.helpers.general import created_recently, created_at_date
        from datetime import datetime
        from datetime import timedelta

        self.days = 30

        self.share_recipe_toggles = created_recently(
            RequestLog.load_by_like(attribute="url", pattern="recipes/toggle_shared"),
            days=self.days,
        )

        from flask_charts import Chart

        activity_chart = Chart("LineChart", "activity_chart")
        activity_chart.data.add_column("date", "date")
        activity_chart.data.add_column("number", "request count")

        user_activity_chart = Chart("LineChart", "user_activity_chart")
        user_activity_chart.data.add_column("date", "date")
        user_activity_chart.data.add_column("number", "user count")

        new_activity_chart = Chart("LineChart", "new_activity_chart")
        new_activity_chart.data.add_column("date", "date")
        new_activity_chart.data.add_column("number", "ingredients")
        new_activity_chart.data.add_column("number", "recipes")
        new_activity_chart.data.add_column("number", "users")
        new_activity_chart.data.add_column("number", "images")
        new_activity_chart.data.add_column("number", "daily plans")
        new_activity_chart.data.add_column("number", "shared toggles")

        for i in range(self.days):
            date = (datetime.today() - timedelta(days=self.days - (i + 1))).date()
            day_requests = [
                request
                for request in RequestLog.created_at_date(date)
                if not request.user.is_admin
            ]
            daily_active_users = len(
                set([r.user_id for r in day_requests if not r.user.is_admin])
            )

            ingredients = [
                ingredient
                for ingredient in Ingredient.created_at_date(date)
                if not ingredient.author_user.is_admin
            ]
            recipes = [
                recipe
                for recipe in Recipe.created_at_date(date)
                if not recipe.author.is_admin
            ]
            users = [user for user in User.created_at_date(date) if not user.is_admin]
            images = [
                image
                for image in ImageFile.created_at_date(date)
                if not image.author.is_admin
            ]
            daily_plans = [
                plan
                for plan in DailyPlan.created_at_date(date)
                if plan.is_active and not plan.author.is_admin
            ]
            share_recipe_toggles = [
                request
                for request in created_at_date(
                    RequestLog.load_by_like(
                        attribute="url", pattern="recipes/toggle_shared"
                    ),
                    date,
                )
                if not request.user.is_admin
            ]

            activity_chart.data.add_row([date, len(day_requests)])
            user_activity_chart.data.add_row([date, daily_active_users])
            new_activity_chart.data.add_row(
                [
                    date,
                    len(ingredients),
                    len(recipes),
                    len(users),
                    len(images),
                    len(daily_plans),
                    len(share_recipe_toggles),
                ]
            )

        self.charts = {
            "activity": activity_chart,
            "users": user_activity_chart,
            "new": new_activity_chart,
        }

        return self.template()
