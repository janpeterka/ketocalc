import factory

from app import db
from app.models import Diet


class DietFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Diet
        sqlalchemy_session = db.session

    name = factory.Sequence(lambda n: "Diet %d" % n)
    user_id = 1
