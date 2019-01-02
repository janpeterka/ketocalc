import os

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

SECRET_KEY = os.environ.get('SECRET_KEY')

SQLALCHEMY_TRACK_MODIFICATIONS = False
# DB_STRING = os.environ.get('DB_STRING')
SQLALCHEMY_DATABASE_URI = os.environ.get('DB_STRING')

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

TEST_VAR = os.environ.get('TEST_VAR')

APP_STATE = os.environ.get('APP_STATE')  # production, dev, debug, shutdown

# old
RECAPTCHA_SECRET = os.environ.get('RECAPTCHA_SECRET')
# new
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_SECRET')
RECAPTCHA_PUBLIC_KEY = '6LfFdWkUAAAAALQkac4_BJhv7W9Q3v11kDH62aO2'
RECAPTCHA_PARAMETERS = {'hl': 'cs', 'render': 'explicit'}
