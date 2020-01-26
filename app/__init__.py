from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import pymysql
import numpy as np

pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

mail = Mail()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name="default"):
    application = Flask(__name__, instance_relative_config=True)

    # CONFIG
    from config import configs

    application.config.from_object(configs[config_name])

    # LOGGING
    # from app.config_logging import file_handler
    # application.logger.addHandler(file_handler)

    # from app.config_logging import mail_handler
    # application.logger.addHandler(mail_handler)

    # APPS
    mail.init_app(application)
    db.init_app(application)
    migrate.init_app(application, db)

    from app.config.config_logging import db_handler, gunicorn_logger

    application.logger.addHandler(gunicorn_logger)
    application.logger.addHandler(db_handler)

    from app.controllers import register_all_controllers  # noqa: F401

    register_all_controllers(application)

    from app.controllers import register_error_handlers  # noqa: F401

    register_error_handlers(application)

    # MODULES

    # Auth module
    from app.auth import create_module as auth_create_module

    auth_create_module(application)

    # Calc module
    from app.calc import create_module as calc_create_module

    calc_create_module(application)

    return application
