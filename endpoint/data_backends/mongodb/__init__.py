from flask_admin import Admin
from database import db
from admin_views import AuthModelView, AdminUserView, AdminGroupView, AdminTokenView
from model import User, Group, Token
from manage import (
    init_db,
    get_user_by_username,
    verify_user_password,
    get_user_by_id,
    user_in_group,
    list_users,
    get_token_by_value,
    create_user,
    create_group,
    get_group_by_groupname,
    add_group_member)


def init(app):
    db.init_app(app)
    admin = Admin(app, name="endpoint", template_mode="bootstrap3")
    admin.add_view(AdminUserView(User))
    admin.add_view(AdminGroupView(Group))
    admin.add_view(AdminTokenView(Token))
