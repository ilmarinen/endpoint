from rest import bp as rest_bp


def init(app, admin):
    app.register_blueprint(rest_bp, url_prefix='/api')
