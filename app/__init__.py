from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

mail = Mail()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    application = Flask(__name__, instance_relative_config=True)

    application.config.from_object('config')
    application.secret_key = application.config['SECRET_KEY']

    import logging
    from flask import request

    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super().format(record)

    file_handler = logging.FileHandler('app/static/error.log')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s: %(levelname)s in %(module)s: %(message)s'
    ))
    application.logger.addHandler(file_handler)

    mail.init_app(application)
    db.init_app(application)
    migrate.init_app(application, db)

    # Main module
    from app.main import create_module as main_create_module
    main_create_module(application)

    # Auth module
    from app.auth import create_module as auth_create_module
    auth_create_module(application)

    # Calc module
    from app.calc import create_module as calc_create_module
    calc_create_module(application)

    # Erros module
    from app.errors import create_module as errors_create_module
    errors_create_module(application)

    return application
