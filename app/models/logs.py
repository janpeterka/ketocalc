from sqlalchemy.sql import func

from sqlalchemy.exc import DatabaseError

from app import db


class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    logger = db.Column(db.String(255))
    level = db.Column(db.String(255), index=True)
    msg = db.Column(db.Text)
    url = db.Column(db.String(255))
    remote_addr = db.Column(db.String(255))
    module = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=func.now())

    def save(self, **kw):
        try:
            db.session.expire_all()
            db.session.add(self)
            db.session.commit()
            return self.id is not None
        except DatabaseError:
            db.session.rollback()
            return False

    @staticmethod
    def load_by_level(level):
        return Log.query.filter_by(level=level)

    @staticmethod
    def load_all():
        return Log.query.order_by(Log.timestamp.desc())

    @staticmethod
    def load_since(date="2019-01-01"):
        return Log.query.filter(Log.timestamp > date).order_by(Log.timestamp.desc())
