from tests.helpers import test_with_authenticated_user, without_user


def test_application(app, client):
    # app is correctly set

    # from conftest>.env.test
    assert app.config["WTF_CSRF_ENABLED"] is False
    assert app.config["SECRET_KEY"] == "justtesting"
    # from config.py
    assert app.config["TESTING"] is True


def test_request(app, db, client):
    without_user(app)
    # getting page responses
    assert client.get("/login") == 200
    assert client.get("/register") == 200

    # not getting to dashboard (login required)
    assert client.get("/dashboard/") == 302


def test_requests_logged_in(app, db, client):
    test_with_authenticated_user(app)

    pages = [
        "/dashboard/",
        "/user/show/",
        "/user/edit/",
        "/kalkulacka",
        # "/daily-plans",  # having problems with context_processors
        "/trial-recipe",
    ]

    redirect_pages = [
        "/login",
    ]

    # WIP - tohle teda možná nebude dělat vůbec to co chci
    for page in pages:
        assert client.get(page, follow_redirects=True) == 200

    for page in redirect_pages:
        assert client.get(page) in (302, 308)
