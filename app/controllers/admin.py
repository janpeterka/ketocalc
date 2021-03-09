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
        from app.helpers.general import created_recently
        from datetime import datetime
        from datetime import timedelta

        self.days = 30
        self.new_users = User.created_in_last_30_days()
        self.new_recipes = Recipe.created_in_last_30_days()
        self.new_ingredients = Ingredient.created_in_last_30_days()
        self.daily_plans = [
            plan
            for plan in DailyPlan.created_in_last_30_days()
            if len(plan.daily_recipes) > 0
        ]
        self.new_images = ImageFile.created_in_last_30_days()
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
        for i in range(self.days):
            date = (datetime.today() - timedelta(days=self.days - (i + 1))).date()
            day_requests = RequestLog.load_by_date(date=date)
            daily_active_users = len(set([r.user_id for r in day_requests]))

            activity_chart.data.add_row([date, len(day_requests)])
            user_activity_chart.data.add_row([date, daily_active_users])

        self.charts = {"activity": activity_chart, "users": user_activity_chart}

        return self.template()
