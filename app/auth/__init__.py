# from flask import flash

from flask_login import LoginManager

from flask_dance.contrib.google import make_google_blueprint

from app.auth.routes import auth_blueprint

login = LoginManager()


def create_module(app, **kwargs):
    login.init_app(app)
    login.login_view = 'auth.showLogin'
    login.login_message = 'Prosím přihlašte se.'

    google_blueprint = make_google_blueprint(
        client_id=app.config.get('GOOGLE_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
        scope=[
            # "https://www.googleapis.com/auth/plus.me",
            "https://www.googleapis.com/auth/userinfo.email",
        ]
    )

    app.register_blueprint(google_blueprint, url_prefix="/login")

    app.register_blueprint(auth_blueprint)
