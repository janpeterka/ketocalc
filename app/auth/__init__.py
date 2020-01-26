from functools import wraps

from flask import abort

from flask_login import LoginManager
from flask_login import current_user

from flask_dance.contrib.google import make_google_blueprint


login = LoginManager()


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin:
            return f(*args, **kwargs)
        else:
            abort(403)

    return decorated_function


def create_module(app, **kwargs):
    from app.auth.routes import auth_blueprint

    login.init_app(app)
    login.login_view = "auth.show_login"
    login.login_message = "Prosím přihlašte se."

    google_blueprint = make_google_blueprint(
        client_id=app.config.get("GOOGLE_CLIENT_ID"),
        client_secret=app.config.get("GOOGLE_CLIENT_SECRET"),
        scope=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
    )

    app.register_blueprint(google_blueprint, url_prefix="/login")
    app.register_blueprint(auth_blueprint)
