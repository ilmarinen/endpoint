from views import bp


def init(app, admin):
    app.register_blueprint(bp, url_prefix='/twilio')