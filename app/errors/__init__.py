from app.errors.routes import errors_blueprint


def create_module(app, **kwargs):
    app.register_blueprint(errors_blueprint)
