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
            if self.id is not None:
                return True
            else:
                return False
        except DatabaseError:
            db.session.rollback()
            return False

    @staticmethod
    def load_by_level(level):
        logs = Log.query.filter_by(level=level)
        return logs

    @staticmethod
    def load_all():
        logs = Log.query.order_by(Log.timestamp.desc())
        return logs

    @staticmethod
    def load_since(date="2019-01-01"):
        logs = Log.query.filter(Log.timestamp > date).order_by(Log.timestamp.desc())
        return logs
