from sqlalchemy import and_
from flask_login import current_user

from app import db

from app.models.base_mixin import BaseMixin
from app.models.request_log import RequestLog


# Custom methods for all my classes
class ItemMixin(BaseMixin):
    @property
    def json(self):
        attributes = []
        for attr in self.__dict__.keys():
            if not attr.startswith("_"):
                attributes.append(attr)

        data = {}
        for attr in attributes:
            value = getattr(self, attr)
            if isinstance(value, list):
                data[attr] = ", ".join([str(x) for x in value])
            else:
                data[attr] = value

        return data

    @property
    def view_count(self):
        logs = (
            db.session.query(RequestLog)
            .filter(
                and_(
                    RequestLog.item_id == self.id,
                    RequestLog.item_type == self.__class__.__name__.lower(),
                    RequestLog.user_id == getattr(current_user, "id", None),
                )
            )
            .all()
        )
        return len(logs)
