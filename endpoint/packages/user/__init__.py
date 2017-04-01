from flask_login import LoginManager
from model import User, Group
from views import bp
from rest import bp as rest_bp
from endpoint.database import db

from flask_admin.contrib.sqla import ModelView


login_manager = LoginManager()


def init(app, admin):
    login_manager.init_app(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Group, db.session))
    app.register_blueprint(bp, url_prefix='/user')
    app.register_blueprint(rest_bp, url_prefix='/api')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
