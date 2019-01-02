from flask import Flask
from flask_mail import Mail
# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__, instance_relative_config=True)

application.config.from_object('config')
application.secret_key = application.config['SECRET_KEY']

mail = Mail(application)
# Bootstrap(application)
db = SQLAlchemy(application)

from app import models, routes
