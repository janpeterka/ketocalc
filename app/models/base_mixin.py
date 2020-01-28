from flask import current_app as application

from sqlalchemy.exc import DatabaseError

from app import db


# Custom methods for all my classes
class BaseMixin(object):
    def edit(self, **kw):
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error("Edit error: {}".format(e))
            return False

    def save(self, **kw):
        """Saves (new) object
        """
        try:
            db.session.add(self)
            db.session.commit()
            if self.id is not None:
                return True
            else:
                return False
        except DatabaseError as e:
            db.session.rollback()
            application.logger.error("Save error: {}".format(e))
            return False

    def remove(self, **kw):
        """Deletes object
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except DatabaseError as e:
            db.session.rollback()
            application.logger.error("Remove error: {}".format(e))
            return False

    def expire(self, **kw):
        """Dumps database changes
        """
        try:
            db.session.expire(self)
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error("Expire error: {}".format(e))
            return False

    def refresh(self, **kw):
        try:
            db.session.refresh(self)
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error("Refresh error: {}".format(e))
            return False

    @property
    def json(self):
        attributes = []
        for attr in self.__dict__.keys():
            if not attr.startswith("_"):
                attributes.append(attr)

        return {attr: getattr(self, attr) for attr in attributes}
