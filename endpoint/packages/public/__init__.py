from views import bp


def init(app):
    app.register_blueprint(bp, url_prefix='/')
