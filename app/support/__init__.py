from app.support.routes import support_blueprint


def create_module(app, **kwargs):
    app.register_blueprint(support_blueprint)
