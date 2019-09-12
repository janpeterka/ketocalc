from app.auth.routes import do_login, do_register
from app.models import User


def test_login(app, client):
    assert client.get("/login") == 200
    # username
    assert do_login("admin", "admin") is False
    assert do_login("", "") is False
    # TODO: OAuth @TEST (30)


def test_logout(app, client):
    # WIP
    assert client.get("/logout") == 302


def test_register(db):
    user = helper_create_user("test", "testtest")

    assert do_register(user) is True
    assert do_login(user.username, user.password) is True

    another_user = helper_create_user("test", "otherpassword")

    assert do_register(another_user) is False

    user.remove()
    # try login deleted user
    assert do_login(user.username, user.password) is False

    # TODO: OAuth @TEST (30)


def test_new_password(app, client, db):
    # TODO: generate new token, change password. @TEST (20)

    # TODO: try invalid token @TEST (20)

    # TODO: try already used token @TEST (20)
    pass


def helper_create_user(username, password):
    user = User(username)
    user.password = password
    user.set_password_hash(user.password.encode("utf-8"))
    user.first_name = "TEST"
    user.last_name = "TEST"
    user.password_version = "bcrypt"

    return user
