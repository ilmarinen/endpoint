from views import bp
from rest import bp as rest_bp
from flask_login import LoginManager
from endpoint.data_backends import DataLayer


login_manager = LoginManager()


def init(app):
    login_manager.init_app(app)
    app.register_blueprint(bp, url_prefix='/user')
    app.register_blueprint(rest_bp, url_prefix='/api')


@login_manager.user_loader
def load_user(user_id):
    return DataLayer.get_user_by_id(user_id)
