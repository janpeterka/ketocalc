from flask_login import LoginManager
from flask_login import login_user

from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized

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
            "https://www.googleapis.com/auth/plus.me",
            "https://www.googleapis.com/auth/userinfo.email",
        ]
    )

    app.register_blueprint(google_blueprint, url_prefix="/login")

    app.register_blueprint(auth_blueprint)


@oauth_authorized.connect
def logged_in(blueprint, token):
    from app.models import User
    if blueprint.name == 'google':
        user_info = google.get("/oauth2/v2/userinfo").json()
        username = user_info['email']
        print(user_info['id'])

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User()
        user.username = username
        user.google_id = user_info['id']
        user.firstName = user_info['given_name']
        user.lastName = user_info['family_name']
        user.save()
        print('new user {}'.format(user.username))

    login_user(user)


from app.auth import routes
