from flask import Blueprint
from flask import render_template as template, request, redirect
from flask import flash, url_for
from flask import current_app as application

from flask_login import login_user, logout_user, current_user, login_required

from flask_dance.contrib.google import google
from flask_dance.consumer import oauth_authorized

from app.models.users import User

from app.helpers.mail import send_email

from app.auth.forms import NewPasswordForm, GetNewPasswordForm


auth_blueprint = Blueprint("auth", __name__, template_folder="templates/auth/")


@auth_blueprint.route("/auth_login")
def show_login():
    """ This exist only for login_manager """
    return redirect(url_for("LoginView:show"))


@oauth_authorized.connect
def oauth_login(blueprint, token):
    # TODO: rewrite for multiple oaths @TEST (30)
    if blueprint.name == "google":
        try:
            user_info = google.get("/oauth2/v2/userinfo").json()
            # username = user_info["email"]
            google_id = user_info["id"]
        except Exception as e:
            application.logger.error(e)
    else:
        # not implemented
        return False

    if blueprint.name == "google":
        user = User.load(google_id, load_type="google_id")

    if user:
        do_oauth_login(user=user, oauth_type="google")
    else:
        do_oauth_register(user_info=user_info, oauth_type="google")


def do_oauth_register(*, user_info, oauth_type):
    user = User()
    user.username = user_info["username"]
    user.password = None
    user.google_id = user_info["id"]

    try:
        user.first_name = user_info["given_name"]
    except Exception:
        user.first_name = "-"

    try:
        user.last_name = user_info["family_name"]
    except Exception:
        user.last_name = "-"

    do_register(user, source="google_oauth")


def do_oauth_login(*, user, oauth_type=None):
    if oauth_type == "google":
        if user.google_id is not None:
            login_user(user)
            user.log_login()


def do_login(username=None, password=None, from_register=False):
    if not isinstance(password, bytes) and password is not None:
        password = password.encode("utf-8")

    user = User.load(username, load_type="username")

    if user is not None and user.check_login(password):
        login_user(user, remember=True)
        user.log_login()

        if not from_register:
            flash("Byl jste úspěšně přihlášen.", "success")
        else:
            flash("Byl jste úspěšně zaregistrován.", "success")
        return True
    else:
        flash("Přihlášení se nezdařilo.", "error")
        return False


@login_required
@auth_blueprint.route("/logout")
def do_logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Byl jste úspěšně odhlášen.", "info")
    return redirect(url_for("LoginView:show"))


def do_register(user, source=None):
    if user.save() is True:
        user.add_default_ingredients()
        if source == "google_oauth":
            do_login(user=user)
        else:
            do_login(
                username=user.username,
                password=user.password.encode("utf-8"),
                from_register=True,
            )
        return True
    else:
        flash("Registrace neproběhla v pořádku", "error")
        return False


def validate_register(username):
    """
    Tests for registration validity:
        - unique username

    Arguments:
        username {string}
    Returns:
        bool
    """
    if User.load(username, load_type="username") is not None:
        return False
    else:
        return True


def generate_new_password_token(user):
    import secrets

    token = secrets.token_hex(40)
    set_new_password_token(user, token)
    return token


def set_new_password_token(user, token):
    user.new_password_token = token
    user.edit()
    return True


@auth_blueprint.route("/get_new_password", methods=["GET", "POST"])
def get_new_password():
    form = GetNewPasswordForm(request.form)
    if request.method == "GET":
        return template("auth/get_new_password.html.j2", form=form)
    elif request.method == "POST":
        if not form.validate_on_submit():
            return template("auth/get_new_password.html.j2", form=form)

        user = User.load(form.username.data, load_type="username")
        if user is None:
            form.username.errors = ["Uživatel s tímto emailem neexistuje"]
            return template("auth/get_new_password.html.j2", form=form)

        html_body = template(
            "auth/mails/_new_password_email.html.j2",
            token=generate_new_password_token(user),
        )
        send_email(
            subject="Nové heslo",
            sender="ketocalc.jmp@gmail.com",
            recipients=[user.username],
            text_body="",
            html_body=html_body,
        )
    flash("Nové heslo vám bylo zasláno do emailu", "success")
    return redirect(url_for("LoginView:show"))


@auth_blueprint.route("/new_password", methods=["GET", "POST"])
@auth_blueprint.route("/new_password/<token>", methods=["GET", "POST"])
def show_new_password(token=None):
    form = NewPasswordForm(request.form)
    user = User.load(token, load_type="new_password_token")
    if user is None:
        flash("tento token již není platný", "error")
        return redirect(url_for("LoginView:show"))

    if request.method == "GET":
        return template(
            "auth/new_password.html.j2", form=form, username=user.username, token=token
        )
    elif request.method == "POST":
        if not form.validate_on_submit():
            return template(
                "auth/new_password.html.j2",
                form=form,
                username=user.username,
                token=token,
            )

        # print(user.username)
        if user is None:
            flash("nemůžete změnit heslo", "error")
        else:
            user.set_password_hash(form.password.data.encode("utf-8"))
            user.password_version = application.config["PASSWORD_VERSION"]
            user.new_password_token = None
            user.edit()
            flash("heslo bylo změněno", "success")

        return redirect("/login")
