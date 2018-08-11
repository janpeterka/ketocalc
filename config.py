import os

UPLOAD_FOLDER = '/tmp',
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif']),

SECRET_KEY = os.environ.get('SECRET_KEY'),

SQLALCHEMY_TRACK_MODIFICATIONS = False,

MAIL_SERVER = 'smtp.googlemail.com',
MAIL_PORT = 465,
MAIL_USE_TLS = False,
MAIL_USE_SSL = True,

MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),

TEST_VAR = os.environ.get('TEST_VAR')

RECAPTCHA_SECRET = os.environ.get('RECAPTCHA_SECRET')
