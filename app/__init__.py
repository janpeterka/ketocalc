from flask import Flask
from flask_mail import Mail
# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

application = Flask(__name__, instance_relative_config=True)

application.config.from_object('config')
application.secret_key = application.config['SECRET_KEY']

mail = Mail(application)
# Bootstrap(application)
db = SQLAlchemy(application)
login = LoginManager(application)
login.view = 'auth.showLogin'
login.login_message = 'Prosím přihlašte se.'

from app.auth import bp as auth_bp
application.register_blueprint(auth_bp)

from app.calc import bp as calc_bp
application.register_blueprint(calc_bp)

from app.errors import bp as errors_bp
application.register_blueprint(errors_bp)


from app import models, routes
