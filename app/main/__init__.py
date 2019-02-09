from app.main.routes import main_blueprint


def create_module(app, **kwargs):
    app.register_blueprint(main_blueprint)
