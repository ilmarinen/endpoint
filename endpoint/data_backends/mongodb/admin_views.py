import manage
import uuid
from flask_login import login_user, logout_user, current_user
from flask import redirect, url_for, request
from flask_admin.contrib import mongoengine


class AuthModelView(mongoengine.ModelView):

    def is_accessible(self):
        return (current_user.is_authenticated and
                manage.user_in_group(current_user, "admin"))

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("user_views.login"), next=url_for("admin"))


class AdminUserView(AuthModelView):
    column_exclude_list = ["_password", ]


class AdminGroupView(AuthModelView):
    column_exclude_list = []


class AdminTokenView(AuthModelView):
    column_exclude_list = []
    form_args = dict(value=dict(default=str(uuid.uuid4())))
