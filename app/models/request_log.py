from sqlalchemy.sql import func

from app.models.base_mixin import BaseMixin

from app import db


class RequestLog(db.Model, BaseMixin):
    __tablename__ = "request_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=func.now())

    url = db.Column(db.String(255))
    remote_addr = db.Column(db.String(255))
    duration = db.Column(db.Float(precision=4))

    item_type = db.Column(db.Enum("user", "diet", "recipe", "ingredient"))
    item_id = db.Column(db.Integer)

    user_id = db.Column(db.ForeignKey(("users.id")), index=True)
