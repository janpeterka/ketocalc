from flask import Flask
from flask_mail import Mail
# from flask_bootstrap import Bootstrap

application = Flask(__name__, instance_relative_config=True)

application.config.from_object('config')
application.secret_key = application.config['SECRET_KEY'][0]

mail = Mail(application)
# Bootstrap(application)

from app import models, routes
