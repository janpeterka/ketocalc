from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

mail = Mail()
db = SQLAlchemy()


def create_app():
    application = Flask(__name__, instance_relative_config=True)

    application.config.from_object('config')
    application.secret_key = application.config['SECRET_KEY']

    mail.init_app(application)
    db.init_app(application)

    from app.main import bp as main_bp
    application.register_blueprint(main_bp)

    from app.auth import create_module as auth_create_module
    auth_create_module(application)

    # from app.auth import bp as auth_bp
    # application.register_blueprint(auth_bp)

    from app.calc import bp as calc_bp
    application.register_blueprint(calc_bp)

    from app.errors import bp as errors_bp
    application.register_blueprint(errors_bp)

    return application


# application = create_app()

from app import models
