from sqlalchemy import and_
from flask_login import current_user

from app.models.base_mixin import BaseMixin
from app.models.request_log import RequestLog


# Custom methods for all my classes
class ItemMixin(BaseMixin):
    @property
    def json(self):
        attributes = [a for a in self.__dict__.keys() if not a.startswith("_")]

        data = {}
        for attr in attributes:
            value = getattr(self, attr)
            if isinstance(value, list):
                data[attr] = ", ".join([str(x) for x in value])
            else:
                data[attr] = value

        return data

    @property
    def view_count(self) -> int:
        return RequestLog.query.filter(
            and_(
                RequestLog.item_id == self.id,
                RequestLog.item_type == self.__class__.__name__.lower(),
                RequestLog.user_id == getattr(current_user, "id", None),
            )
        ).count()

    # CONTEXT PROCESSOR UTILITIES
    def link_to(self, **kwargs):
        from flask import url_for, Markup, escape

        self_view_name = f"{type(self).__name__.capitalize()}View:show"

        text = kwargs.get("text")
        if not text:
            text = escape(self.name)

        return Markup(
            f"<a data-turbo=\"false\" href='{url_for(self_view_name, id=self.id)}'> {text} </a>"
        )
