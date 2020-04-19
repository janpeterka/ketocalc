from sqlalchemy.sql import func

from app.models.base_mixin import BaseMixin

from app import db


class RequestLog(db.Model, BaseMixin):
    __tablename__ = "request_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255))
    user_id = db.Column(db.String(255))
    remote_addr = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=func.now())
