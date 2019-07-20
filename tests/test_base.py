def test_assert():
    assert True


def test_application(app, client):
    # app is correctly set

    # from conftest
    assert app.config['TESTING'] is True
    # from conftest>.env.test
    assert app.config['SECRET_KEY'] == "justtesting"
    # from config.py
    assert app.config['TEMPLATES_AUTO_RELOAD'] is True


def test_request(client):
    # getting page responses
    assert client.get("/test_landing") == 200
    assert client.get("/login") == 200

    # not getting to dashboard (login required)
    assert client.get("/dashboard") == 302
