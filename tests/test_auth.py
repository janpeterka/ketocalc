from app.auth.routes import do_login, do_register
from app.models import User


def test_login(app, client):
    assert client.get("/login") == 200
    # username
    # assert do_login("admin", "adminadmin") is True
    assert do_login("admin", "admin") is False
    assert do_login("", "") is False
    # TODO OAuth


def test_logout(app, client):
    # WIP
    assert client.get("/logout") == 302


def test_register(db):
    user = User(username="test")
    user.password = "testtest"
    user.set_password_hash(user.password.encode("utf-8"))
    user.first_name = "TEST"
    user.last_name = "TEST"
    user.password_version = "bcrypt"

    assert do_register(user) is True
    assert do_login(user.username, user.password) is True

    # duplicate username
    another_user = User(username="test")
    another_user.password = "otherpassword"
    another_user.set_password_hash(another_user.password.encode("utf-8"))
    another_user.first_name = "TEST"
    another_user.last_name = "TEST"
    another_user.password_version = "bcrypt"

    assert do_register(another_user) is False

    user.remove()
    # try login deleted user
    assert do_login(user.username, user.password) is False

    # TODO OAuth


def test_new_password(app, client, db):
    # TODO generate new token, change password.

    # TODO try invalid token

    # TODO try already used token
    pass
