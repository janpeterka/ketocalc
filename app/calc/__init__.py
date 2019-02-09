from app.calc.calculations import calc_blueprint


def create_module(app, **kwargs):
    app.register_blueprint(calc_blueprint)
