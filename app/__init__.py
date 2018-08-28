from flask import Flask
from flask_mail import Mail
# from flask_bootstrap import Bootstrap

application = Flask(__name__, instance_relative_config=True)

# a simple page that says hello
application.config.from_object('config')
application.secret_key = application.config['SECRET_KEY'][0]

mail = Mail()
# Bootstrap(application)

from app import models, routes
