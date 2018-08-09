from flask import Flask
from flask_mail import Mail

app = Flask(__name__, instance_relative_config=True)

# a simple page that says hello
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY'][0]

mail = Mail()

from app import models, routes
