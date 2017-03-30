from flask_login import LoginManager
from model import User
from rest import bp as rest_bp


login_manager = LoginManager()


def init(app):
    login_manager.init_app(app)
    app.register_blueprint(rest_bp, url_prefix='/api')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
