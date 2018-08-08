from rest import bp as rest_bp
from flask_login import LoginManager
from endpoint.data_backends import DataLayer


login_manager = LoginManager()


def init(app):
    app.register_blueprint(rest_bp, url_prefix='/api')
