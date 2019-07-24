from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


mail = Mail()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='default'):
    application = Flask(__name__, instance_relative_config=True)

    # CONFIG
    from config import configs
    application.config.from_object(configs[config_name])

    # LOGGING
    # from app.config_logging import file_handler
    # application.logger.addHandler(file_handler)

    # from app.config_logging import mail_handler
    # application.logger.addHandler(mail_handler)

    from app.config_logging import db_handler, gunicorn_logger
    application.logger.addHandler(gunicorn_logger)
    application.logger.addHandler(db_handler)

    # APPS
    mail.init_app(application)
    db.init_app(application)
    migrate.init_app(application, db)

    # MODULES

    # Main module
    from app.main import create_module as main_create_module
    main_create_module(application)

    # Auth module
    from app.auth import create_module as auth_create_module
    auth_create_module(application)

    # Calc module
    from app.calc import create_module as calc_create_module
    calc_create_module(application)

    # Errors module
    from app.errors import create_module as errors_create_module
    errors_create_module(application)

    # Support module
    from app.support import create_module as support_create_module
    support_create_module(application)

    return application
