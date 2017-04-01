from endpoint.lib.http import RESTView
from endpoint.lib import formatter
from endpoint.packages.user import data_format
from flask import Blueprint, request
from flask_login import current_user, login_required
import permissions
import manage


bp = Blueprint('user_rest_views', __name__, template_folder='templates')


class AuthenticatedUserAPI(RESTView):

    @login_required
    def get(self):
        return formatter.make(current_user, data_format.user_format)


class UserModelAPI(RESTView):

    @permissions.can_view_user
    def get(self, user_id):
        user = manage.get_user_by_id(user_id)
        return formatter.make(current_user, data_format.user_format)


class UsersAPI(RESTView):

    @permissions.can_list_users
    def get(self, **kwargs):
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        users = manage.list_users(limit, offset)
        return map(lambda user: formatter.make(user, data_format.user_format), users)


bp.add_url_rule('/v1/users/authenticated_user', view_func=AuthenticatedUserAPI.as_view('authenticated_user_api'))
bp.add_url_rule('/v1/users/<int:user_id>', view_func=UserModelAPI.as_view('user_model_api'))
bp.add_url_rule('/v1/users/', view_func=UsersAPI.as_view('users_view'))
