def test_application(app, client):
    # app is correctly set

    # from conftest>.env.test
    assert app.config["WTF_CSRF_ENABLED"] is False
    assert app.config["SECRET_KEY"] == "justtesting"
    # from config.py
    assert app.config["TESTING"] is True


def test_request(client):
    # getting page responses
    assert client.get("/login") == 200
    assert client.get("/register") == 200

    # not getting to dashboard (login required)
    assert client.get("/dashboard/") == 302


def test_requests_logged_in(app, db, client):
    import helpers

    helpers.test_with_authenticated_user(app)

    pages = [
        "/dashboard/",
        "/users/show/",
        "/users/edit/",
        "/kalkulacka",
        # "/daily-plans",  # having poblems with context_processors
    ]

    redirect_pages = [
        "/login",
    ]

    for page in pages:
        assert client.get(page, follow_redirects=True) == 200

    for page in redirect_pages:
        assert client.get(page) in (302, 308)
