import datetime
import bcrypt
import hashlib
import unidecode

from flask import current_app as application

from flask_login import UserMixin

from app import db
from app.auth import login

from app.models.item_mixin import ItemMixin
from app.models.ingredients import Ingredient
from app.models.request_log import RequestLog


class User(db.Model, UserMixin, ItemMixin):
    """User class


    Extends:
        Base

    Variables:
        __tablename__ {str} -- DB table name
        id {int} -- user id
        username {string} -- username (email)
        pwdhash {string} -- password hash (sha256 / bcrypt)
        first_name {string} -- first name
        last_name {string} -- last name
        password_version {string} -- password version (sha256 / bcrypt)
        diets {relationship} -- diets of user
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    google_id = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    pwdhash = db.Column(db.CHAR(64), nullable=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    password_version = db.Column(db.String(45), nullable=True)

    created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)

    last_logged_in = db.Column(db.DateTime, nullable=True)
    login_count = db.Column(db.Integer, nullable=True, default=0)

    new_password_token = db.Column(db.String(255), nullable=True)

    diets = db.relationship(
        "Diet", order_by="desc(Diet.active)", back_populates="author"
    )

    sent_mails = db.relationship(
        "SentMail", order_by="desc(SentMail.created_at)", back_populates="recipient"
    )

    daily_plans = db.relationship("DailyPlan", back_populates="author")

    @staticmethod
    @login.user_loader
    def load(user_identifier, load_type="id"):
        if load_type == "id":
            user = db.session.query(User).filter(User.id == user_identifier).first()
        elif load_type == "username":
            user = (
                db.session.query(User).filter(User.username == user_identifier).first()
            )
        elif load_type == "google_id":
            user = (
                db.session.query(User).filter(User.google_id == user_identifier).first()
            )
        elif load_type == "new_password_token":
            user = (
                db.session.query(User)
                .filter(User.new_password_token == user_identifier)
                .first()
            )
        else:
            return None

        return user

    @staticmethod
    def load_by_username(username):
        return User.load(username, load_type="username")

    def set_password_hash(self, password):
        if not isinstance(password, bytes) and password is not None:
            password = password.encode("utf-8")

        self.pwdhash = bcrypt.hashpw(password, bcrypt.gensalt())
        return self

    def check_login(self, password):
        """Verifies login data

        Verifies login data and changes hash function if necessary

        Arguments:
            password {string} -- plaintext password

        Returns:
            bool -- verification
        """
        if not isinstance(password, bytes) and password is not None:
            password = password.encode("utf-8")

        db_password_hash = self.pwdhash
        if not isinstance(db_password_hash, bytes):
            db_password_hash = db_password_hash.encode("utf-8")

        if self.password_version == "SHA256":
            if hashlib.sha256(password).hexdigest() == self.pwdhash:
                # changing from sha256 to current
                self.set_password_hash(password)
                self.password_version = application.config["PASSWORD_VERSION"]
                self.edit()
                return True
            else:
                return False
        else:
            if bcrypt.checkpw(password, db_password_hash):
                return True
            else:
                return False

    def log_login(self):
        if application.config["APP_STATE"] == "production":
            self.last_logged_in = datetime.datetime.now()
            if self.login_count is None:
                self.login_count = 1
            else:
                self.login_count += 1
            self.edit()

    @property
    def recipes(self, ordered=True):
        recipes = []
        for diet in self.diets:
            recipes.extend(diet.recipes)
        if ordered is True:
            recipes.sort(
                key=lambda x: unidecode.unidecode(x.name.lower()), reverse=False
            )
        return recipes

    @property
    def active_diets(self):
        return list(filter(lambda diet: diet.active, self.diets))

    @property
    def ingredients(self, ordered=True):
        ingredients = (
            db.session.query(Ingredient)
            .filter(Ingredient.author == self.username)
            .all()
        )
        if ordered:
            ingredients.sort(
                key=lambda x: unidecode.unidecode(x.name.lower()), reverse=False
            )
        return ingredients

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    # LOGS

    @property
    def last_request(self):
        request = (
            db.session.query(RequestLog)
            .filter(RequestLog.user_id == self.id)
            .order_by(RequestLog.created_at.desc())
            .first()
        )
        return request

    # MAILING

    @property
    def onboarding_welcome_mail_sent(self):
        for mail in self.sent_mails:
            if mail.template == "mails/onboarding/welcome.html.j2":
                return mail.created_at

        return None

    @property
    def onboarding_inactive_mail_sent(self):
        for mail in self.sent_mails:
            if mail.template == "mails/onboarding/inactive.html.j2":
                return mail.created_at

        return None

    def state(self, name=None):
        if name == "onboarding_welcome":
            if (
                self.created
                and datetime.date.today() - datetime.timedelta(days=7)
                < self.created.date()
            ):
                return True
            else:
                return False
        elif name == "onboarding_inactive":
            if (
                self.created
                and datetime.date.today() - datetime.timedelta(days=30)
                < self.created.date()
                and len(self.recipes) == 0
            ):
                return True
            else:
                return False
        else:
            return False

    # TODO: TO BE REFACTORED
    @staticmethod
    def load_shared_user():
        User.load_by_attribute("username", "ketocalc.jmp@gmail.com")

    # tohle není ideální
    @property
    def is_admin(self):
        return self.username == "admin"
