from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration


import pymysql
import numpy as np

pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

mail = Mail()
db = SQLAlchemy(session_options={"autoflush": False, "autocommit": False})
migrate = Migrate()
cache = Cache(config={"CACHE_TYPE": "simple"})


sentry_sdk.init(
    dsn="https://cf0294c7f1784ba2acbe5c9ed2409bef@o457759.ingest.sentry.io/5454190",
    integrations=[FlaskIntegration(), SqlalchemyIntegration()],
    traces_sample_rate=1.0,
)


def create_app(config_name="default"):
    application = Flask(__name__, instance_relative_config=True)

    # CONFIG
    from config import configs

    application.config.from_object(configs[config_name])

    # APPS
    mail.init_app(application)
    db.init_app(application)
    migrate.init_app(application, db)
    cache.init_app(application)

    # LOGGING
    from .config.config_logging import db_handler, gunicorn_logger

    application.logger.addHandler(gunicorn_logger)
    application.logger.addHandler(db_handler)

    # CONTROLLERS
    from .controllers import register_all_controllers  # noqa: F401

    register_all_controllers(application)

    from .controllers import register_error_handlers  # noqa: F401

    register_error_handlers(application)

    # MODULES

    from .auth import create_module as auth_create_module

    auth_create_module(application)

    return application
